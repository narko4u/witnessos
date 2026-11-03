"""Authoring script for the 200-case VoltLedger corpus.

Run once, freeze the output. The generated file is the judgement; the four
implementations are the accused.

    python3 derive_corpus.py            # writes corpus/corpus.tsv + corpus.sha256

Independence. This script authors the expected bytes by calling `eval/oracle.py`,
which is a second Python implementation written against the wire contract. The
oracle is anchored by two things that do not come from it:

  1. TWENTY literals in HAND_CHECK, worked out on paper from AS/NZS 3760 and the
     wire contract. They fail the build if the oracle drifts.
  2. Three independent implementations must reproduce all 200 rows: the Rust
     core natively, the same Rust core compiled to WASM, and the browser result
     the operator actually sees. A shared Python mistake cannot survive that.

Blank expected values do not exist: an implementation that returns nothing has
to be told so explicitly, which is why empty results are recorded as the single
token "<empty>".

Escapes: \\ -> \\\\, newline -> \\n, tab -> \\t. Nothing else is escaped.
"""

import datetime
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.dirname(HERE)
sys.path.insert(0, EVAL)

import oracle  # noqa: E402

OUT_DIR = os.path.join(HERE, "corpus")


def add(date_text, months):
    return (1, f"{date_text},{months}")


def due(class_key, date_text):
    return (2, f"{class_key},{date_text}")


def status(due_text, as_of, window=None):
    if window is None:
        return (3, f"{due_text},{as_of}")
    return (3, f"{due_text},{as_of},{window}")


def imp(header, *rows):
    return (5, "\n".join([header] + list(rows)) + "\n")


def rec(*ops):
    return (4, "\n".join(ops) + "\n")


def export(*records):
    return (6, "\n".join(records) + "\n")


def roundtrip(*rows):
    return (8, "\n".join(rows) + "\n")


ITEM_HDR = "item_tag,description,location,class,site"
TEST_HDR = "item_tag,result,tested_at,class,next_due,note,op_id"
OP = "{op}|{dev}|{seq}|{tag}|{res}|{at}|{cls}|{note}"
REC = "{tag}|{res}|{at}|{cls}|{due}|{note}|{op}"


CASES = []


def case(cat, payload):
    CASES.append((cat, payload))


# ---- 1. interval boundary dates (24) -------------------------------------
for d, m in [
    ("2026-01-31", 3), ("2026-01-31", 6), ("2026-01-31", 12), ("2026-01-31", 60),
    ("2026-03-31", 3), ("2026-03-31", 6), ("2026-03-31", 12), ("2026-03-31", 60),
    ("2026-05-31", 3), ("2026-05-31", 6), ("2026-05-31", 12), ("2026-05-31", 60),
    ("2026-08-31", 3), ("2026-08-31", 6), ("2026-08-31", 12), ("2026-08-31", 60),
    ("2026-10-31", 3), ("2026-10-31", 6), ("2026-10-31", 12), ("2026-10-31", 60),
    ("2026-12-31", 3), ("2026-12-31", 6), ("2026-12-31", 12),
]:
    case("interval_boundary", add(d, m))

# ---- 2. leap years (14) --------------------------------------------------
for d, m in [
    ("2024-02-29", 1), ("2024-02-29", 2), ("2024-02-29", 3), ("2024-02-29", 4),
    ("2024-02-29", 6), ("2024-02-29", 12), ("2024-02-29", 48), ("2024-02-29", 60),
    ("2024-02-29", 120), ("2025-02-28", 12), ("2023-02-28", 12), ("2028-02-29", 12),
    ("2024-01-31", 1), ("2027-02-28", 12),
]:
    case("leap_year", add(d, m))

# ---- 3. month-end transitions (16) --------------------------------------
for d, m in [
    ("2026-01-30", 1), ("2026-03-30", 1), ("2026-05-31", 1), ("2026-07-31", 1),
    ("2026-08-31", 1), ("2026-10-31", 1), ("2026-12-31", 1), ("2026-11-30", 1),
    ("2026-09-30", 1), ("2026-06-30", 1), ("2026-04-30", 1), ("2026-02-28", 1),
    ("2026-01-31", 2), ("2026-03-31", 2), ("2026-05-31", 2), ("2026-08-31", 2),
]:
    case("month_end", add(d, m))

