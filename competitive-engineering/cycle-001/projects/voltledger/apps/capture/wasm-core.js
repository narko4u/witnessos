// WASM bridge to voltledger-core (Rust). Same API shape as core.js so the app can
// run either implementation. The parity check is not optional: the browser only
// uses the WASM core if it reproduces every vector the JS and Rust suites assert.
import { INTERVALS_MONTHS, CLASS_LABELS, toIso } from "./core.js";

const OPS = { addMonths: 1, nextDue: 2, status: 3, reconcile: 4, importItems: 5, testsCsv: 6 };

export async function loadWasmCore(url = "./core.wasm") {
  let instance;
  try {
    const res = await fetch(url);
    const bytes = await res.arrayBuffer();
    ({ instance } = await WebAssembly.instantiate(bytes, {}));
  } catch (err) {
    return { ok: false, reason: `wasm unavailable: ${err.message}` };
  }

  const { emp_alloc: alloc, emp_call: call, memory } = instance.exports;
  const enc = new TextEncoder();
  const dec = new TextDecoder();

  function invoke(op, input) {
    const bytes = enc.encode(input);
    const ptr = alloc(bytes.length);
    new Uint8Array(memory.buffer, ptr, bytes.length).set(bytes);
    const packed = call(op, ptr, bytes.length);           // u64 as BigInt
    const outPtr = Number(packed >> 32n);
    const outLen = Number(packed & 0xffffffffn);
    return dec.decode(new Uint8Array(memory.buffer, outPtr, outLen));
  }

  const fail = (text) => {
    if (text.startsWith("ERR ")) throw new Error(text.slice(4));
    return text;
  };

  const api = {
    ok: true,
    engine: "rust-wasm",
    // Unmediated access to the wire: the corpus gate uses this so it scores the
    // exact code path the app runs, not a test-only wrapper.
    rawDispatch: (op, input) => invoke(op, input),
    INTERVALS_MONTHS,
    CLASS_LABELS,
    toIso,
    addMonths: (iso, months) => fail(invoke(OPS.addMonths, `${iso},${months}`)),
    nextDue: (classKey, testedAt) => fail(invoke(OPS.nextDue, `${classKey},${testedAt}`)),
    status: (due, asOf, win = 30) => fail(invoke(OPS.status, `${due},${asOf},${win}`)),

    reconcile(ops) {
      const payload = ops
        .map((o) => [o.opId, o.deviceId, o.seq, o.itemTag, o.result, o.testedAt, o.classKey,
          (o.note || "").replaceAll("|", "/")].join("|"))
        .join("\n");
      const out = invoke(OPS.reconcile, payload);
      if (out.startsWith("ERR ")) throw new Error(out.slice(4));
      const state = new Map();
      const conflicts = [];
      let applied = 0;
      let duplicatesDropped = 0;
      for (const line of out.split("\n")) {
        if (!line) continue;
        const f = line.split("|");
        if (f[0] === "HDR") {
          applied = Number(f[1]);
          duplicatesDropped = Number(f[2]);
        } else if (f[0] === "ITEM") {
          state.set(f[1], {
            itemTag: f[1], result: f[2], testedAt: f[3], classKey: f[4],
            nextDue: f[5], opId: f[6], history: Number(f[7]), note: f.slice(8).join("|"),
          });
        } else if (f[0] === "CONFLICT") {
          conflicts.push({ itemTag: f[1], testedAt: f[2], chosen: f[3], candidates: Number(f[4]) });
        }
      }
      return { state, conflicts, applied, duplicatesDropped };
    },

    importItems(text) {
      const out = invoke(OPS.importItems, text);
      if (out.startsWith("ERR ")) throw new Error(out.slice(4));
      const items = [];
      const errors = [];
      for (const line of out.split("\n")) {
        if (!line) continue;
        const f = line.split("|");
        if (f[0] === "ITEM") {
          items.push({ itemTag: f[1], description: f[2], location: f[3], classKey: f[4], site: f[5] });
        } else if (f[0] === "ERRROW") {
          errors.push({ line: Number(f[1]), reason: f[2] });
        }
      }
      return { items, errors };
    },

    testsToCsv(state) {
      const payload = [...state.values()]
        .map((s) => [s.itemTag, s.result, s.testedAt, s.classKey, s.nextDue,
          (s.note || "").replaceAll("|", "/"), s.opId].join("|"))
        .join("\n");
      return invoke(OPS.testsCsv, payload);
    },
  };

  // Parity: the same cases the Rust and Node suites assert, run through WASM
  // before a single test record is allowed near it.
  const vectors = [
    ["addMonths", ["2026-01-31", 12], "2027-01-31"],
    ["addMonths", ["2024-02-29", 12], "2025-02-28"],
    ["addMonths", ["2026-08-31", 3], "2026-11-30"],
    ["nextDue", ["construction", "2026-11-03"], "2027-02-03"],
    ["nextDue", ["hostile", "2026-11-03"], "2027-11-03"],
    ["status", ["2026-11-03", "2026-11-03", 30], "due_soon"],
    ["status", ["2026-11-02", "2026-11-03", 30], "overdue"],
    ["status", ["2026-12-04", "2026-11-03", 30], "current"],
  ];
  const failures = [];
  for (const [fn, args, want] of vectors) {
    const got = api[fn](...args);
    if (got !== want) failures.push(`${fn}(${args.join(",")}) = ${got}, expected ${want}`);
  }
  api.parity = { total: vectors.length, failed: failures.length, failures };
  if (failures.length) return { ok: false, reason: `parity failed: ${failures[0]}` };
  return api;
}
