# Tester export intake

A capture form for the first genuine tester export. Nothing here is built until a
real file exists. The file is evidence, not development input and it is preserved
before anything else happens to it.

## Before touching the file

1. Copy the file into the evidence store byte for byte, under its original name.
2. Record the SHA-256 of that copy. This is the identity of the sample.
3. Record who provided it, on what date and their permission to use it for this
   work. A sample without provenance is not usable as evidence.
4. Never edit the original. Every later artefact is derived from a copy.

## Capture sheet

Fill every row. Where a value is not present in the file, write `absent`, never a
guess.

| Field | Value |
|---|---|
| Tester manufacturer | |
| Tester model | |
| Tester firmware version | |
| Companion software name and version | |
| Export format (CSV, TSV, TXT, XML, PDF, other) | |
| Delimiter | |
| Character encoding | |
| Byte order mark present | |
| Header row present | |
| Column names, in file order | |
| Units as printed (MΩ, Ω, mA, V, other) | |
| Date format as printed | |
| Time format as printed, if present | |
| Pass token or tokens | |
| Fail token or tokens | |
| Other verdict tokens | |
| Asset identifier source (typed into tester, scanned, assigned by software) | |
| Retest interval present or absent | |
| Operator or technician field present or absent | |
| Location or site field present or absent | |
| Notes field present or absent | |
| Rows in the sample | |
| Sample file name | |
| Sample SHA-256 | |
| Provided by | |
| Permission to use, dated | |

## Sequence after capture

1. Preserve the original bytes and hash them. Nothing else happens first.
2. Identify model, firmware and companion software version from the operator.
3. Run the existing generic profile analysis by hand against the capture sheet. No
   code change yet.
4. If the generic layer already reads the file, that is the finding: record it and
   stop. A branded adapter that adds nothing is waste.
5. Only if a gap is proven: build a fixture from the sample, define the adapter
   profile as data and register it.
6. Prove wrong-profile behaviour: the new profile must reject a file from another
   tester rather than produce plausible readings.
7. Only then design the operator flow. The flow follows real fields, never the
   other way round.

## What must stay true

- No branded adapter name appears in the product before step 5 and its fixture.
- No silent coercion of readings, dates or verdict tokens.
- The raw row is retained for every imported reading.
- A sample used as a fixture carries its provenance in the repository.

## Current state

No tester export has been obtained. Three generic profiles exist:
`generic_csv`, `generic_csv_no_header`, `generic_csv_day_first`. Branded adapters
are absent by design.