# ---- 4. register states (22) --------------------------------------------
for args in [
    ("2026-11-03", "2026-11-03", 30),
    ("2026-11-03", "2026-11-02", 30),
    ("2026-11-02", "2026-11-03", 30),
    ("2026-11-03", "2026-11-03", 0),
    ("2026-11-04", "2026-11-03", 0),
    ("2026-12-03", "2026-11-03", 30),
    ("2026-12-02", "2026-11-03", 30),
    ("2026-12-04", "2026-11-03", 30),
    ("2026-11-03", "2025-11-03", 30),
    ("2026-01-01", "2025-12-31", 30),
    ("2026-01-31", "2026-01-01", 30),
    ("2026-03-01", "2026-01-30", 30),
    ("2026-02-28", "2026-01-29", 30),
    ("2024-02-29", "2024-01-31", 29),
    ("2024-03-01", "2024-01-31", 30),
    ("2026-11-03", "2026-11-03", 60),
    ("2026-11-20", "2026-11-03", 30),
    ("2026-11-21", "2026-11-03", 30),
    ("2026-12-31", "2026-12-01", 30),
    ("2026-11-03", "2026-11-04", 30),
    ("2026-06-30", "2026-05-31", 30),
    ("2026-06-30", "2026-06-01", 30),
]:
    case("register_state", status(*args))

# ---- 5. zero and invalid intervals (14) ---------------------------------
for payload in [
    "2026-11-03,0", "2026-11-03,-3", "2026-11-03,abc", "2026-11-03,1.5",
    "2026-11-03,", "2026-11-03", ",12", "2026-11-03,999999",
    "2026-02-30,3", "2026-13-01,3", "03-11-2026,3", "2026-11-03, 12",
    "2026-11-03,+6", "2026-11-03,0x6",
]:
    case("zero_invalid_interval", (1, payload))

# ---- 6. duplicate ids (12) ----------------------------------------------
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,construction,Main",
                         "CAB-001,Drill copy,Store,construction,Main"))
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,factory,Main",
                         "CAB-002,Grinder,Store,factory,Main",
                         "CAB-001,Drill again,Yard,construction,Main"))
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,factory,Main",
                         "CAB-001,Drill,Store,factory,Main",
                         "CAB-001,Drill,Store,factory,Main"))
case("duplicate_id", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note="replay"),
))
case("duplicate_id", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-11-04", cls="factory", note=""),
))
case("duplicate_id", rec(
    OP.format(op="x", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-01", cls="factory", note=""),
    OP.format(op="x", dev="phone-b", seq=9, tag="CAB-002", res="pass", at="2026-11-01", cls="factory", note=""),
))
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,factory,Main",
                         "cab-001,Drill lower,Store,factory,Main"))
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,factory,Main",
                         "CAB-002,Grinder,Store,factory,Main",
                         "CAB-002,Grinder two,Store,factory,Main",
                         "CAB-003,Press,Store,factory,Main"))
case("duplicate_id", rec(
    OP.format(op="dup", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="dup", dev="phone-b", seq=2, tag="CAB-002", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="dup", dev="phone-c", seq=3, tag="CAB-003", res="pass", at="2026-11-03", cls="factory", note=""),
))
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,factory,Main",
                         "CAB-001,Drill,Store,kitchen,Main"))
case("duplicate_id", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="first"),
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="second"),
))
case("duplicate_id", imp(ITEM_HDR,
                         "CAB-001,Drill,Store,factory,Main",
                         ",Noname,Store,factory,Main",
                         "CAB-001,Drill dup,Store,factory,Main"))

# ---- 7. malformed dates (12) --------------------------------------------
for payload in [
    due("factory", "2026-02-30"), due("factory", "2026-13-01"), due("factory", "2026-00-10"),
    due("factory", "03-11-2026"), due("factory", "2026-11-3"), due("factory", ""),
    due("factory", "2026-11-31"), due("factory", "1900-02-29"), due("factory", "2024-02-30"),
    status("2026-02-30", "2026-11-03"), status("2026-11-03", "2026-11-31"),
]:
    case("malformed_date", payload)
case("malformed_date", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-02-30", cls="factory", note=""),
))
case("malformed_date", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="03/11/2026", cls="factory", note=""),
))

