# Security Assessment

Status: assessment performed for the current release. This document records
the most likely and impactful potential security problems for this project and
the mitigations in place. It is reviewed before each release.

## What this project is

The witnessos agent asset registry: a python package defining the schema and registry for agent assets (identities, capabilities, attestations).

## Assets

1. **Content/specification integrity** - the published content must not silently change.
2. **Tool correctness** - any shipped tooling must not be tricked into wrong output.
3. **No foothold from use** - consuming the content or running the tooling must not compromise the user's host.

## Likely and impactful problems

| # | Problem | Likelihood | Impact | Mitigation |
|---|---------|------------|--------|------------|
| Invalid asset records accepted | Medium | Medium | Schema validation + tests |
| Tampered registry data | Medium | High | Version-controlled; release signing |
| Dependency supply-chain risk | Low | Medium | Minimal deps; OSV-Scanner in CI |

## Threat model scope

- **In scope:** content integrity, tooling input handling, release integrity.
- **Explicitly out of scope:** transport security of external endpoints the user chooses to reach.

## Attack surface analysis

- Components: Asset Registry package, registry/ data, schema/.
- CI workflows: least-privilege `contents: read` permissions (plus scoped `security-events: write` for SAST).
