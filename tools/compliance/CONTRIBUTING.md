# Contributing to WitnessOS Compliance

Thanks for your interest in contributing! This repo ships compliance tooling for autonomous AI agents, covering the **Agent Capability Interface (ACI)**, the **Agent Interaction Protocol (AIP)**, the CLI, and regulatory mappings (NSA MCP, EU AI Act, CSA).

## Repository layout

```
aci/py/                 # ACI Python package — manifest schema + validation
aip/go/                 # AIP Go implementation — protocol types + receipts
cli/                    # witnessos-compliance CLI (Python, Click)
templates/eu-ai-act/    # EU AI Act evidence templates (E0–E4)
mappings/               # Standards-to-feature mapping documents
tools/                  # Standalone utilities (compliance-scanner.py)
```

## Setting up locally

**Python** (ACI, CLI, tools):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e aci/py/
pip install -e cli/           # if working on the CLI
```

**Go** (AIP):

```bash
cd aip/go && go mod tidy && go build ./...
```

## Coding standards

- **Python**: Use type hints throughout (`from __future__ import annotations` preferred). Follow [PEP 8](https://peps.python.org/pep-0008/). Use `snake_case` for functions/variables, `PascalCase` for classes. Document public APIs with Google-style docstrings (Args / Returns / Raises).
- **Go**: Follow [effective Go](https://go.dev/doc/effective_go) conventions. Use `CamelCase` for exported identifiers. Add doc comments on every exported type and function. Run `gofmt` before committing.
- **CLI**: Use `click` for commands and `rich` for output formatting. Keep report generators in separate modules under `cli/`.

## Testing requirements

- **Python**: Add or update tests in a `tests/` directory adjacent to the module. Run with `pytest` — aim for 80%+ coverage on new code.
- **Go**: Tests live in `*_test.go` files alongside the package. Run with `go test ./...`.
- Integration and end-to-end tests are welcome in `tools/` or as standalone scripts.

## Pull request guidelines

1. **Link a related issue** — every PR should reference a GitHub issue that describes the problem or feature.
2. **Describe your changes** in the PR body — what changed, why, and any trade-offs considered.
3. **Add tests** — new features and bug fixes must include tests that cover the change.
4. **Keep PRs focused** — one logical change per PR. Refactoring, docs, and feature work should be separate PRs.
5. **Run the linter and tests** locally before pushing.

## Code of conduct

All contributors are expected to uphold the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) code of conduct. Report unacceptable behaviour to the project maintainers.

## Questions?

Open a [discussion](https://github.com/narko4u/witnessos-compliance/discussions) or a feature request via the issue templates.

## Developer Certificate of Origin

Every commit must carry a `Signed-off-by` trailer (use `git commit -s`). The
CI `dco` job enforces this on every pull request.
