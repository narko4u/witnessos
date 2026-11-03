// VoltLedger capture core. Pure functions, no DOM, no network, no dependencies.
// Judgement lives in the eval vectors. This file only calculates.

export const INTERVALS_MONTHS = {
  construction: 3,
  hire: 3,
  factory: 6,
  workshop: 6,
  hostile: 12,
  office_flexed: 12,
  office_low_risk: 60,
};

export const CLASS_LABELS = {
  construction: "Construction and demolition",
  hire: "Hire equipment",
  factory: "Factory and manufacturing",
  workshop: "Workshop and maintenance",
  hostile: "Hostile environment",
  office_flexed: "Office, flexed or abused",
  office_low_risk: "Office, low risk",
};

export function parseDate(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!m) throw new Error(`bad date: ${iso}`);
  const d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
  if (d.getUTCMonth() !== +m[2] - 1 || d.getUTCDate() !== +m[3]) {
    throw new Error(`not a real date: ${iso}`);
  }
  return d;
}

export function toIso(d) {
  // toISOString expands years outside 0000-9999 to "+085360-02-03", which is not
  // the wire format. Build the string from the parts instead.
  const year = String(d.getUTCFullYear()).padStart(4, "0");
  const month = String(d.getUTCMonth() + 1).padStart(2, "0");
  const day = String(d.getUTCDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function daysInMonth(year, monthIndex) {
  return new Date(Date.UTC(year, monthIndex + 1, 0)).getUTCDate();
}

// Month arithmetic with the day clamped to the last day of the target month,
// which is the only definition that keeps a 31st from rolling into the next month.
export function addMonths(iso, months) {
  if (!Number.isInteger(months) || months <= 0) throw new Error("months must be a positive integer");
  const d = parseDate(iso);
  const total = (d.getUTCMonth() + months);
  const year = d.getUTCFullYear() + Math.floor(total / 12);
  const month = ((total % 12) + 12) % 12;
  const day = Math.min(d.getUTCDate(), daysInMonth(year, month));
  return toIso(new Date(Date.UTC(year, month, day)));
}

export function nextDue(classKey, testedAt) {
  const months = INTERVALS_MONTHS[classKey];
  if (!months) throw new Error(`unknown class: ${classKey}`);
  return addMonths(testedAt, months);
}

export function status(nextDueIso, asOfIso, windowDays = 30) {
  const due = parseDate(nextDueIso).getTime();
  const now = parseDate(asOfIso).getTime();
  const day = 86400000;
  if (due < now) return "overdue";
  if (due <= now + windowDays * day) return "due_soon";
  return "current";
}

// ---- operations and reconciliation -------------------------------------

export function makeOp({
  opId,
  deviceId,
  seq,
  itemTag,
  result,
  testedAt,
  classKey,
  note = "",
}) {
  if (!opId) throw new Error("opId required");
  if (!itemTag) throw new Error("itemTag required");
  if (!["pass", "fail"].includes(result)) throw new Error(`bad result: ${result}`);
  if (!INTERVALS_MONTHS[classKey]) throw new Error(`bad class: ${classKey}`);
  parseDate(testedAt);
  if (!Number.isInteger(seq) || seq < 0) throw new Error("seq must be a non-negative integer");
  return { opId, deviceId, seq, itemTag, result, testedAt, classKey, note };
}

// Deterministic reconciliation.
// 1. An opId seen twice is applied once, whatever order it arrives in.
// 2. The current result for an item is the record with the latest testedAt; ties
//    on testedAt are broken by deviceId then seq, so two phones offline on the
//    same day cannot produce two different answers on two different devices.
// 3. A tie with different results is reported as a conflict, never merged away.
// Arrival order does not affect the outcome. That is the property the tests assert.
export function reconcile(ops) {
  const seen = new Set();
  const unique = [];
  for (const op of ops) {
    if (seen.has(op.opId)) continue;
    seen.add(op.opId);
    unique.push(op);
  }

  const byItem = new Map();
  for (const op of unique) {
    if (!byItem.has(op.itemTag)) byItem.set(op.itemTag, []);
    byItem.get(op.itemTag).push(op);
  }

  const state = new Map();
  const conflicts = [];

  for (const [itemTag, list] of byItem) {
    list.sort((a, b) =>
      a.testedAt === b.testedAt
        ? a.deviceId === b.deviceId
          ? a.seq - b.seq
          : a.deviceId < b.deviceId ? -1 : 1
        : a.testedAt < b.testedAt ? -1 : 1);

    const latest = list[list.length - 1];
    const sameDay = list.filter((o) => o.testedAt === latest.testedAt);
    const results = new Set(sameDay.map((o) => o.result));
    if (results.size > 1) {
      conflicts.push({
        itemTag,
        testedAt: latest.testedAt,
        candidates: sameDay.map((o) => ({ opId: o.opId, deviceId: o.deviceId, result: o.result })),
        chosen: latest.opId,
        rule: "latest deviceId wins, conflict retained for review",
      });
    }

    state.set(itemTag, {
      itemTag,
      result: latest.result,
      testedAt: latest.testedAt,
      classKey: latest.classKey,
      nextDue: nextDue(latest.classKey, latest.testedAt),
      note: latest.note,
      opId: latest.opId,
      history: list.length,
    });
  }

  return { state, conflicts, applied: unique.length, duplicatesDropped: ops.length - unique.length };
}

// ---- CSV ----------------------------------------------------------------

const ITEM_COLUMNS = ["item_tag", "description", "location", "class", "site"];

export function csvParse(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i += 1; }
      else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ",") { row.push(field); field = ""; }
    else if (ch === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (ch !== "\r") field += ch;
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((c) => c.trim() !== ""));
}

export function importItems(text) {
  const rows = csvParse(text);
  if (!rows.length) throw new Error("empty file");
  const header = rows[0].map((h) => h.trim().toLowerCase());
  const missing = ITEM_COLUMNS.filter((c) => !header.includes(c));
  if (missing.length) throw new Error(`missing columns: ${missing.join(", ")}`);
  const idx = Object.fromEntries(ITEM_COLUMNS.map((c) => [c, header.indexOf(c)]));

  const items = [];
  const errors = [];
  const seen = new Set();
  rows.slice(1).forEach((r, n) => {
    const line = n + 2;
    const tag = (r[idx.item_tag] || "").trim();
    const classKey = (r[idx.class] || "").trim().toLowerCase();
    if (!tag) { errors.push({ line, reason: "item_tag is empty" }); return; }
    if (seen.has(tag)) { errors.push({ line, reason: "duplicate asset id" }); return; }
    if (!INTERVALS_MONTHS[classKey]) { errors.push({ line, reason: `unknown class: ${classKey || "blank"}` }); return; }
    seen.add(tag);
    items.push({
      line,
      itemTag: tag,
      description: (r[idx.description] || "").trim(),
      location: (r[idx.location] || "").trim(),
      site: (r[idx.site] || "").trim(),
      classKey,
    });
  });
  return { items, errors };
}

export function toCsv(records, columns) {
  const esc = (v) => {
    const s = String(v ?? "");
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [columns.join(","), ...records.map((r) => columns.map((c) => esc(r[c])).join(","))].join("\n");
}

export function testsToCsv(state) {
  const cols = ["item_tag", "result", "tested_at", "class", "next_due", "note", "op_id"];
  return toCsv(
    [...state.values()].map((s) => ({
      item_tag: s.itemTag, result: s.result, tested_at: s.testedAt, "class": s.classKey,
      next_due: s.nextDue, note: s.note, op_id: s.opId,
    })),
    cols,
  );
}
