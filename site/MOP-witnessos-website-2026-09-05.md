# MOP — WitnessOS Public Website (2026-09-05)

**Builder:** Senti (ChatGPT Sites / Codex) — builds the site cold from this
document. **Scope owner:** Empire Labs Pty Ltd (Eddie + Sovereign review the
output; nothing goes live until Eddie approves). **Launch:** domain chosen by
Eddie; deploy to **Netlify** (Empire-owned account, we control the site and
launch it there).

**EDIT BEFORE PASTING:** domain and contact email are already filled
(WitnessOS.com.au / contact@empirelabs.com.au).

**IMPORTANT — Senti already built a trial WitnessOS website.** Keep the SAME
style and visual theme from that trial (look, feel, layout patterns, colour,
typography, overall vibe). Do NOT redesign from scratch. Apply the copy,
structure, sections, content intent, and rules in this document ON TOP of that
existing trial theme. If any instruction here conflicts with the trial site's
style, follow the instruction but preserve the theme wherever possible.

---

## 1. Non-negotiables (violating any of these = reject the build)

1. **No false claims.** Site copy must not claim certifications, customers,
   metrics, or capabilities we have not delivered. Where a claim is
   directional, say "designed for" / "built for", never "certified" /
   "compliant with".
2. **WitnessOS is NOT an operating system.** It is a runtime governance layer
   for autonomous agents. Use the operating-system metaphor only as a clear
   analogy: "the operating layer for governed agent action". Never describe
   it as managing hardware, processes, or memory.
3. **No E5, no engine internals, no repo paths.** Public copy refers to the
   product and the open standards vocabulary (ACI / AIP / AJSON). Never
   mention "gateway repo", file paths, or internal architecture names beyond
   what appears in this document.
4. **No fabricated identities.** No invented customers, logos, quotes, or
   testimonials. No "Eddie" anywhere. Legal entity is always "Empire Labs Pty
   Ltd" in full on first mention and in the footer.
5. **Static artifact only.** Plain HTML/CSS/JS (no Next.js/React build
   requirement unless explicitly agreed). No external analytics, no
   third-party trackers, no cookies that require consent banners. Zero
   external font/CDN dependency beyond a graceful system-font fallback.
6. **All links are relative or use the WitnessOS.com.au constant** — the site must
   work from a local file preview AND from the final domain without editing.
7. **No em dashes in any copy.** Use commas, colons, or full stops instead.

## 2. Measured product context (verified 2026-09-05)

WitnessOS is a drop-in governance layer for autonomous AI agents and systems.
Existing public page (empirelabs.com.au/witnessos.html) describes:

- Deterministic policy evaluation before any action runs: Allow, Deny,
  Conditional, Escalate (OPA/Rego policy-as-code compatible).
- Evidence receipts: SHA-256 signed, tamper-evident, exportable audit bundles.
- RemediLevel R0-R6 escalation framework (advisory to hard failsafe).
- Machine binding for licensing (TPM / fingerprint), API-first design,
  multi-layer policy tiers (system, environment, action-level).

New capability to surface (the E4 verifiable-evidence layer, live in
production 2026-09-05 under strict mode):

- Evidence ladder E0-E4. Public framing: E0-E2 events recorded/chained/signed;
  E3 chain intact and self-consistent; E4 independently timestamped by a
  standards-based RFC 3161 Time Stamping Authority at the moment of record,
  with revocation checked at that time. The ladder closes at E4.
- A governed-actions allowlist means only sanctioned action types reach E4;
  everything else fails closed at E3. Tamper-tested: altered records cannot
  reach E4. Watchdog coverage: if the evidence gate degrades, operators are
  alerted; no silent drift.
- Receipts verify with zero trust in Empire Labs (no DB access needed).

Open standards positioning: built on the Empire Stack vocabulary — ACI (Agent
Communication Interface with AJSON manifest authoring) and AIP (Agent
Interaction Protocol). Reference: empirelabs.com.au/aci/.

## 3. Audience and job (single page serves both)

1. **Enterprise buyer** (CTO, VP Eng, Head of AI/Risk/Compliance): "How do I
   prove what my agents actually did, to my auditor?" -> assessment/demo CTA.
2. **Investor/partner**: "This is the governance layer that makes agents
   deployable in regulated environments — evidence, not dashboards." -> proof
   of a real shipped product.

The two audiences share one core message; the page flows from problem to
product to proof to CTA without a fork in the road.

## 4. Page structure (single long-form page, ~7 sections)

### 4.1 Hero (above the fold)
- Eyebrow: WitnessOS by Empire Labs Pty Ltd
- H1 direction: "Every agent action, provable." (or a variant on: proof, not
  dashboards)
- Subhead direction (grounding the OS metaphor honestly): "WitnessOS isn't an
  operating system for machines. It's the operating layer for governed agent
  action — the kernel between 'the agent wants to' and 'the agent may'."
- One-line value: deterministic policy, human approval, tamper-evident
  receipts, independent timestamps. Auditor-verifiable with zero trust in us.
- Primary CTA: "Book a technical assessment" (mailto link to
  contact@empirelabs.com.au, subject WitnessOS Assessment).
- Secondary CTA: "See the evidence ladder" (anchors to section 4.4).

