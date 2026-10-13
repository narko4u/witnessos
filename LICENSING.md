# Licensing

This page states what is free, what carries a commercial licence and how the two
fit together. It is short on purpose. Where a number or a scope is needed, the
canonical pricing page is [witnessos.com.au/pricing](https://witnessos.com.au/pricing)
and that page is the source of truth for commercial terms.

## Free and staying free

- **Local verification.** Anyone can verify a receipt offline with the published
  [verifier](https://github.com/narko4u/witnessos-verifier). No account, no
  server, no licence key and no network call. Verification is never paywalled,
  because a claim that only its vendor can check is not evidence.
- **The receipt format.** [SPEC.md](SPEC.md) is published under Apache 2.0 and
  frozen, so anyone may implement it, extend it or write another verifier.
  [EVIDENCE-GRADES.md](EVIDENCE-GRADES.md) is the normative statement of the
  ladder and is free to cite.
- **The other open tools.** The verifier, the MCP validator and the passport are
  free and open source. Each can be run against your own artifacts today.
- **This repository.** Documentation, the grade definitions and the product
  surface are Apache 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

## What carries a commercial licence

The WitnessOS issuance engine is not part of this distribution. A deployment that
uses it is licensed. So is the work that carries our time and our judgement.
The categories published on the pricing page are:

- a governed deployment of the engine, run for a named entity
- retention custody, where records are held so that a third party can still
  verify them later
- audits that compare what agents declare against what they do, with the
  evidence behind every grade
- evidence packs prepared for an auditor, a regulator or a counterparty
- named support with response windows

Each is priced on the pricing page. A quote states its own scope. We do not
bill open-ended time. A licence does not transfer ownership of your data: audit
trails, policies and agent configurations remain yours.

## Why the split is where it is

The format is free because a format that only one vendor implements cannot be
checked by anyone. The engine is licensed because it is the part that does the
work and because running it carries obligations that have to be supported.
Anyone can verify a record produced by a licensed deployment without holding a
licence. That is deliberate.

## Asking

For anything in the second list, contact Empire Labs Pty Ltd at
contact@empirelabs.com.au. For a defect in the format or in the verifier, open an
issue instead. That is free and it improves the thing everyone depends on.

---

Part of the [WitnessOS](https://github.com/narko4u/witnessos) family,
[Empire Labs Pty Ltd](https://www.empirelabs.com.au)
