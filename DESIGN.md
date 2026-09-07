# Design: witnessos

This document describes the design of the WitnessOS runtime governance product site, public specification (SPEC.md), SDK, and audit tooling: the actors, the actions
they perform, and the data flow. It accompanies
[THREAT-ASSESSMENT.md](THREAT-ASSESSMENT.md) (threat model) and
[TESTING.md](TESTING.md) (test policy).

## Purpose

The witnessos runtime governance product site, public specification (spec.md), sdk, and audit tooling.

## Actors

| Actor | Description |
| --- | --- |
| Site visitor | A prospective customer or partner who evaluates WitnessOS via the public pages (index, pricing, whitepaper, demo, casestudy, deck). |
| Auditor | A user running the audit tool to check agent runtime behaviour against the WitnessOS evidence model. |
| Specification steward | Maintains SPEC.md and the public site content. |

## Actions

| Action | Performed by | Implemented in |
| --- | --- | --- |
| Publish product site + spec | Steward | `index.html + SPEC.md + deck.html` |
| Run audit checks | Auditor | `audit-tool` |

## Data flow

```
repository (main branch)
        │
        ▼
CI (on push / pull_request) ──► validate / test / security jobs
        │
        ▼
tagged release ──► build artifacts + CycloneDX SBOM + Sigstore signatures + SHA256SUMS
```

## Design invariants

1. **Open by construction.** The content is freely licensed and version-controlled.
2. **Minimal dependencies.** Fewer dependencies means a smaller attack surface.
3. **Tamper-evident releases.** Where releases exist, assets carry Sigstore signatures and checksums.
