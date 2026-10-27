# Design: witnessos-compliance

This document describes the design of the WitnessOS Compliance Pack: a Python CLI (cli/witnessos_cli) that generates compliance reports for NSA MCP and EU AI Act, plus mappings, k8s assets, and partner content: the actors, the actions
they perform, and the data flow. It accompanies
[THREAT-ASSESSMENT.md](THREAT-ASSESSMENT.md) (threat model) and
[TESTING.md](TESTING.md) (test policy).

## Purpose

The witnessos compliance pack: a python cli (cli/witnessos_cli) that generates compliance reports for nsa mcp and eu ai act, plus mappings, k8s assets, and partner content.

## Actors

| Actor | Description |
| --- | --- |
| Compliance officer | Runs the witnessos-compliance CLI to produce reports. |
| Content steward | Maintains mappings/, k8s/, docs/. |

## Actions

| Action | Performed by | Implemented in |
| --- | --- | --- |
| Generate compliance reports | Compliance officer | `cli/witnessos_cli` |
| Validate content | CI | `docs-ci.yml` |

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
