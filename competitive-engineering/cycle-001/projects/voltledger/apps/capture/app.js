// VoltLedger capture PWA. Browser wiring only: the rules live in the Rust core,
// with the JS implementation kept as the readable fallback and parity oracle.
import * as jsCore from "./core.js";
import * as jsWire from "./wire.js";
import { loadWasmCore } from "./wasm-core.js";

const wasm = await loadWasmCore("./core.wasm");
const core = wasm.ok ? wasm : jsCore;

// The browser's own entry point to the wire, whichever engine won. The corpus
// gate calls this so it scores what this page actually runs.
const runWire = (op, input) => (wasm.ok ? wasm.rawDispatch(op, input) : jsWire.dispatch(op, input));
const { status, reconcile, importItems, testsToCsv, INTERVALS_MONTHS, CLASS_LABELS, toIso } = core;

const $ = (sel) => document.querySelector(sel);
const state = { items: new Map(), records: new Map(), ops: [], deviceId: null, seq: 0, conflicts: [] };

// ---- storage -------------------------------------------------------------

let dbPromise;
function openDb() {
  if (dbPromise) return dbPromise;
  dbPromise = new Promise((resolve, reject) => {
    const req = indexedDB.open("voltledger", 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains("items")) db.createObjectStore("items", { keyPath: "itemTag" });
      if (!db.objectStoreNames.contains("ops")) {
        db.createObjectStore("ops", { keyPath: "opId" }).createIndex("itemTag", "itemTag");
      }
      if (!db.objectStoreNames.contains("meta")) db.createObjectStore("meta", { keyPath: "k" });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return dbPromise;
}

function tx(db, names, mode) {
  const t = db.transaction(names, mode);
  return { t, done: new Promise((res, rej) => { t.oncomplete = () => res(); t.onerror = () => rej(t.error); }) };
}

const req = (r) => new Promise((res, rej) => { r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });

async function loadAll() {
  const db = await openDb();
  const items = await req(db.transaction("items").objectStore("items").getAll());
  const ops = await req(db.transaction("ops").objectStore("ops").getAll());
  const meta = await req(db.transaction("meta").objectStore("meta").getAll());
  state.items = new Map(items.map((i) => [i.itemTag, i]));
  for (const m of meta) {
    if (m.k === "deviceId") state.deviceId = m.v;
    if (m.k === "seq") state.seq = m.v;
  }
  if (!state.deviceId) {
    const id = crypto.randomUUID().slice(0, 8);
    const pair = tx(db, ["meta"], "readwrite");
    pair.t.objectStore("meta").put({ k: "deviceId", v: id });
    pair.t.objectStore("meta").put({ k: "seq", v: 0 });
    await pair.done;
    state.deviceId = id;
  }
  state.ops = ops;
  recompute();
}

// One transaction: the op record and the sequence counter commit together or
// not at all, so a phone dying mid-save cannot leave a gap or a phantom test.
async function commitOp(op) {
  const db = await openDb();
  const t = tx(db, ["ops", "meta"], "readwrite");
  t.t.objectStore("ops").add(op);
  t.t.objectStore("meta").put({ k: "seq", v: op.seq });
  await t.done;
}

function recompute() {
  const r = reconcile(state.ops);
  state.records = r.state;
  state.conflicts = r.conflicts;
  render();
}

// ---- rendering -----------------------------------------------------------

// Render untrusted CSV fields as text, never executable HTML.
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function rowFor(item, rec) {
  const today = toIso(new Date());
  // Failed tests must never appear OK just because their due date is current.
  const st = rec ? (rec.result === "fail" ? "failed" : status(rec.nextDue, today)) : "untested";
  const label = { failed: "FAILED", overdue: "OVERDUE", due_soon: "DUE SOON", current: "OK", untested: "NOT TESTED" }[st];
  return `<li class="row s-${st}" data-tag="${escapeHtml(item.itemTag)}">
      <div class="tag">${escapeHtml(item.itemTag)}</div>
      <div class="desc">${escapeHtml(item.description || "no description")}<span class="loc">${escapeHtml(item.location || "")}</span></div>
      <div class="due">${rec ? rec.nextDue : "-"}<span class="pill">${label}</span></div>
    </li>`;
}

function render() {
  const items = [...state.items.values()];
  const counts = { failed: 0, overdue: 0, due_soon: 0, current: 0, untested: 0 };
  const today = toIso(new Date());
  for (const item of items) {
    const rec = state.records.get(item.itemTag);
    counts[rec ? (rec.result === "fail" ? "failed" : status(rec.nextDue, today)) : "untested"] += 1;
  }
  $("#counts").textContent =
    `${counts.overdue} overdue | ${counts.due_soon} due soon | ${counts.current} current | ${counts.untested} untested | ${counts.failed} failed`;
  $("#items").innerHTML = items.map((i) => rowFor(i, state.records.get(i.itemTag))).join("") ||
    `<li class="row empty">Import a register or add the first item.</li>`;
  $("#outbox").textContent = `${state.ops.length} records on device`;
  $("#conflicts").textContent = state.conflicts.length
    ? `${state.conflicts.length} conflict(s) need review` : "";
  $("#net").textContent = navigator.onLine ? "online" : "offline, capturing locally";
  $("#net").className = navigator.onLine ? "net up" : "net down";
}

function banner(text, kind = "ok") {
  const el = $("#banner");
  el.textContent = text;
  el.className = `banner ${kind}`;
  clearTimeout(banner.t);
  banner.t = setTimeout(() => { el.className = "banner hidden"; }, 4000);
}

// ---- capture -------------------------------------------------------------

async function saveResult(result) {
  const tag = $("#tag").value.trim();
  if (!tag) { banner("Scan or type a tag first", "bad"); return; }
  const item = state.items.get(tag);
  if (!item) { banner(`Tag ${tag} is not in the register`, "bad"); return; }
  const classKey = $("#class").value || item.classKey;
  const seq = state.seq + 1;
  const op = {
    opId: crypto.randomUUID(),
    deviceId: state.deviceId,
    seq,
    itemTag: tag,
    result,
    testedAt: $("#tested").value || toIso(new Date()),
    classKey,
    note: $("#note").value.trim(),
  };
  const t0 = performance.now();
  await commitOp(op);            // durable before the operator sees a tick
  const ms = performance.now() - t0;
  state.seq = seq;
  state.ops.push(op);
  recompute();
  $("#tag").value = "";
  $("#note").value = "";
  banner(`${tag} ${result} in ${ms.toFixed(0)}ms`, "ok");
  $("#tag").focus();
}

// ---- camera --------------------------------------------------------------

let detector = null;
async function startScan() {
  if (!("BarcodeDetector" in window)) { banner("Camera scanning is unsupported here. Type the tag instead.", "warn"); return; }
  if (!navigator.mediaDevices?.getUserMedia) { banner("Camera needs HTTPS or localhost. Type the tag instead.", "warn"); return; }
  try {
  const supported = await window.BarcodeDetector.getSupportedFormats();
  const formats = ["qr_code", "code_128", "code_39", "ean_13"].filter((f) => supported.includes(f));
  detector = new window.BarcodeDetector({ formats: formats.length ? formats : supported });
  const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
  const video = $("#video");
  video.srcObject = stream;
  $("#scan").classList.add("hidden");
  $("#scanstop").classList.remove("hidden");
  const loop = async () => {
    if (!detector) return;
    if (!video.videoWidth) { requestAnimationFrame(loop); return; }
    try {
      const codes = await detector.detect(video);
      if (codes.length) {
        $("#tag").value = codes[0].rawValue.trim();
        stopScan();
        banner(`scanned ${codes[0].rawValue}`, "ok");
        return;
      }
    } catch { /* a missed frame is not an error */ }
    requestAnimationFrame(loop);
  };
  loop();
  } catch (err) {
    stopScan();
    banner(`Camera unavailable: ${err?.message || "permission not granted"}. Enter the tag manually.`, "warn");
  }
}

function stopScan() {
  detector = null;
  const v = $("#video");
  if (v.srcObject) v.srcObject.getTracks().forEach((t) => t.stop());
  v.srcObject = null;
  $("#scan").classList.remove("hidden");
  $("#scanstop").classList.add("hidden");
}

// ---- import and export ---------------------------------------------------

async function importCsv(file) {
  const text = await file.text();
  let parsed;
  try {
    parsed = importItems(text);
  } catch (err) {
    banner(String(err.message), "bad");
    return;
  }
  const db = await openDb();
  const t = tx(db, ["items"], "readwrite");
  for (const item of parsed.items) t.t.objectStore("items").put(item);
  await t.done;
  for (const item of parsed.items) state.items.set(item.itemTag, item);
  recompute();
  banner(`imported ${parsed.items.length} items, ${parsed.errors.length} rejected`, parsed.errors.length ? "warn" : "ok");
  if (parsed.errors.length) console.table(parsed.errors);
}

function download(name, text) {
  const url = URL.createObjectURL(new Blob([text], { type: "text/csv" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

// ---- wiring --------------------------------------------------------------

// The tag decides the class, not the dropdown's first option. An operator can
// still override it afterwards, and the override is what gets recorded.
function syncClassFromTag() {
  const item = state.items.get($("#tag").value.trim());
  if (item) $("#class").value = item.classKey;
}

$("#tag").addEventListener("input", syncClassFromTag);
$("#tag").addEventListener("change", syncClassFromTag);

$("#pass").addEventListener("click", () => saveResult("pass"));
$("#fail").addEventListener("click", () => saveResult("fail"));
$("#scan").addEventListener("click", startScan);
$("#scanstop").addEventListener("click", stopScan);
$("#import").addEventListener("change", (e) => e.target.files[0] && importCsv(e.target.files[0]));
$("#export").addEventListener("click", () => download(`voltledger-tests-${toIso(new Date())}.csv`, testsToCsv(state.records)));
$("#template").addEventListener("click", () => download("voltledger-register-template.csv",
  "item_tag,description,location,class,site\n" +
  "CAB-001,Extension lead,Warehouse,factory,Maroochydore\n"));
window.addEventListener("online", render);
window.addEventListener("offline", render);

const classSelect = $("#class");
classSelect.innerHTML = Object.entries(INTERVALS_MONTHS)
  .map(([k, m]) => `<option value="${k}">${CLASS_LABELS[k]} (${m} months)</option>`).join("");
$("#tested").value = toIso(new Date());

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

await loadAll();
document.body.dataset.engine = core.ok ? "rust-wasm" : "js-fallback";
document.body.dataset.parity = wasm.ok ? `${wasm.parity.total}/${wasm.parity.total}` : wasm.reason;
// Only publish the browser test probe AFTER the live engine is recorded.
window.__volt = { engine: () => document.body.dataset.engine, run: runWire };
banner(
  core.ok ? `core rust-wasm, vectors ${wasm.parity.total}/${wasm.parity.total}` : `js fallback: ${wasm.reason}`,
  core.ok ? "ok" : "warn",
);
