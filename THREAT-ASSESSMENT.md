# Security Assessment

Status: assessment performed for the current release. This document records
the most likely and impactful potential security problems for this project and
the mitigations in place. It is reviewed before each release.

## What this project is

The witnessos runtime governance product site, public specification (spec.md), sdk, and audit tooling.

## Assets

1. **Content/specification integrity** - the published content must not silently change.
2. **Tool correctness** - any shipped tooling must not be tricked into wrong output.
3. **No foothold from use** - consuming the content or running the tooling must not compromise the user's host.

## Likely and impactful problems

| # | Problem | Likelihood | Impact | Mitigation |
|---|---------|------------|--------|------------|
| Tampered site content misleading buyers | Low | Medium | Content is version-controlled; releases signed with Sigstore keyless signatures + SHA256SUMS |
| Credentials committed accidentally | Medium | High | CI blocks credential files (.env, .key, .pem); secrets policy in SECURITY.md |
| Spec drift between site and SDK | Medium | Medium | Single-repo ownership; SPEC.md is the normative source |

## Threat model scope

- **In scope:** content integrity, tooling input handling, release integrity.
- **Explicitly out of scope:** transport security of external endpoints the user chooses to reach.

## Attack surface analysis

- Components: WitnessOS site (HTML pages), SPEC.md (public spec), audit-tool.
- CI workflows: least-privilege `contents: read` permissions (plus scoped `security-events: write` for SAST).