# ---- 8. missing fields (12) ---------------------------------------------
case("missing_field", imp("item_tag,description,location,class", "CAB-001,Drill,Store,factory"))
case("missing_field", imp("item_tag,description,location,site", "CAB-001,Drill,Store,Main"))
case("missing_field", imp("description,location,class,site", "Drill,Store,factory,Main"))
case("missing_field", imp("item_tag,description,location,class,site", ""))
case("missing_field", imp(ITEM_HDR, "CAB-001,Drill,Store,,Main"))
case("missing_field", imp(ITEM_HDR, ",Drill,Store,factory,Main"))
case("missing_field", imp(ITEM_HDR, "CAB-001"))
case("missing_field", (5, ""))
case("missing_field", rec(OP.format(op="", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="")))
case("missing_field", rec(OP.format(op="a1", dev="phone-a", seq=1, tag="", res="pass", at="2026-11-03", cls="factory", note="")))
case("missing_field", rec(OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="", at="2026-11-03", cls="factory", note="")))
case("missing_field", rec(OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="", note="")))

# ---- 9. class changes (10) ---------------------------------------------
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-05-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="construction", note="reclassed on site"),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="construction", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-08-03", cls="hostile", note="earlier test"),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="office_low_risk", note="moved to office"),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="same day reclass"),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-002", res="pass", at="2026-11-03", cls="hire", note=""),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-12-31", cls="workshop", note=""),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="hire", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-11-04", cls="construction", note=""),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-01-31", cls="construction", note=""),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-02-28", cls="office_flexed", note=""),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2024-02-29", cls="hostile", note=""),
))
case("class_change", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="kitchen", note="bad class later"),
))

# ---- 10. operator override (10) ----------------------------------------
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="override: retest 3 months, manager instruction"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="class changed from construction to factory by office"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note="removed from service: plug damaged"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="tag, with comma"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note='quote " inside'),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="pass overridden to fail by supervisor"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="hostile", note="operator selected hostile"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="office_low_risk", note="5 year interval applied"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="construction", note="operator marked fail without reading"),
))
case("operator_override", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="note keeps leading space"),
))

# ---- 11. imported historical records (10) ------------------------------
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2024-11-03", cls="factory", note="imported from spreadsheet"),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2025-02-28", cls="construction", note=""),
    OP.format(op="h2", dev="import", seq=2, tag="CAB-002", res="fail", at="2025-08-31", cls="hostile", note="historic fail"),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2024-02-29", cls="workshop", note="leap day test"),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2026-01-31", cls="hire", note=""),
    OP.format(op="h2", dev="import", seq=2, tag="CAB-001", res="fail", at="2026-04-30", cls="hire", note=""),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2026-10-31", cls="office_flexed", note=""),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2026-05-31", cls="factory", note=""),
    OP.format(op="h2", dev="import", seq=2, tag="CAB-001", res="pass", at="2026-11-30", cls="factory", note=""),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-009", res="pass", at="2025-12-31", cls="hostile", note=""),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2026-03-31", cls="construction", note=""),
    OP.format(op="h2", dev="import", seq=2, tag="CAB-002", res="pass", at="2026-03-31", cls="construction", note=""),
    OP.format(op="h3", dev="import", seq=3, tag="CAB-003", res="pass", at="2026-03-31", cls="construction", note=""),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2020-02-29", cls="office_low_risk", note="five year test"),
))
case("imported_history", rec(
    OP.format(op="h1", dev="import", seq=1, tag="CAB-001", res="pass", at="2026-08-31", cls="workshop", note=""),
    OP.format(op="h2", dev="import", seq=2, tag="CAB-002", res="fail", at="2026-08-31", cls="workshop", note=""),
))

