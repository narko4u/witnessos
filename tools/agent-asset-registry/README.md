# Agent Asset Registry

[![OpenSSF Best Practices - Baseline 1](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14142.json&query=badge_percentage_baseline_1&label=OpenSSF%20Baseline%201&suffix=%25&color=success)](https://www.bestpractices.dev/projects/14142) [![OpenSSF Best Practices - Baseline 2](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14142.json&query=badge_percentage_baseline_2&label=OpenSSF%20Baseline%202&suffix=%25&color=success)](https://www.bestpractices.dev/projects/14142) [![OpenSSF Best Practices - Baseline 3](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14142.json&query=badge_percentage_baseline_3&label=OpenSSF%20Baseline%203&suffix=%25&color=success)](https://www.bestpractices.dev/projects/14142)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/narko4u/witnessos-agent-asset-registry)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Contributors Welcome](https://img.shields.io/badge/contributors-welcome-orange.svg)](CONTRIBUTING.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Registry Entries](https://img.shields.io/badge/registry-8%20agents-blueviolet)](registry/agent_types/)

## Overview

**The Agent Asset Registry is the first community-driven catalog of known AI agent types.** As autonomous AI agents proliferate across every industry — from customer support and code generation to financial trading and legal document processing — there is no central, standardized repository for tracking who builds them, what they do, and how they behave.

This registry fills that gap.

We collect, categorize, and document AI agent types in a structured, machine-readable format. Each entry describes an agent's capabilities, risk profile, known behavioral patterns, and detection signatures. The result is a shared knowledge base that enables security researchers, governance platforms, compliance officers, and developers to understand the agent landscape.

### Why This Matters

AI agents are no longer experimental. They are deployed in production systems processing financial transactions, drafting legal contracts, managing email workflows, and writing production code. Yet there is no equivalent of a CVE database or software bill of materials for AI agents. When a new agent type appears, there is no standard way to answer:

- **What is this agent capable of?**
- **What risk level does it carry?**
- **Has it been observed exhibiting unexpected behaviors?**
- **What signatures can detect it in a runtime environment?**

The Agent Asset Registry exists to answer these questions — and to provide a foundation for governance tools like [WitnessOS](https://witnessos.nousresearch.com), a governance runtime for AI agents, to build upon.

### Who Is This For?

- **Security researchers** cataloging agent behaviors and attack surfaces
- **Platform operators** deploying governance controls around agents
- **Compliance teams** assessing third-party agent integrations
- **Developers** building agents who want to understand the ecosystem
- **Policy makers** studying the landscape of autonomous systems

## Repository Structure

```
agent-asset-registry/
├── LICENSE                          # Apache 2.0
├── README.md                        # This file
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md               # Community standards
├── SECURITY.md                      # Security disclosure process
├── schema/
│   └── agent-type-schema.json       # JSON Schema for agent entries
├── registry/
│   ├── agent_types/                 # Individual agent type definitions
│   │   ├── general-purpose/         # General-purpose agent types
│   │   ├── workflow/               # Workflow automation agents
│   │   └── industry/               # Industry-specific agents
│   └── vendors/                     # Vendor/platform definitions
└── tools/
    ├── validate-registry.py         # Schema validation tool
    ├── search-registry.py           # Search and filter CLI
    └── generate-report.py           # Human-readable report generator
```

## Getting Started

### Prerequisites

- Python 3.12+
- PyYAML (`pip install pyyaml`)

### Validate the Registry

```bash
python tools/validate-registry.py
```

This checks all agent type and vendor YAML files against the JSON schema and reports any structural issues.

### Search Agents

```bash
# Search by keyword
python tools/search-registry.py --keyword "trading"

# Filter by category
python tools/search-registry.py --category "general-purpose"

# Filter by risk level
python tools/search-registry.py --risk-level "high"

# Combine filters
python tools/search-registry.py --category "workflow" --risk-level "medium"
```

### Generate a Report

```bash
python tools/generate-report.py
```

Produces a formatted summary of all registered agents, organized by category, with risk distributions and capability overviews.

## How to Contribute

We welcome contributions from the community. To add a new agent type:

1. **Fork** this repository
2. Create a **YAML file** in the appropriate category under `registry/agent_types/`
3. Follow the **schema** defined in `schema/agent-type-schema.json`
4. Run **validation** with `tools/validate-registry.py`
5. Submit a **pull request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## The Agent Governance Problem

The proliferation of AI agents creates a fundamental accountability gap. Unlike traditional software components, agents can:

- **Act autonomously** within their delegated authority
- **Execute multi-step plans** across systems
- **Interact with other agents** in ways that are hard to audit
- **Evolve behaviors** through learning and prompt injection
- **Operate opaquely** behind API boundaries

The Agent Asset Registry is one piece of the solution — providing transparency into what agents exist and what they do. Combined with governance runtimes like [WitnessOS](https://witnessos.nousresearch.com), organizations can move from blind trust to verifiable control over their agent ecosystems.

## License

This project is licensed under the **Apache 2.0 License** — see the [LICENSE](LICENSE) file for details.

## Community

- **Issues**: Report problems or suggest features via [GitHub Issues](https://github.com/narko4u/witnessos-agent-asset-registry/issues)
- **Discussions**: Start a conversation in [GitHub Discussions](https://github.com/narko4u/witnessos-agent-asset-registry/discussions)
- **Contributions**: See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved

---

*Built for a future where agents are transparent, accountable, and governable.*


---

<sub>Part of the [WitnessOS launch family](https://github.com/narko4u/witnessos): [witnessos-alpha](https://github.com/narko4u/witnessos-alpha) · [witnessos-compliance](https://github.com/narko4u/witnessos-compliance) · [eu-ai-act-compliance-grade](https://github.com/narko4u/eu-ai-act-compliance-grade) · [witnessos-rogue-agent-audit](https://github.com/narko4u/witnessos-rogue-agent-audit) · [witnessos-agent-asset-registry](https://github.com/narko4u/witnessos-agent-asset-registry) · [witnessos-verifier](https://github.com/narko4u/witnessos-verifier) · [agent-interaction-specs](https://github.com/narko4u/agent-interaction-specs) · [aci-spec](https://github.com/narko4u/aci-spec) · [aip-spec](https://github.com/narko4u/aip-spec) · [ajson](https://github.com/narko4u/ajson) — [Empire Labs Pty Ltd](https://www.empirelabs.com.au)</sub>
## Dependencies

Runtime dependencies are declared in `pyproject.toml` (Python 3.12). The
dependency set is kept minimal to reduce the attack surface. SCA is enforced
in CI via OSV-Scanner.

## Building from source

```sh
git clone https://github.com/narko4u/witnessos-agent-asset-registry.git
cd witnessos-agent-asset-registry
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
   cosign verify-blob --certificate <asset>.pem --signature <asset>.sig --certificate-identity-regexp "^https://github.com/narko4u/witnessos-agent-asset-registry/.github/workflows/release.yml@refs/tags/v.*" --certificate-oidc-issuer "https://token.actions.githubusercontent.com" <asset>
   ```
