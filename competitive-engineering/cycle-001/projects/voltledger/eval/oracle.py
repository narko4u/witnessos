"""VoltLedger independent oracle.

A second implementation of the wire protocol, in Python, written against the
contract rather than against the Rust source. Its whole job is to disagree when
the product is wrong. It is used to author the 200-case corpus and to score the
runners in `corpus_gate.py`.

Wire protocol, op by op. Every implementation must reproduce these bytes.

    1 addMonths   "DATE,MONTHS"                  -> "YYYY-MM-DD" | "ERR <reason>"
    2 due         "CLASS,DATE"                   -> "YYYY-MM-DD" | "ERR <reason>"
    3 status      "DUE,AS_OF[,WINDOW]"           -> current|due_soon|overdue | "ERR <reason>"
    4 reconcile   "op|...\\nop|..."               -> HDR/ITEM/CONFLICT lines | "ERR <reason>"
    5 importItems "csv text"                     -> ITEM/ERRROW lines | "ERR <reason>"
    6 testsCsv    "tag|result|testedAt|class|nextDue|note|opId\\n..." -> CSV
    8 roundtrip   "tests csv text"                -> CSV re-emitted | "ERR <reason>"

There is no clock, no locale and no I/O in here.
"""

import calendar
from datetime import date

INTERVALS_MONTHS = {
    "construction": 3,
    "hire": 3,
    "factory": 6,
    "workshop": 6,
    "hostile": 12,
    "office_flexed": 12,
    "office_low_risk": 60,
}


def parse_date(text):
    """Strict YYYY-MM-DD. Rejects anything the calendar does not have."""
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        raise ValueError(f"bad date: {text}")
    y, m, d = text[0:4], text[5:7], text[8:10]
    if not (y.isdigit() and m.isdigit() and d.isdigit()):
        raise ValueError(f"bad date: {text}")
    yi, mi, di = int(y), int(m), int(d)
    if mi < 1 or mi > 12:
        raise ValueError(f"not a real date: {text}")
    if di < 1 or di > calendar.monthrange(yi, mi)[1]:
        raise ValueError(f"not a real date: {text}")
    return date(yi, mi, di)


def add_months(iso, months):
    """Month arithmetic with the day clamped into the target month."""
    if months <= 0:
        raise ValueError("months must be a positive integer")
    d = parse_date(iso)
    total = d.month - 1 + months
    year = d.year + total // 12
    month = total % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return f"{year:04d}-{month:02d}-{day:02d}"


def next_due(class_key, tested_at):
    if class_key not in INTERVALS_MONTHS:
        raise ValueError(f"unknown class: {class_key}")
    return add_months(tested_at, INTERVALS_MONTHS[class_key])


def status(next_due_iso, as_of_iso, window_days=30):
    due = parse_date(next_due_iso)
    now = parse_date(as_of_iso)
    if due < now:
        return "overdue"
    if (due - now).days <= window_days:
        return "due_soon"
    return "current"


# ---- wire ops ------------------------------------------------------------


def _op_add_months(text):
    parts = text.split(",")
    if len(parts) < 2:
        return "ERR bad input"
    try:
        months = int(parts[1])
    except ValueError:
        return "ERR bad input"
    try:
        return add_months(parts[0], months)
    except ValueError as exc:
        return f"ERR {exc}"


def _op_due(text):
    parts = text.split(",")
    if len(parts) < 2:
        return "ERR bad input"
    try:
        return next_due(parts[0], parts[1])
    except ValueError as exc:
        return f"ERR {exc}"


def _op_status(text):
    parts = text.split(",")
    if len(parts) < 2:
        return "ERR bad input"
    window = 30
    if len(parts) > 2:
        try:
            window = int(parts[2])
        except ValueError:
            window = 30
    try:
        return status(parts[0], parts[1], window)
    except ValueError as exc:
        return f"ERR {exc}"


class Op:
    __slots__ = ("op_id", "device_id", "seq", "item_tag", "result", "tested_at", "class_key", "note")


def parse_op(line):
    f = line.split("|")
    while len(f) < 8:
        f.append("")
    op = Op()
    op.op_id, op.device_id = f[0], f[1]
    try:
        op.seq = int(f[2])
    except ValueError:
        op.seq = 0
    op.item_tag, op.result, op.tested_at, op.class_key = f[3], f[4], f[5], f[6]
    op.note = f[7]
    return op


def validate_op(op):
    if not op.op_id:
        raise ValueError("opId required")
    if not op.item_tag:
        raise ValueError("itemTag required")
    if op.result not in ("pass", "fail"):
        raise ValueError(f"bad result: {op.result}")
    if op.class_key not in INTERVALS_MONTHS:
        raise ValueError(f"bad class: {op.class_key}")
    parse_date(op.tested_at)


def reconcile(ops):
    seen = set()
    unique = []
    for op in ops:
        if op.op_id in seen:
            continue
        seen.add(op.op_id)
        unique.append(op)
    duplicates = len(ops) - len(unique)

    by_item = {}
    for op in unique:
        by_item.setdefault(op.item_tag, []).append(op)

    records = []
    conflicts = []
    for tag in sorted(by_item):
        items = sorted(by_item[tag], key=lambda o: (o.tested_at, o.device_id, o.seq))
        latest = items[-1]
        same_day = [o for o in items if o.tested_at == latest.tested_at]
        if len({o.result for o in same_day}) > 1:
            conflicts.append((tag, latest.tested_at, latest.op_id, len(same_day)))
        records.append(
            {
                "item_tag": tag,
                "result": latest.result,
                "tested_at": latest.tested_at,
                "class_key": latest.class_key,
                "next_due": next_due(latest.class_key, latest.tested_at),
                "note": latest.note,
                "op_id": latest.op_id,
                "history": len(items),
            }
        )
    return records, conflicts, len(unique), duplicates