### 4.2 The problem (why now)
- Regulators are moving from AI governance guidance to AI governance
  evidence. Enterprises will soon have to answer audit, risk, and insurance:
  "Show me, don't tell me."
- Today's agent platforms answer with self-attested logs the vendor could
  edit. Dashboards are not audit trails.
- One sentence job: when an agent spends money, sends a message, or touches a
  governed action, who can prove what happened, who approved it, and when?

### 4.3 How it works (keep existing governance framing, add evidence)
Four steps, short and concrete:
1. Action proposed — an agent proposes an action with context: target,
   parameters, scope, asserted intent.
2. Policy evaluated — deterministic evaluation (OPA/Rego compatible), result:
   Allow, Deny, Conditional, Escalate.
3. Evidence receipt — every evaluation produces a tamper-evident receipt:
   action hash, policy version, context, decision, timestamp, chain of
   custody. SHA-256 signed, exportable as an audit bundle.
4. Governed execution + remediation if denied — structured response from
   advisory to failsafe; every escalation logged as evidence-grade receipts.

### 4.4 The evidence ladder (E0-E4, new layer)
Explain the ladder plainly. Emphasise:
- E4 means an independent third party (RFC 3161 Time Stamping Authority)
  sealed the moment the record was finalised, and revocation was checked at
  that time, not later.
- Fail-closed by default: unprovable gates cap the grade down, never up.
- Allowlist: only sanctioned action types can reach E4.
- Receipts verify without Empire trust — no database access required.
- Tamper-tested + watchdog: no silent drift.

### 4.5 Capability grid (from existing page, lightly updated)
Policy engine (OPA-native Rego) | Evidence receipts (tamper-evident, SHA-256,
exportable) | RemediLevel R0-R6 | Machine binding (TPM/fingerprint licensing)
| API-first (REST, WebSocket, SDKs) | Multi-layer policy tiers.

### 4.6 Proof and positioning (serves investor + enterprise)
Real, safe claims only:
- E4-grade evidence issuing in production under strict mode with a real
  third-party RFC 3161 anchor (fact, 2026-09-05).
- Tamper testing: altered records cannot reach the top grade.
- Governed-actions allowlist; everything else fails closed.
- Watchdog coverage; no silent drift.
- 400+ automated tests green, including real-CA timestamp verification.
- Built on open standards vocabularies (ACI/AIP/AJSON). Link to
  https://empirelabs.com.au/aci/ for the agent-discoverable manifests.
- Do NOT fabricate logos, customer quotes, funding figures, or headcounts.

### 4.7 CTA / contact
- Book a 30-minute technical assessment -> mailto contact@empirelabs.com.au, subject
  WitnessOS Assessment.
- Enterprise enquiry mailto with subject WitnessOS Enterprise Enquiry.
- Footer: Empire Labs Pty Ltd. www.empirelabs.com.au. No Eddie name anywhere.

## 5. Visual direction
- Dark, technical, trustworthy. Light copy on dark background; one accent
  colour. No stock-photo cliches of robots/hands/glowing brains.
- Evidence motif: receipts, hashes, chain links, a simple ladder graphic for
  E0-E4. Diagrams are flat SVG or CSS, inline, no heavy libraries.
- System font stack with optional self-hosted font; graceful fallback.
- Fully responsive, single HTML file (or 2-3 small files: index.html,
  style.css, script.js) with no build step. Keep it under ~400KB total
  excluding nothing (no heavy hero video by default).

## 6. Acceptance criteria (builder proves each before delivery)
1. Opens correctly from a local file (file://) and all links work relative.
2. No prohibited claims, no E5/engine internals/repo paths, no Eddie name, no
   fabricated customers or certifications, no em dashes.
3. The OS question is answered honestly in the hero subhead (metaphor only).
4. E0-E4 ladder present, closes at E4, fail-closed semantics described.
5. Both CTAs present and pointing to contact@empirelabs.com.au mailto links.
6. Valid HTML, no console errors, responsive at 360px / 768px / 1440px.
7. Lighthouse-approximable basics: semantic headings, one h1, alt text on
   meaningful images, reasonable contrast.
8. No external trackers, no cookie banners needed.

## 7. Deliverables
- `index.html`, `style.css`, `script.js` (or one self-contained index.html if
  cleaner), plus a short `README.md` for Empire stating how to preview and
  where to change the domain constant and CTA email.
- A plain-text copy pass (headlines, body copy) inline in the HTML, not as an
  image.
- Optional `netlify.toml` (build/publish settings: publish dir = the folder
  with index.html; no build command needed for a static site). Empire deploys
  to Netlify (their account) and attaches the chosen custom domain there.
  Do NOT assume any external API or server-side logic — the site is static by
  design.

## 8. Decisions log (starter)
- 2026-09-05: Audience = enterprise buyer + investor on one page.
- 2026-09-05: Story = keep existing policy/remediation framing, add E4 layer.
- 2026-09-05: Domain chosen = WitnessOS.com.au. Deploy + launch target =
  Netlify (Empire-owned account, we control the site).
- 2026-09-05: Senti has a trial WitnessOS website — new build keeps the same
  style/theme, applies this MOP's copy + structure on top of it.
- 2026-09-05: Static artifact, no build framework, no tracking.
- 2026-09-05: Public ladder closes at E4. E5 and engine internals are never
  mentioned in any public material.
