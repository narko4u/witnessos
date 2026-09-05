# Contributing to WitnessOS

Thank you for your interest in contributing.

## Current Status

WitnessOS is in **Design Partner Alpha** (Phase F). At this stage, contributions are limited to:

- Documentation improvements
- Receipt specification feedback
- Verifier test cases and test vectors
- Bug reports and security disclosures

## What We Cannot Accept

- **Gateway implementation contributions** - the credential broker, policy engine, and enforcement layer are proprietary during Alpha. We cannot accept external pull requests modifying gateway source code at this time.
- **Customer evidence bundles** - do not submit real receipt data, customer logs, or evidence containing PII in any form.

## How to Contribute

1. **Documentation:** Open an issue describing the proposed change, then submit a PR against `main`.
2. **Spec feedback:** Open a discussion or issue referencing the relevant section of SPEC.md.
3. **Bug reports:** Open an issue with reproduction steps. Do not include credentials, secrets, or customer data.
4. **Security issues:** See [SECURITY.md](SECURITY.md). Do not open public issues for security vulnerabilities.

## Development

```bash
git clone https://github.com/narko4u/witnessos.git
cd witnessos
uv sync
uv run pytest
```

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

## Developer Certificate of Origin

Every commit must carry a `Signed-off-by` trailer (use `git commit -s`). The
CI `dco` job enforces this on every pull request.