def _op_reconcile(text):
    ops = [parse_op(line) for line in text.split("\n") if line.strip()]
    for op in ops:
        try:
            validate_op(op)
        except ValueError as exc:
            return f"ERR {exc}"
    records, conflicts, applied, duplicates = reconcile(ops)
    out = [f"HDR|{applied}|{duplicates}|{len(conflicts)}"]
    for r in records:
        out.append(
            "ITEM|{}|{}|{}|{}|{}|{}|{}|{}".format(
                r["item_tag"], r["result"], r["tested_at"], r["class_key"],
                r["next_due"], r["op_id"], r["history"], r["note"],
            )
        )
    for tag, tested_at, chosen, count in conflicts:
        out.append(f"CONFLICT|{tag}|{tested_at}|{chosen}|{count}")
    return "\n".join(out) + "\n"


ITEM_COLUMNS = ["item_tag", "description", "location", "class", "site"]


def csv_parse(text):
    rows, row, field, quoted, i = [], [], "", False, 0
    while i < len(text):
        ch = text[i]
        if quoted:
            if ch == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    field += '"'
                    i += 1
                else:
                    quoted = False
            else:
                field += ch
        elif ch == '"':
            quoted = True
        elif ch == ",":
            row.append(field)
            field = ""
        elif ch == "\n":
            row.append(field)
            rows.append(row)
            row, field = [], ""
        elif ch != "\r":
            field += ch
        i += 1
    if field or row:
        row.append(field)
        rows.append(row)
    return [r for r in rows if any(c.strip() for c in r)]


def csv_escape(value):
    if any(c in value for c in (",", '"', "\n")):
        return '"' + value.replace('"', '""') + '"'
    return value


def _op_import(text):
    rows = csv_parse(text)
    if not rows:
        return "ERR empty file"
    header = [h.strip().lower() for h in rows[0]]
    missing = [c for c in ITEM_COLUMNS if c not in header]
    if missing:
        return "ERR missing columns: " + ", ".join(missing)
    idx = {c: header.index(c) for c in ITEM_COLUMNS}

    def cell(row, name):
        i = idx[name]
        return (row[i] if i < len(row) else "").strip()

    out, seen = [], set()
    for n, row in enumerate(rows[1:], start=2):
        tag = cell(row, "item_tag")
        class_key = cell(row, "class").lower()
        if not tag:
            out.append(f"ERRROW|{n}|item_tag is empty")
            continue
        if tag in seen:
            out.append(f"ERRROW|{n}|duplicate asset id")
            continue
        if class_key not in INTERVALS_MONTHS:
            out.append(f"ERRROW|{n}|unknown class: {class_key or 'blank'}")
            continue
        seen.add(tag)
        out.append(
            f"ITEM|{tag}|{cell(row, 'description')}|{cell(row, 'location')}|{class_key}|{cell(row, 'site')}"
        )
    return ("\n".join(out) + "\n") if out else ""


TESTS_COLUMNS = ["item_tag", "result", "tested_at", "class", "next_due", "note", "op_id"]


def tests_to_csv(records):
    out = [",".join(TESTS_COLUMNS)]
    for r in records:
        out.append(",".join(csv_escape(r[c]) for c in TESTS_COLUMNS))
    return "\n".join(out) + "\n"


def _op_tests_csv(text):
    records = []
    for line in text.split("\n"):
        if not line.strip():
            continue
        f = line.split("|")
        while len(f) < 7:
            f.append("")
        records.append(
            {
                "item_tag": f[0], "result": f[1], "tested_at": f[2], "class": f[3],
                "next_due": f[4], "note": f[5], "op_id": f[6],
            }
        )
    return tests_to_csv(records)


def _op_roundtrip(text):
    """Export, then re-import the export, then export again: same bytes."""
    rows = csv_parse(text)
    if not rows:
        return "ERR empty file"
    header = [h.strip().lower() for h in rows[0]]
    missing = [c for c in TESTS_COLUMNS if c not in header]
    if missing:
        return "ERR missing columns: " + ", ".join(missing)
    idx = {c: header.index(c) for c in TESTS_COLUMNS}
    records = []
    for n, row in enumerate(rows[1:], start=2):
        rec = {c: (row[idx[c]] if idx[c] < len(row) else "").strip() for c in TESTS_COLUMNS}
        try:
            parse_date(rec["tested_at"])
        except ValueError as exc:
            return f"ERR row {n}: {exc}"
        if rec["class"] not in INTERVALS_MONTHS:
            return f"ERR row {n}: unknown class: {rec['class'] or 'blank'}"
        expected_due = next_due(rec["class"], rec["tested_at"])
        if rec["next_due"] != expected_due:
            return f"ERR row {n}: next_due {rec['next_due']} does not match {expected_due}"
        records.append(rec)
    return tests_to_csv(records)


DISPATCH = {
    1: _op_add_months,
    2: _op_due,
    3: _op_status,
    4: _op_reconcile,
    5: _op_import,
    6: _op_tests_csv,
    8: _op_roundtrip,
}


def dispatch(op, text):
    fn = DISPATCH.get(op)
    return fn(text) if fn else "ERR unknown op"
