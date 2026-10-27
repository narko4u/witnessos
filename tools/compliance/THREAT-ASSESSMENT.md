# Security Assessment

Status: assessment performed for the current release. This document records
the most likely and impactful potential security problems for this project and
the mitigations in place. It is reviewed before each release.

## What this project is

The witnessos compliance pack: a python cli (cli/witnessos_cli) that generates compliance reports for nsa mcp and eu ai act, plus mappings, k8s assets, and partner content.

## Assets

1. **Content/specification integrity** - the published content must not silently change.
2. **Tool correctness** - any shipped tooling must not be tricked into wrong output.
3. **No foothold from use** - consuming the content or running the tooling must not compromise the user's host.

## Likely and impactful problems

| # | Problem | Likelihood | Impact | Mitigation |
|---|---------|------------|--------|------------|
| Incorrect compliance guidance | Medium | High | Mappings are version-controlled and reviewed |
| Credential leakage in content | Low | High | Secrets policy + CI validation |
| Dependency supply-chain risk | Low | Medium | Minimal deps (click, pyyaml, jinja2, rich) |

## Threat model scope

- **In scope:** content integrity, tooling input handling, release integrity.
- **Explicitly out of scope:** transport security of external endpoints the user chooses to reach.

## Attack surface analysis

- Components: witnessos-compliance CLI, mappings/ + k8s/ + docs/.
- CI workflows: least-privilege `contents: read` permissions (plus scoped `security-events: write` for SAST).