# ---- 12. reconciliation collisions (14) --------------------------------
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-b", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-b", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a3", dev="phone-c", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-b", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-01", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a3", dev="phone-a", seq=3, tag="CAB-001", res="pass", at="2026-11-02", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="b2", dev="phone-b", seq=5, tag="CAB-002", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="b1", dev="phone-a", seq=9, tag="CAB-002", res="pass", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="tablet", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-b", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-003", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a3", dev="phone-a", seq=3, tag="CAB-002", res="pass", at="2026-11-03", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="structural", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-30", cls="construction", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-12-01", cls="construction", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-02-28", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-02-28", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2024-02-29", cls="factory", note=""),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2024-02-29", cls="factory", note=""),
))
case("reconcile_collision", rec(
    OP.format(op="a1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="first device"),
    OP.format(op="a2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="second device"),
))

# ---- 13. offline-created records (10) ---------------------------------
case("offline_record", rec(
    OP.format(op="c1", dev="phone-a", seq=7, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="created offline"),
))
case("offline_record", rec(
    OP.format(op="c1", dev="phone-b", seq=7, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="offline a"),
    OP.format(op="c2", dev="phone-c", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note="offline c"),
))
case("offline_record", rec(
    OP.format(op="c1", dev="phone-a", seq=900, tag="CAB-001", res="pass", at="2026-11-03", cls="construction", note="seq high"),
    OP.format(op="c2", dev="phone-a", seq=901, tag="CAB-001", res="fail", at="2026-11-03", cls="construction", note="seq higher"),
))
case("offline_record", rec(
    OP.format(op="c1", dev="phone-z", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="workshop", note=""),
    OP.format(op="c2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-11-03", cls="workshop", note=""),
))
case("offline_record", rec(
    OP.format(op="c3", dev="phone-a", seq=3, tag="CAB-002", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="c1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="c2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("offline_record", rec(
    OP.format(op="c1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-02", cls="factory", note="yesterday offline"),
    OP.format(op="c2", dev="phone-a", seq=2, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note="today online"),
))
case("offline_record", rec(
    OP.format(op="c1", dev="phone-a", seq=0, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="seq zero"),
))
case("offline_record", rec(
    OP.format(op="c1", dev="", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="no device id"),
))
case("offline_record", rec(
    OP.format(op="c1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="c1", dev="phone-b", seq=1, tag="CAB-002", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="c2", dev="phone-b", seq=2, tag="CAB-002", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("offline_record", rec(
    OP.format(op="c9", dev="phone-a", seq=9, tag="CAB-001", res="pass", at="2026-11-03", cls="office_flexed", note=""),
    OP.format(op="c10", dev="phone-a", seq=10, tag="CAB-001", res="pass", at="2026-11-03", cls="office_flexed", note=""),
))

# ---- 14. conflicting edits (8) -----------------------------------------
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="e2", dev="tablet", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="fail", at="2026-11-03", cls="factory", note=""),
    OP.format(op="e2", dev="phone-a", seq=2, tag="CAB-001", res="pass", at="2026-11-04", cls="factory", note="corrected next day"),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="e2", dev="phone-b", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="construction", note="class edited"),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="note a"),
    OP.format(op="e2", dev="phone-b", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="note b"),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="e2", dev="phone-b", seq=1, tag="CAB-001", res="quit", at="2026-11-03", cls="factory", note="bad result value"),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="e2", dev="phone-b", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="", note="blank class"),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    OP.format(op="e2", dev="phone-b", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note="extra|pipe"),
))
case("conflicting_edit", rec(
    OP.format(op="e1", dev="phone-a", seq=1, tag="CAB-001", res="pass", at="2026-11-03", cls="factory", note=""),
    "e2|phone-b|1|CAB-001|pass|2026-11-03|factory",
))

# ---- 15. export and re-import parity (12) ------------------------------
case("export_parity", export(
    REC.format(tag="CAB-001", res="pass", at="2026-11-03", cls="factory", due="2027-05-03", note="", op="a1"),
))
case("export_parity", export(
    REC.format(tag="CAB-001", res="pass", at="2026-11-03", cls="factory", due="2027-05-03", note="tag, with comma", op="a1"),
))
case("export_parity", export(
    REC.format(tag="CAB-001", res="fail", at="2026-11-03", cls="construction", due="2027-02-03", note='quote " inside', op="a2"),
    REC.format(tag="CAB-002", res="pass", at="2026-11-03", cls="hostile", due="2027-11-03", note="", op="a3"),
))
case("export_parity", export(
    "CAB-001|pass|2026-11-03|factory|2027-05-03|a1",
))
case("export_parity", (6, ""))
case("export_parity", roundtrip(
    TEST_HDR,
    "CAB-001,pass,2026-11-03,factory,2027-05-03,,a1",
))
case("export_parity", roundtrip(
    TEST_HDR,
    "CAB-001,pass,2026-11-03,factory,2026-05-03,,a1",
))
case("export_parity", roundtrip(
    TEST_HDR,
    "CAB-001,pass,2026-11-03,factory,2027-05-03,note, a1",
))
case("export_parity", roundtrip(
    TEST_HDR,
    'CAB-001,pass,2026-11-03,factory,2027-05-03,"tag, with comma",a1',
))
case("export_parity", roundtrip(
    TEST_HDR,
    "CAB-001,pass,2026-11-03,kitchen,2027-05-03,,a1",
))
case("export_parity", roundtrip(
    TEST_HDR,
    "CAB-001,pass,2026-02-30,factory,2027-05-03,,a1",
))
case("export_parity", roundtrip(
    "item_tag,result,tested_at,class",
    "CAB-001,pass,2026-11-03,factory",
))

