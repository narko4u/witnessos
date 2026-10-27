# WitnessOS Compliance Pack

[![OpenSSF Best Practices - Baseline 1](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14146.json&query=badge_percentage_baseline_1&label=OpenSSF%20Baseline%201&suffix=%25&color=success)](https://www.bestpractices.dev/projects/14146) [![OpenSSF Best Practices - Baseline 2](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14146.json&query=badge_percentage_baseline_2&label=OpenSSF%20Baseline%202&suffix=%25&color=success)](https://www.bestpractices.dev/projects/14146) [![OpenSSF Best Practices - Baseline 3](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14146.json&query=badge_percentage_baseline_3&label=OpenSSF%20Baseline%203&suffix=%25&color=success)](https://www.bestpractices.dev/projects/14146)

**Regulatory readiness for autonomous AI agents.**
Built on the [WitnessOS](https://github.com/narko4u/witnessos) enforcement platform.

## What This Repo Contains

| Directory | Purpose |
|-----------|---------|
| `mappings/` | NSA MCP Security Guidance → WitnessOS feature mapping + NIST/ISO/C SA/ Singapore alignment |
| `templates/eu-ai-act/` | E0-E4 evidence templates for EU AI Act Articles 9, 14, 43 |
| `cli/` | `witnessos compliance` CLI — generate compliance reports |
| `content/blog/` | Positioning docs, blog posts, competitive analysis, technical tutorials |
| `docs/` | Updated architecture docs, deployment guide, interactive demos |
| `aci/py/` | ACI (Agent Capability Interface) Python package — schema + validation |
| `aip/go/` | AIP (Agent Interaction Protocol) Go module |
| `tools/` | Compliance scanner — fleet-wide agent governance audit |
| `docker/` | Enterprise deployment: Dockerfile + docker-compose.yml |
| `k8s/` | Kubernetes manifests for production deployment |
| `partner-kit/` | Design partner program — agreement, engagement model, onboarding checklist, technical guide |
| `ecosystem/` | Phase 6 launch — outreach sequence, revenue ops framework, community launch plan, OpenAI pipeline |

## Linked Repositories

- [`witnessos`](https://github.com/narko4u/witnessos) — Core WitnessOS runtime governance platform (public)
- [`witnessos-alpha`](https://github.com/narko4u/witnessos-alpha) — Alpha preview (public)
- [`witnessos-rogue-agent-audit`](https://github.com/narko4u/witnessos-rogue-agent-audit) — Agent discovery tool (public)
- [`eu-ai-act-compliance-grade`](https://github.com/narko4u/eu-ai-act-compliance-grade) — Self-assessment tool (public)

## Standards Alignment

- **NSA CSI** — Model Context Protocol: Security Design Considerations (June 2, 2026)
- **EU AI Act** — Articles 9 (Risk Management), 14 (Human Oversight), 43 (Conformity Assessment)
- **CSA** — Cloud Security Alliance AI Agent Governance Gap Research Note (April 3, 2026)
- **NIST AI 600-1** — AI Risk Management Framework
- **ISO/IEC 42001** — AI Management System
- **Singapore AI Verify** — AI Governance Testing Framework

## Phase Completion Status

| Phase | Title | Status | Date |
|-------|-------|--------|------|
| **Phase 1** | Foundation — NSA mapping, EU AI Act templates, CLI, positioning | ✅ Complete | Jul 28, 2026 |
| **Phase 2** | Build & Deploy — interactive demo, receipt visualizer, blog, GitHub push | ✅ Complete | Jul 28, 2026 |
| **Phase 3** | Commerce & Content — commerce demo, rogue agent video, landing page, compliance mapping, ACI/AIP packages | ✅ Complete | Jul 28, 2026 |
| **Phase 4** | Revenue & Reach — OpenAI pipeline, lead capture, ACI docs, content pipeline, community | ✅ Complete | Jul 29, 2026 |
| **Phase 5** | Scale & Enterprise — Docker Compose, k8s manifests, design partner kit | ✅ Complete | Jul 29, 2026 |
| **Phase 6** | Ecosystem & Adoption — design partners, revenue ops, community launch, OpenAI pipeline | 🚀 In Progress | Started Jul 31, 2026 |

## Quick Start

```bash
# Install the CLI
pip install witnessos-compliance

# Run a compliance report
witnessos-compliance nsa-mcp
witnessos-compliance eu-ai-act --grade E3

# Fleet-wide compliance scan
python tools/compliance-scanner.py
```

## Enterprise Deployment

```bash
# Docker
cd docker && docker compose up

# Kubernetes
kubectl apply -f k8s/
```

---

**Empire Labs Security Division** · [empirelabs.com.au](https://www.empirelabs.com.au)


---

<sub>Part of the [WitnessOS launch family](https://github.com/narko4u/witnessos): [witnessos-alpha](https://github.com/narko4u/witnessos-alpha) · [witnessos-compliance](https://github.com/narko4u/witnessos-compliance) · [eu-ai-act-compliance-grade](https://github.com/narko4u/eu-ai-act-compliance-grade) · [witnessos-rogue-agent-audit](https://github.com/narko4u/witnessos-rogue-agent-audit) · [witnessos-agent-asset-registry](https://github.com/narko4u/witnessos-agent-asset-registry) · [witnessos-verifier](https://github.com/narko4u/witnessos-verifier) · [agent-interaction-specs](https://github.com/narko4u/agent-interaction-specs) · [aci-spec](https://github.com/narko4u/aci-spec) · [aip-spec](https://github.com/narko4u/aip-spec) · [ajson](https://github.com/narko4u/ajson) — [Empire Labs Pty Ltd](https://www.empirelabs.com.au)</sub>
## Dependencies

The CLI declares its dependencies in `pyproject.toml`: `click`, `pyyaml`,
`jinja2`, `rich` (Python 3.11+). SCA is enforced in CI via OSV-Scanner.

## Building from source

```sh
git clone https://github.com/narko4u/witnessos-compliance.git
cd witnessos-compliance
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Verifying releases

Release assets (wheel, source distribution, `sbom.cdx.json`, `SHA256SUMS`)
are published on the GitHub release page. To verify integrity and authorship:

1. Download `SHA256SUMS` and the assets for the release tag.
2. Verify checksums: `sha256sum -c SHA256SUMS`
3. Verify the Sigstore signature on an asset (keyless, OIDC-bound to this
   repository's `release.yml` workflow):

   ```
   cosign verify-blob --certificate <asset>.pem --signature <asset>.sig --certificate-identity-regexp "^https://github.com/narko4u/witnessos-compliance/.github/workflows/release.yml@refs/tags/v.*" --certificate-oidc-issuer "https://token.actions.githubusercontent.com" <asset>
   ```
