# Tester import: an adapter boundary, not product logic

A tester prints a file. Every tester prints a different file. The import layer
exists so that difference is absorbed at one edge and never reaches the register,
the reconciliation or the evidence core.

## The shape

    core-rs/src/tester_import/
        mod.rs            the profile type, the registry, the import driver, the report
        generic_csv.rs    bytes to rows, header detection, verbatim row capture
        validation.rs     column resolution and every rejection rule
        normalisation.rs  a validated row to the VoltLedger shape

A new tester is a **profile**, which is data:

```rust
TesterProfile {
    adapter: "generic_csv_day_first",
    label: "Generic tester CSV with day-first dates",
    model: "unstated",
    delimiter: ',',
    has_header: true,
    date_format: DateFormat::DayMonthYear,
    columns: ColumnMap { item_tag: "asset id", result: "result",
                         tested_at: "test date", class: Some("environment"),
                         reading: Some("insulation"), note: Some("comments") },
    results: &[("PASS", "pass"), ("FAIL", "fail")],
}
```

Three profiles are registered today and all three are generic: `generic_csv`,
`generic_csv_no_header` and `generic_csv_day_first`. No brand appears in this
module. `adapter_metrel`, `adapter_seaward`, `adapter_fluke` and
`adapter_wavecom` are deliberately absent and a test asserts they stay absent
until a real export exists to build them from. Writing a name first and a parser
second is how a compatibility claim gets made before it is true.

## Two representations, kept apart

- **raw** - every data row, its 1-based line number and the exact text the tester
  wrote, quoting included. This is what the report quotes back.
- **normalised** - item tag, pass or fail, ISO date, advisory class, reading text,
  note. Built only after the row passed every rule.

Neither overwrites the other. The raw row is what an auditor gets when the
normalised reading is questioned.

## Nothing is coerced

| input | what happens | what does not happen |
|---|---|---|
| `>999` insulation | stored as the text `>999` | not turned into `999` or `1000` |
| `03/11/2026` under an ISO profile | row rejected, `bad date: 03/11/2026` | not interpreted day-first on a guess |
| `2026-02-30` | row rejected | not rolled forward to March |
| result token `MAYBE` | row rejected, `unknown result: MAYBE` | not counted as pass or fail |
| empty class cell | class recorded as absent | not defaulted to a class |
| duplicate asset id | second row rejected, `duplicate asset id` | not merged or silently overridden |
| empty file | refused, `empty file` | not reported as zero readings |
| missing column | whole import refused before any row | not padded with blanks |

Readings are text on purpose. An instrument that prints `OL` or `---` has told the
operator something a float cannot carry and the evidence pack has to say what the
instrument said.

## The report

`cargo run --bin import_report -- --file export.csv` prints:

    adapter, label, model        which profile read the file and that its model is unstated
    source                       the file name the operator picked, recorded not trusted
    file_sha256                  digest of the bytes, independent of the name
    total_rows, accepted
    rejected[]                   line, reason and the raw row
    readings[]                   line, item tag, result, ISO date, class, reading, note

The digest is what identifies the file. Renaming the export does not change it and
two imports of the same bytes produce the same report. SHA-256 lives in
`core-rs/src/sha256.rs` with the NIST vectors as tests, because the core ships with
no dependencies; the harness recomputes the digest with Python's `hashlib` so the
implementation is checked against a reference rather than against itself.

## What the gate proves

`python3 eval/gate.py` runs the `import` leg:

- eight Rust tests over four hand-written fixtures, naming every rejection line and
  reason;
- `eval/tester_import_gate.py`, which drives the real binary over the same fixtures
  and checks 31 independent expectations, the digest included.

Deliberately wrong-profile cases are in there too: an ISO export read with the
day-first profile must reject all four rows rather than produce four plausible
dates.

## Out of scope, on purpose

Tester Bluetooth and USB capture, tester-brand adapters and any customer-specific
mapping remain gated. The pilot reads exported files. Hardware paths wait on the
incumbent baseline and on the contractor evidence.