# ---- hand checks --------------------------------------------------------
# Worked out on paper. If these disagree with the oracle the oracle is wrong.
HAND_CHECK = [
    (1, "2026-01-31,12", "2027-01-31"),
    (1, "2024-02-29,12", "2025-02-28"),
    (1, "2026-03-31,1", "2026-04-30"),
    (1, "2024-02-29,48", "2028-02-29"),
    (1, "2026-12-31,3", "2027-03-31"),
    (1, "2026-08-31,6", "2027-02-28"),
    (1, "2026-11-03,0", "ERR months must be a positive integer"),
    (2, "construction,2026-11-03", "2027-02-03"),
    (2, "office_low_risk,2026-11-03", "2031-11-03"),
    (2, "factory,2026-02-30", "ERR not a real date: 2026-02-30"),
    (2, "kitchen,2026-11-03", "ERR unknown class: kitchen"),
    (3, "2026-11-03,2026-11-03", "due_soon"),
    (3, "2026-11-02,2026-11-03", "overdue"),
    (3, "2026-12-03,2026-11-03", "due_soon"),
    (3, "2026-12-04,2026-11-03", "current"),
    (5, "item_tag,description,location,class,site\nCAB-001,Drill,Store,factory,Main\nCAB-001,Dup,Store,factory,Main\n",
     "ITEM|CAB-001|Drill|Store|factory|Main\nERRROW|3|duplicate asset id\n"),
    (5, "item_tag,description\nCAB-001,Drill\n", "ERR missing columns: location, class, site"),
    (6, "CAB-001|pass|2026-11-03|factory|2027-05-03||a1\n",
     "item_tag,result,tested_at,class,next_due,note,op_id\nCAB-001,pass,2026-11-03,factory,2027-05-03,,a1\n"),
    (4, "a1|phone-a|1|CAB-001|pass|2026-11-03|factory|\n",
     "HDR|1|0|0\nITEM|CAB-001|pass|2026-11-03|factory|2027-05-03|a1|1|\n"),
    (8, "item_tag,result,tested_at,class,next_due,note,op_id\nCAB-001,pass,2026-11-03,factory,2027-05-03,,a1\n",
     "item_tag,result,tested_at,class,next_due,note,op_id\nCAB-001,pass,2026-11-03,factory,2027-05-03,,a1\n"),
]


def check_hand_checks():
    bad = []
    for op, payload, expected in HAND_CHECK:
        got = oracle.dispatch(op, payload)
        if got != expected:
            bad.append((payload, expected, got))
    if bad:
        for payload, expected, got in bad:
            print(f"HAND CHECK FAILED: {payload!r}\n  expected {expected!r}\n  got      {got!r}")
        raise SystemExit("oracle disagrees with the hand-worked answers")


def esc(text):
    return text.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


MANIFEST = os.path.join(OUT_DIR, "MANIFEST.json")


