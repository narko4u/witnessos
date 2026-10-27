# Navy Theme Rebuild Spec — witnessos.com.au (2026-09-07, theme reversion, FINAL)

Eddie's directives (09-07, in order):
1. The ORIGINAL navy theme (as live before 2026-09-07) is canonical. The purple re-skin
   is REJECTED. Every page uses the navy design system below. No invented styles.
2. FINAL STRUCTURE: the navy landing page (index.html) STAYS the first page — it is the
   summary of the full site. The ~11 pages are COMPRESSED TO MAIN POINTS ONLY and built
   in the SAME EXACT navy theme/layout. The landing page hyperlinks to the page set
   (Explore section + footer). Content-honesty work from the purple phase carries over.
3. Website must be a masterpiece: consistent titles ("WitnessOS | X"), consistent nav,
   sitewide footer with Pages/Legal/Contact columns, zero dead links, zero leaks.
4. NOTHING goes live without Eddie's eyes on a local preview + explicit go.

## Read these files first
1. THEME SOURCE (authoritative): `/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/replica-dist/index.html`
   — this IS the original theme. Your page must look like a natural sibling of it.
2. CONTENT SOURCE (your page's current content — text is already approved):
   `/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v1/<YOURPAGE>.html`
3. EXTRA CLASSES: `/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/navy-extras.css`
4. ASSETS dir: `/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v2/assets/` (webp images)

## Page shell (mirror replica-dist exactly)
- Doctype + head: charset, viewport, description, theme-color #07101d, title pattern
  "WitnessOS | <short>", canonical https://witnessos.com.au/<file>, og:type website,
  og:site_name WitnessOS, og:title, og:description, og:url, og:image
  https://narko4u.github.io/witnessos/witnessos-logo.png (width 1200 height 400),
  twitter:card summary_large_image + twitter mirrors, NO google-fonts link (theme is
  system-font Inter/ui-sans-serif), NO purple/light themes.
- THE <style> MUST START WITH THE ENTIRE CORE THEME CSS FROM replica-dist/index.html
  lines 26-129 VERBATIM (the block between `<style>` and `</style>`). Then append only
  the EXTRA CLASSES you need from navy-extras.css (copy the rule text verbatim).
- body structure: `<div class="wrap">` > `<header class="nav">` containing a centered
  `<nav aria-label="Main navigation">` with text links (color:var(--muted), 14px, gap 24px)
  + `<a class="button">` mailto contact (WitnessOS%20Assessment) at the end, plus
  `<a class="button mobile">Contact</a>` outside the inner nav (see replica). Then
  `<main id="top">` with `<a class="logo-stage" href="index.html">` + `<img
  src="assets/witnessos-logo.webp" width="1800" height="600" alt="WitnessOS">`, then the
  page content sections, then `<footer>` mirroring replica-dist (empire-banner.webp image
  + "Empire Labs Pty Ltd" block + www.empirelabs.com.au / contact@empirelabs.com.au /
  github.com/narko4u/witnessos links). Close .wrap/body/html.
- Nav links on content pages: Home (index.html), Why now (index.html#problem),
  How it works (index.html#how), Evidence (index.html#evidence), Capabilities
  (index.html#capabilities), plus the page's own label (plain text, no link, or link to
  itself) placed in the same order as the anchor links, then the button. Keep it short:
  max ~7 items.

## Layout/content rules (translate, don't copy purple structure)
- Convert the purple page's content into navy section patterns from the ORIGINAL theme:
  section borders: `section{padding:86px 0;border-top:1px solid var(--line)}` — the CSS is
  already in core. Each content page should read like a set of sections: `.eyebrow` label
  + `<h2>` heading (clamp sizes in core) + body copy.
- Prose-heavy pages (whitepaper, roadmap, manifesto, terms, privacy, casestudy): wrap text
  in `<div class="prose">` sections with eyebrow/h2 per part; long docs may use many
  sections. Use `.toc` at top for docs with 6+ parts.
- Card content → `.card` (panel card). Grids of 2 → `.grid2`, 3 → `.grid3`, capability
  tiles → `.cap-grid`/`.cap` with `<code>` eyebrow labels. Step sequences → `.steps`/
  `.step`/`.num`. FAQ → `.faq`/`.faq-item`. CTA end piece → `<section class="cta">` with
  `.actions` and `.button`/`.button.secondary`. Inline spec/link chips → `.connector-chip`
  inside `.connector-row`.
- Headings use plain `<h1>`/`<h2>`/`<h3>` (no display-large/section-heading/sub-heading
  classes). Body copy = plain `<p>` (muted via .copy/.value context or inside .prose). Keep
  an `<h1>` with the page title at top of content (after logo-stage), styled by core h1.
- Tables: use the .prose table styling if a table is genuinely needed.
- KEEP ALL APPROVED CONTENT/COPY from publish-v1 source. Do NOT rewrite claims, do NOT
  soften, do NOT invent. Preserve every factual statement (E4 anchored receipts, RFC 3161,
  FreeTSA/independent TSA wording, "live September 2026" status lines, request-access
  framing, honest deployment language, interactive simulation labels, E4 Shipped roadmap
  item). Only re-skin markup + adjust structure to the navy patterns.

## Hard rules (never violate)
- No `#6e62ff`, no `Source Sans`, no GitHub-dark hex palette (#0d1117/#161b22/#30363d/#8b949e)
  anywhere in the output. Theme tokens ONLY from core CSS.
- No `api.witnessos.dev` anywhere. No `narko4u.github.io/witnessos-compliance` link.
- No "Sovereign, Co-founder" — only "Empire Labs Pty Ltd" as the organisation.
- No `demo@witnessos.com` email; no fabricated people/emails.
- No ™ / ® glyphs. No em dashes (—). No `@` in visible copy.
- No dead internal links: every href to another page in the set must target a real file.
  Homepage file is `index.html`; page set: index, whitepaper, quickstart, demo, casestudy,
  manifesto, roadmap, pricing, terms, privacy, signup.
- Money-domain framing (approved): access not "pricing tiers"; early access by arrangement;
  simulation is an in-browser demo, never a claim of a live backend; engine proprietary,
  design-partner/NDA deployments only; terms/privacy pages reference witnessos.com.au.
- Keep `mailto:contact@empirelabs.com.au` CTAs (subject=WitnessOS%20Assessment for the
  main CTA). Do not invent other addresses.
- Preserve any working <script> behaviour (request-access form, simulation runner) but
  restyle its DOM with navy classes and make sure JS references match the new classes/ids.

## Output
- Write the completed file to `/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v2/<YOURPAGE>.html`
- Then run a quick self-check: `grep -c "6e62ff\|Source Sans\|api.witnessos.dev\|Sovereign, Co-founder\|demo@witnessos" <output>` → must print 0; and
  `python3 - <<'EOF'
  import re
  s=open('<output>').read()
  for t in re.findall(r'<[^>]+>', s):
      pass
  print('tag balance ok:', s.count('<section')==s.count('</section>') and s.count('<div')==s.count('</div>'))
  EOF`
- Report: output path + self-check results + any content you had to paraphrase (should be none).
