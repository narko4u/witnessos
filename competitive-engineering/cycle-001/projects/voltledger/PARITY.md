# Parity: one corpus, four runtimes, no tolerance

VoltLedger computes due dates, next-test dates, register state, reconciliation and
export bytes in four places:

| leg | what runs | where |
|---|---|---|
| oracle | `eval/oracle.py` | Python, authored the corpus |
| rust | `voltledger_core::wire::dispatch` | native, `core-rs` |
| js | `apps/capture/wire.js` | plain JavaScript fallback |
| browser | the same Rust code as WebAssembly | Chromium, the page the tester uses |

`python3 eval/gate.py` runs all four. A disagreement fails the gate. There is no
variance list and no tolerance band.

## The corpus

`eval/vectors/corpus/corpus.tsv` holds 200 cases, frozen and hashed
(`corpus.sha256`). Each row is: case id, category, op code, payload, expected
bytes. Escapes are `\\`, `\n` and `\t` and an empty result is written as
`<empty>` so nothing can pass by returning nothing.

Categories and counts:

    interval_boundary        23   leap_year                14
    month_end                16   register_state           22
    zero_invalid_interval    14   duplicate_id             12
    malformed_date           13   missing_field            12
    class_change             10   operator_override        10
    imported_history         10   reconcile_collision      14
    offline_record           10   conflicting_edit          8
    export_parity            12

Regenerate with `python3 eval/vectors/derive_corpus.py`. Do not regenerate to make
a failure go away: a red gate means one runtime is wrong and the work is to find
out which.

## How the expectations were arrived at

`derive_corpus.py` calls the oracle to fill the expected column. That is honest
about one thing and must be said plainly: the oracle authored the corpus, so the
corpus cannot prove the oracle right. Two things stop that from being circular:

1. **Twenty literal answers** in `HAND_CHECK`, worked out on paper from
   AS/NZS 3760 and the wire contract, are asserted before any case is written. If
   the oracle drifts, generation stops. They cover month-ending arithmetic, leap
   days, both status boundaries, the interval error and one worked example of each
   wire op.
2. **Three independent implementations** must reproduce all 200 rows. A mistake
   shared by the oracle and one implementation is caught by the other two. This is
   what has actually happened: the first native run disagreed on import row order,
   the first JavaScript run on expanded-year formatting and on the same import
   order. Both were real defects, fixed at source.

## Defects this gate found

Recorded because a gate that has never caught anything is decoration:

- **Import report order.** Rust grouped accepted rows then rejected rows; the
  oracle read down the file. The operator reading a report against the file they
  imported needs row order, so Rust was wrong and now interleaves by line.
- **Expanded-year formatting.** JavaScript used `toISOString()`, which writes
  `+085360-02` for years past 9999. The date was wrong for any absurd interval.
- **Non-positive intervals.** `0` and `-3` months are refused with the same words
  in all four runtimes. `-3` needed the status window and the interval parser to
  carry a signed integer; while it was unsigned, that case could not even be
  expressed, so the corpus forced the type change.

## Boundaries worth stating

- A year-past-9999 result is still a result. A 999,999 month interval is operator
  error and the contract answers rather than pretending to validate intent. This
  is recorded as a known weak spot, not a feature.
- The corpus tests the wire, not the screen. Screen behaviour has its own gate in
  `eval/e2e/run_e2e.py`, which is what caught the capture screen reading the class
  from the dropdown instead of the register.
