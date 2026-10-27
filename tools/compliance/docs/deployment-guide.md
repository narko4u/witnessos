# WitnessOS Compliance Pack — Deployment Guide

Deploy the WitnessOS Compliance Pack to generate regulatory compliance reports for autonomous AI agents. Supports **NSA MCP**, **EU AI Act** (Articles 9, 14, 43), **NIST CAISI**, and **Singapore AI Verify**.

---

## Prerequisites

- **Python 3.11+** — CLI tested on 3.12+
- **pip** and **Git** — for installation
- **OS** — Linux (WSL supported)
- **Network** — access to WitnessOS Gateway (default `http://localhost:8100`)
- **Optional** — running WitnessOS Gateway with live evidence cases

## Installation

```bash
git clone <repo-url> witnessos-compliance
cd witnessos-compliance
pip install -e .
```

Dependencies: click, pyyaml, jinja2, rich. Verify with:

```bash
witnessos-compliance --help
```

## CLI Configuration

No runtime configuration needed. Data lives in the repo tree:

| Path | Purpose |
|---|---|
| `mappings/` | Regulatory-to-WitnessOS mapping docs |
| `templates/eu-ai-act/` | Evidence templates per article (E0–E4) |
| `content/` | Generated reports and blog assets |

Check readiness:

```bash
witnessos-compliance status --standard nsa-mcp
witnessos-compliance status --standard eu-ai-act
witnessos-compliance list          # all standards in one view
```

## Running Compliance Scans

### CLI Report Generation

```bash
# NSA MCP compliance report
witnessos-compliance report --standard nsa-mcp

# EU AI Act overview
witnessos-compliance report --standard eu-ai-act

# Specific article + evidence grade
witnessos-compliance report --standard eu-ai-act --article 9 --evidence E2

# JSON output for automation
witnessos-compliance report --standard nsa-mcp --output json
```

### Fleet Compliance Scanner

The `tools/compliance-scanner.py` script performs a live 5-step scan of your agent environment:

```bash
python tools/compliance-scanner.py
```

Pipeline:
1. **SCAN** — probes `/proc` for agent processes (Hermes, Sovereign, Autogen, etc.) and exposed credentials
2. **IDENTIFY** — matches findings against the EAB 9-agent fleet registry
3. **GRADE** — computes a letter grade (A–F) per agent
4. **VERIFY** — invokes `witnessos-verifier` to confirm E4-vertex receipts
5. **REPORT** — prints a compliance matrix and saves JSON to `~/.hermes/profiles/porgie/workspace/reports/`

## EU AI Act Reports

Covers **Article 9** (Risk Management), **Article 14** (Human Oversight), and **Article 43** (Conformity Assessment). Each supports five evidence grades:

| Grade | Meaning |
|---|---|
| E0 | Raw audit log entry |
| E1 | Signed evidence, single-agent |
| E2 | Signed with policy linkage |
| E3 | Cross-signed, multi-agent |
| E4 | Verifiable cryptographic vertex receipt |

```bash
# Available grades per article
witnessos-compliance report --standard eu-ai-act

# Generate specific evidence
witnessos-compliance report --standard eu-ai-act --article 9 --evidence E2
witnessos-compliance report --standard eu-ai-act --article 14 --evidence E4

# Structured JSON for conformity bodies
witnessos-compliance report --standard eu-ai-act --output json
```

Templates live in `templates/eu-ai-act/` as Markdown files with embedded JSON schemas.

## Gateway Integration

Query a live WitnessOS Gateway for real-time evidence.

### List All Cases

```bash
witnessos-compliance evidence --gateway http://localhost:8100
witnessos-compliance evidence --gateway http://localhost:8100 --output json
witnessos-compliance evidence --gateway http://localhost:8100 --output md   # saves report
```

### Inspect a Single Case

```bash
witnessos-compliance evidence --gateway http://localhost:8100 --case case-abc-123
```

Returns action payload, policy decision, outcome stage, and chain integrity hash.

### Gateway-Backed Reports

```bash
witnessos-compliance report --standard nsa-mcp --gateway http://localhost:8100
witnessos-compliance report --standard eu-ai-act --gateway http://localhost:8100
```

The `--gateway` flag fetches live evidence from `/v1/evidence` and overlays it onto the compliance report.

### Gateway API

- `GET /v1/evidence` — list all cases
- `GET /v1/evidence/{case_id}` — single case detail

Each case includes: `case_id`, `agent_id`, `event_count`, `evidence_grade`, `evidence_status`, action details, policy decision, outcome, and chain hashes.

---

## Quick Reference

| Command | Purpose |
|---|---|
| `pip install -e .` | Install CLI |
| `witnessos-compliance list` | Show all standards |
| `witnessos-compliance report -s nsa-mcp` | NSA MCP report |
| `witnessos-compliance report -s eu-ai-act -a 9 -e E2` | EU AI Act Article 9, E2 |
| `python tools/compliance-scanner.py` | Fleet scan |
| `witnessos-compliance evidence -g http://localhost:8100` | Gateway query |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found` | Run `pip install -e .` from repo root |
| `Cannot reach gateway` | Verify with `curl http://localhost:8100/v1/evidence` |
| Scanner finds nothing | Run on the host where agents execute |
| `verifier binary not found` | Build verifier or set PATH |

## Next Steps

1. Deploy CLI on your agent host
2. Run `witnessos-compliance list` to verify mappings
3. Execute `python tools/compliance-scanner.py` for fleet assessment
4. Generate EU AI Act evidence for each applicable article and grade
5. Connect to the WitnessOS Gateway for live monitoring
6. Schedule the scanner as a cron job for continuous compliance
