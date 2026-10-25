# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Foundation v1.0.1 - interoperability patch

- New integration guide, [INTEGRATION-v1.0.1.md](INTEGRATION-v1.0.1.md): how to
  read the contract projection, the local-host Unix socket ingress boundary, the
  normative canonical mission digest with worked examples and the provisioning
  procedure for policy packs and approver roles.
- The contract projection is served at `GET /v1/foundation/cases/{case_id}` and is
  validated against the frozen schema before it is returned.
- SDK 0.1.1: `witnessos_sdk.digest.canonical_mission_digest()` and
  `WitnessOSClient.get_foundation_case()`.
- SDK 0.1.1 fixes an import error: `witnessos_sdk` exported four names its contract
  module never defined, so importing the package raised `ImportError`.

- OpenSSF Best Practices baseline evidence: DESIGN.md, THREAT-ASSESSMENT.md,
  VEX.md, MAINTAINERS.md, TESTING.md, canonical SECURITY.md, DCO check in CI.
- Release pipeline (SBOM + Sigstore signing + checksums) where a releaseable
  artifact exists.

## [0.1.0] / v0.1.0-spec - 2026-08-20

- Initial release of witnessos.
