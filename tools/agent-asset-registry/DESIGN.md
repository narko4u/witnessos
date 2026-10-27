# Design: witnessos-agent-asset-registry

This document describes the design of the WitnessOS Agent Asset Registry: a Python package defining the schema and registry for agent assets (identities, capabilities, attestations): the actors, the actions
they perform, and the data flow. It accompanies
[THREAT-ASSESSMENT.md](THREAT-ASSESSMENT.md) (threat model) and
[TESTING.md](TESTING.md) (test policy).

## Purpose

The witnessos agent asset registry: a python package defining the schema and registry for agent assets (identities, capabilities, attestations).

## Actors

| Actor | Description |
| --- | --- |
| Registry operator | Maintains asset records in registry/ using the schema. |
| Tooling user | Runs tools/ helpers against the registry. |
| Schema consumer | Integrates the registry schema into WitnessOS deployments. |

## Actions

| Action | Performed by | Implemented in |
| --- | --- | --- |
| Validate asset records | Registry operator | `registry/ + schema/` |
| Run helper tools | Tooling user | `tools/` |
| Run tests | CI | `tests/` |

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