def read_json(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def guard_frozen(path, body, digest):
    """The corpus is acceptance evidence. Changing it needs a version, a reason
    and the old file kept. Regenerating it because code changed is refused."""
    if not os.path.exists(path):
        return
    current = io.open(path, encoding="utf-8").read()
    if current == body:
        print("corpus unchanged")
        return

    manifest = read_json(MANIFEST) if os.path.exists(MANIFEST) else {"version": 0, "sha256": ""}
    version = int(manifest.get("version", 0))
    args = sys.argv[1:]
    if "--revise" not in args:
        old_lines = {l.split("\t")[0]: l for l in current.split("\n") if l}
        new_lines = {l.split("\t")[0]: l for l in body.split("\n") if l}
        changed = [cid for cid in sorted(set(old_lines) | set(new_lines))
                   if old_lines.get(cid) != new_lines.get(cid)]
        print(f"REFUSED: corpus v{version} is frozen at {manifest.get('sha256', '')[:16]}...")
        print(f"{len(changed)} of {len(new_lines) - 1} cases would change: {', '.join(changed[:12])}")
        print('Re-run with --revise "<what changed and why>" to publish a new version.')
        raise SystemExit(1)

    i = args.index("--revise")
    reason = args[i + 1] if len(args) > i + 1 else ""
    if not reason.strip():
        raise SystemExit("--revise needs a reason in words")

    archive = os.path.join(OUT_DIR, f"corpus.v{version}.tsv")
    if os.path.exists(archive):
        raise SystemExit(f"{archive} already exists; the old corpus is never overwritten")
    with io.open(archive, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(current)
    with io.open(os.path.join(OUT_DIR, f"corpus.v{version}.sha256"), "w", encoding="utf-8") as fh:
        fh.write(hashlib.sha256(current.encode("utf-8")).hexdigest() + f"  corpus.v{version}.tsv\n")

    old_lines = {l.split("\t")[0]: l for l in current.split("\n") if l}
    new_lines = {l.split("\t")[0]: l for l in body.split("\n") if l}
    changed = [cid for cid in sorted(set(old_lines) | set(new_lines))
               if old_lines.get(cid) != new_lines.get(cid)]

    note = [
        "",
        f"## v{version + 1}, {datetime.date.today().isoformat()}",
        "",
        f"- reason: {reason.strip()}",
        f"- old: v{version}, {len(old_lines) - 1} cases, sha256 {hashlib.sha256(current.encode('utf-8')).hexdigest()}",
        f"- new: v{version + 1}, {len(new_lines) - 1} cases, sha256 {digest}",
        f"- changed vectors ({len(changed)}): {', '.join(changed)}",
        f"- preserved at: corpus.v{version}.tsv",
    ]
    with io.open(os.path.join(OUT_DIR, "REVISIONS.md"), "a", encoding="utf-8") as fh:
        fh.write("\n".join(note) + "\n")

    manifest.update(
        {
            "version": version + 1,
            "file": "corpus.tsv",
            "sha256": digest,
            "cases": len(new_lines) - 1,
            "frozen": datetime.date.today().isoformat(),
            "status": "IMMUTABLE",
            "history": manifest.get("history", [])
            + [{"version": version, "sha256": hashlib.sha256(current.encode("utf-8")).hexdigest(),
                "cases": len(old_lines) - 1, "reason": reason.strip()}],
        }
    )
    with io.open(MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print(f"published corpus v{version + 1} with {len(changed)} changed vectors")


def main():
    check_hand_checks()
    if len(CASES) != 200:
        raise SystemExit(f"corpus is {len(CASES)} cases, contract says 200")

    os.makedirs(OUT_DIR, exist_ok=True)
    lines = ["case\tcategory\top\tpayload\texpected"]
    seen = set()
    for i, (cat, (op, payload)) in enumerate(CASES, start=1):
        cid = f"C{i:03d}"
        if cid in seen:
            raise SystemExit(f"duplicate case id {cid}")
        seen.add(cid)
        expected = oracle.dispatch(op, payload)
        if expected == "":
            expected = "<empty>"
        lines.append("\t".join([cid, cat, str(op), esc(payload), esc(expected)]))

    body = "\n".join(lines) + "\n"
    out = os.path.join(OUT_DIR, "corpus.tsv")
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    guard_frozen(out, body, digest)
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    with io.open(os.path.join(OUT_DIR, "corpus.sha256"), "w", encoding="utf-8") as fh:
        fh.write(digest + "  corpus.tsv\n")

    counts = {}
    for cat, _ in CASES:
        counts[cat] = counts.get(cat, 0) + 1
    print(f"cases {len(CASES)}  sha256 {digest}")
    for cat in sorted(counts):
        print(f"  {cat:24s} {counts[cat]}")
    print(f"written {out}")


if __name__ == "__main__":
    main()
