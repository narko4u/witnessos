# Corpus revisions

The 200-case corpus is acceptance evidence for the CYCLE-001 baseline. It is not a
fixture that follows the code.

## The rule

1. A change in expected behaviour is a **contract change**, not a code change. The
   code is wrong until the contract says otherwise.
2. Publishing a new version requires all four of: a new version number, a written
   reason, the old corpus preserved byte for byte and a diff naming every vector
   that moved.
3. Expectations are never regenerated because the implementation changed. If the
   gate is red, the work is to find out which runtime is wrong.

## How the rule is enforced

`eval/vectors/derive_corpus.py` refuses to write when the output differs from the
frozen corpus unless it is given a reason:

    python3 eval/vectors/derive_corpus.py
    REFUSED: corpus v1 is frozen at 40c4afe56db5150a...
    1 of 200 cases would change: C054
    Re-run with --revise "<what changed and why>" to publish a new version.

With `--revise` it archives the old file as `corpus.v1.tsv` plus its digest, appends
the change to this file, names the changed case ids, bumps `MANIFEST.json` and
records the old digest in its history. It will not overwrite an existing archive.

`eval/gate.py` recomputes the digest of `corpus.tsv` against `MANIFEST.json` on every
run, so an edit made outside the generator is caught before any runtime is judged.

Review a revision with:

    python3 eval/vectors/corpus_diff.py corpus.v1.tsv corpus.tsv

## Version history

## v1, 2026-11-03

- 200 cases, sha256 `40c4afe56db5150a1d6ec003d34847c68a15302ede38129c15d5d74574fc4a3e`.
- Baseline commit `8638bd9`, checkpoint tag `CE001-VOLTLEDGER-PRE-VALIDATION`.
- Reproduced byte for byte by four runtimes: Python oracle, native Rust, JavaScript
  and the Rust core as WebAssembly inside Chromium.
- Status: IMMUTABLE.
