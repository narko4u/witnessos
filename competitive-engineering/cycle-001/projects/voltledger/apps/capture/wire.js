// The wire protocol in plain JavaScript.
//
// Same op codes, same bytes and same error strings as the Rust core: this file
// is what the app falls back to when the WASM module cannot load, so a phone
// with an unusual browser still gets the same answers as the audited core.
// It is also a full second implementation, which is what makes the 200-case
// gate meaningful: two runtimes, one contract, no tolerance.

import {
  INTERVALS_MONTHS,
  addMonths,
  nextDue,
  status,
  reconcile,
  csvParse,
  importItems,
  testsToCsv,
} from "./core.js";

const TESTS_COLUMNS = ["item_tag", "result", "tested_at", "class", "next_due", "note", "op_id"];
const ITEM_COLUMNS = ["item_tag", "description", "location", "class", "site"];

function fail(err) {
  return `ERR ${err.message}`;
}

function intOrNull(text) {
  const t = text.trim();
  if (!/^[-+]?\d+$/.test(t)) return null;
  return Number.parseInt(t, 10);
}

function opAddMonths(input) {
  const parts = input.split(",");
  if (parts.length < 2) return "ERR bad input";
  const months = intOrNull(parts[1]);
  if (months === null) return "ERR bad input";
  if (months <= 0) return "ERR months must be a positive integer";
  try {
    return addMonths(parts[0].trim(), months);
  } catch (err) {
    return fail(err);
  }
}

function opDue(input) {
  const parts = input.split(",");
  if (parts.length < 2) return "ERR bad input";
  try {
    return nextDue(parts[0].trim(), parts[1].trim());
  } catch (err) {
    return fail(err);
  }
}

function opStatus(input) {
  const parts = input.split(",");
  if (parts.length < 2) return "ERR bad input";
  const window = parts.length > 2 ? intOrNull(parts[2]) : 30;
  try {
    return status(parts[0].trim(), parts[1].trim(), window === null ? 30 : window);
  } catch (err) {
    return fail(err);
  }
}

function parseOpLine(line) {
  const f = line.split("|");
  while (f.length < 8) f.push("");
  const seq = intOrNull(f[2]);
  return {
    opId: f[0],
    deviceId: f[1],
    seq: seq === null ? 0 : seq,
    itemTag: f[3],
    result: f[4],
    testedAt: f[5],
    classKey: f[6],
    note: f[7],
  };
}

function opReconcile(input) {
  const ops = input
    .split("\n")
    .filter((line) => line.trim() !== "")
    .map(parseOpLine);

  for (const op of ops) {
    if (!op.opId) return "ERR opId required";
    if (!op.itemTag) return "ERR itemTag required";
    if (!["pass", "fail"].includes(op.result)) return `ERR bad result: ${op.result}`;
    if (!INTERVALS_MONTHS[op.classKey]) return `ERR bad class: ${op.classKey}`;
    try {
      // Date validity is the only check left; the rest was done above.
      addMonths(op.testedAt, 1);
    } catch (err) {
      return fail(err);
    }
  }

  const { state, conflicts, applied, duplicatesDropped } = reconcile(ops);
  const out = [`HDR|${applied}|${duplicatesDropped}|${conflicts.length}`];
  const tags = [...state.keys()].sort();
  for (const tag of tags) {
    const s = state.get(tag);
    out.push(
      `ITEM|${s.itemTag}|${s.result}|${s.testedAt}|${s.classKey}|${s.nextDue}|${s.opId}|${s.history}|${s.note}`,
    );
  }
  for (const c of conflicts) {
    out.push(`CONFLICT|${c.itemTag}|${c.testedAt}|${c.chosen}|${c.candidates.length}`);
  }
  return `${out.join("\n")}\n`;
}

function opImportItems(input) {
  let parsed;
  try {
    parsed = importItems(input);
  } catch (err) {
    return fail(err);
  }
  // Accepted and rejected rows interleave by line so the report reads down the
  // file the operator actually imported.
  const lines = [
    ...parsed.items.map((item) => ({
      line: item.line,
      text: `ITEM|${item.itemTag}|${item.description}|${item.location}|${item.classKey}|${item.site}`,
    })),
    ...parsed.errors.map((err) => ({
      line: err.line,
      text: `ERRROW|${err.line}|${err.reason}`,
    })),
  ].sort((a, b) => a.line - b.line);
  return lines.length ? `${lines.map((l) => l.text).join("\n")}\n` : "";
}

function opTestsCsv(input) {
  const rows = [];
  for (const line of input.split("\n")) {
    if (line.trim() === "") continue;
    const f = line.split("|");
    while (f.length < 7) f.push("");
    rows.push({
      item_tag: f[0],
      result: f[1],
      tested_at: f[2],
      class: f[3],
      next_due: f[4],
      note: f[5],
      op_id: f[6],
    });
  }
  const header = TESTS_COLUMNS.join(",");
  const esc = (v) => {
    const s = String(v ?? "");
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const body = rows.map((r) => TESTS_COLUMNS.map((c) => esc(r[c])).join(","));
  return `${[header, ...body].join("\n")}\n`;
}

function opRoundtrip(input) {
  let rows;
  try {
    rows = csvParse(input);
  } catch (err) {
    return fail(err);
  }
  if (!rows.length) return "ERR empty file";
  const header = rows[0].map((h) => h.trim().toLowerCase());
  const missing = TESTS_COLUMNS.filter((c) => !header.includes(c));
  if (missing.length) return `ERR missing columns: ${missing.join(", ")}`;
  const idx = Object.fromEntries(TESTS_COLUMNS.map((c) => [c, header.indexOf(c)]));

  const records = [];
  for (let i = 1; i < rows.length; i += 1) {
    const line = i + 1;
    const row = rows[i];
    const cell = (name) => ((row[idx[name]] ?? "").trim());
    const testedAt = cell("tested_at");
    try {
      addMonths(testedAt, 1);
    } catch (err) {
      return `ERR row ${line}: ${err.message}`;
    }
    const classKey = cell("class");
    if (!INTERVALS_MONTHS[classKey]) {
      return `ERR row ${line}: unknown class: ${classKey || "blank"}`;
    }
    const expectedDue = nextDue(classKey, testedAt);
    if (cell("next_due") !== expectedDue) {
      return `ERR row ${line}: next_due ${cell("next_due")} does not match ${expectedDue}`;
    }
    records.push({
      item_tag: cell("item_tag"),
      result: cell("result"),
      tested_at: testedAt,
      class: classKey,
      next_due: expectedDue,
      note: cell("note"),
      op_id: cell("op_id"),
    });
  }
  const esc = (v) => {
    const s = String(v ?? "");
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const body = records.map((r) => TESTS_COLUMNS.map((c) => esc(r[c])).join(","));
  return `${[TESTS_COLUMNS.join(","), ...body].join("\n")}\n`;
}

const HANDLERS = {
  1: opAddMonths,
  2: opDue,
  3: opStatus,
  4: opReconcile,
  5: opImportItems,
  6: opTestsCsv,
  8: opRoundtrip,
};

export function dispatch(op, input) {
  const fn = HANDLERS[op];
  return fn ? fn(input) : "ERR unknown op";
}

export { ITEM_COLUMNS, TESTS_COLUMNS };
