# Contributing to the Agent Asset Registry

Thank you for your interest in contributing to the Agent Asset Registry! This is a community-driven project, and every contribution helps build a more transparent and accountable AI agent ecosystem.

## Ways to Contribute

- **Add a new agent type** — Document an agent type not yet represented in the registry
- **Update an existing entry** — Correct or expand information about a registered agent type
- **Improve tooling** — Enhance the validation, search, or reporting tools
- **Fix bugs** — Address issues in the schema, tools, or documentation
- **Improve documentation** — Clarify guidelines, add examples, or fix typos

## Adding a New Agent Type

### Step 1: Choose the Right Category

Agent types are organized into category subdirectories under `registry/agent_types/`:

| Category | Description | Example |
|---|---|---|
| `general-purpose/` | Agents with broad, non-specialized capabilities | LLM chat agents, coding assistants |
| `workflow/` | Agents focused on automating business workflows | Email automation, scheduling |
| `industry/` | Agents serving specific industry verticals | Fintech trading, legal document processing |

If your agent type doesn't fit an existing category, propose a new one in your pull request.

### Step 2: Create the YAML File

Create a file named with the agent's identifier (e.g., `my-agent-type.yaml`) in the appropriate category directory. Follow the schema defined in `schema/agent-type-schema.json`.

Required fields:

```yaml
id: my-agent-type            # Unique, kebab-case identifier
name: My Agent Type           # Human-readable name
description: >               # 2-5 sentence description
  What this agent does, how it works, and its typical use cases.
category: general-purpose     # Must match the directory name
vendor: vendor-name           # Must match a vendor file in registry/vendors/
capabilities:
  - capability one
  - capability two
risk_profile: medium          # One of: low, medium, high, critical
```

Optional fields are documented in the [JSON Schema](schema/agent-type-schema.json).

### Step 3: Run Validation

Before submitting, validate your entry:

```bash
pip install pyyaml
python tools/validate-registry.py
```

All entries must pass validation. The validator checks:
- Structural compliance with the JSON schema
- Valid field types and enum values
- Cross-references to vendor files

### Step 4: Submit a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b add-agent-type-<your-agent-id>`
3. Commit your changes: `git commit -m "Add agent type: <Your Agent Name>"`
4. Push: `git push origin add-agent-type-<your-agent-id>`
5. Open a pull request against the `main` branch

### Pull Request Guidelines

- **One agent type per pull request** — keeps review focused
- **Include a meaningful description** — explain what the agent does and why it belongs in the registry
- **Ensure validation passes** — include the output of `validate-registry.py` in your PR description
- **Provide sources** — link to documentation, vendor pages, or research papers as references

## Review Process

1. **Automated checks** — GitHub Actions runs schema validation and YAML linting
2. **Community review** — Maintainers and community members review the submission for accuracy, completeness, and structural correctness
3. **Merge** — Once approved, a maintainer merges your contribution

We aim to review pull requests within 5 business days.

## Community Guidelines

- **Be respectful** — This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md) code of conduct
- **Be accurate** — Only submit agent types you have researched; speculative entries will be rejected
- **Be specific** — Prefer concrete behavioral patterns and detection signatures over vague descriptions
- **No proprietary code** — Do not include proprietary code, trade secrets, or confidential information
- **No promotional content** — Entries should be factual and informative, not promotional

## Code Style

### YAML

- Use 2-space indentation
- Use `>` for multi-line descriptions where appropriate
- Use kebab-case for IDs
- Include descriptive comments for non-obvious fields
- Run `yamllint` if available

### Python (tools/)

- Target Python 3.12+
- Use type hints for all function signatures
- Follow PEP 8 style
- Include docstrings for all public functions
- Use `argparse` for CLI interfaces

## Adding or Updating Vendors

Vendor files live in `registry/vendors/`. Each file describes a platform, framework, or organization that produces agents. To add a vendor:

1. Create a file `registry/vendors/<vendor-id>.yaml`
2. Follow the vendor schema implied by the existing vendor files
3. Run validation

## Reporting Issues

If you find an error in an existing entry or have a suggestion for improvement, open a [GitHub Issue](https://github.com/narko4u/witnessos-agent-asset-registry/issues).

## Questions?

Start a discussion in [GitHub Discussions](https://github.com/narko4u/witnessos-agent-asset-registry/discussions) or reach out to the maintainers.

---

*Thank you for helping make AI agents more transparent and accountable.*

## Developer Certificate of Origin

Every commit must carry a `Signed-off-by` trailer (use `git commit -s`). The
CI `dco` job enforces this on every pull request.

## Running tests

See TESTING.md for the test policy and the exact commands CI runs. Always run
the suite locally before opening a pull request.
