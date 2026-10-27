# WitnessOS public tools

Utilities that justify their own existence, kept in the public repository because they
support the product rather than extend it. Each one is standalone: no engine internals, no
private packages, no signing material.

| Tool | Purpose | Entry point |
|---|---|---|
| `agent-asset-registry/` | Catalog of known AI agent types with a schema, a validator, search and a report generator | `python3 tools/validate-registry.py` |
| `rogue-agent-audit/` | Scans an environment for ungoverned, unregistered or misbehaving agents | `python3 -m audit --target localhost` |
| `compliance/` | Generates compliance mapping reports for NSA MCP, EU AI Act, NIST CAISI and Singapore AI Verify, plus a scanner | `witnessos-compliance --help` |

Licence is Apache-2.0 in each directory.

## A mapping is not evidence

The compliance tool states which controls the WitnessOS documentation maps to product
features. That is a claim. It is labelled as one: the report says MAPPED, never PASS.
Graded evidence comes from `witnessos-verifier`, which reads a receipt and returns the
grade it observed. Where no receipt has been graded, report NOT_VERIFIED.

## Running them

```
cd agent-asset-registry && pip install pyyaml jsonschema && python3 tools/validate-registry.py
cd rogue-agent-audit    && pip install -e .            && python3 -m audit --target localhost
cd compliance           && pip install -e .            && witnessos-compliance --help
```

Each directory carries its own tests. Run them with `python3 -m pytest -q` from inside the
directory.

## Provenance

These arrived by migration on 2026-10-27 from three repositories that are now archived, each
with its history intact:

| Source repository | Head at migration | What moved |
|---|---|---|
| `empirelabs-au/witnessos-agent-asset-registry` | `d4baa1e` | everything except the repository workflows |
| `empirelabs-au/witnessos-rogue-agent-audit` | `9fde695` | everything except the repository workflows |
| `empirelabs-au/witnessos-compliance` | `96e0999` | CLI, scanner, mappings, EU AI Act templates, docker, k8s, deployment guide |

Left behind deliberately, because it has no support purpose here: internal business
material (`ecosystem/`, `partner-kit/`), the phase notes, the duplicated demo pages and the
video, copies of the ACI and AIP standards that live canonically in `narko4u/aci-spec` and
`narko4u/aip-spec`. One internal document-pull script also stayed behind.

Verification at migration: 13 tests pass across the three directories, the registry
validates 12 entries. The report generator and the HTML dashboard both produce output.
The CLI installs and runs from this tree.
