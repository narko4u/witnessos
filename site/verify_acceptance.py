import re, sys
html = open('/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/dist/index.html', encoding='utf-8').read()
checks = {
  'em dash (U+2014)': html.count('\u2014'),
  'E5 mentioned': len(re.findall(r'\bE5\b', html)),
  'engine internals (gateway/repo path)': len(re.findall(r'witnessos-gateway|/opt/witnessos|narko4u', html, re.I)),
  'Eddie / Edward Wade': len(re.findall(r'Eddie|Edward Wade', html)),
  'fabricated cert claims (certified/ISO/SOC2)': len(re.findall(r'\bcertified\b|\bcompliant with\b|\bISO 27001\b|\bSOC 2\b', html)),
  'literal-OS overclaim': len(re.findall(r'is an operating system for machines', html)),
  'OS metaphor present (kernel line)': len(re.findall(r'operating layer for governed agent action', html)),
  'external trackers': len(re.findall(r'gtag|google-analytics|googletagmanager|plausible|fathom|segment', html)),
  'cookie/consent words': len(re.findall(r'cookie|consent', html, re.I)),
  'mailto contact@ count': len(re.findall(r'mailto:contact@empirelabs\.com\.au', html)),
  'aci link target': re.findall(r'href="(https://[^"]*aci/[^"]*)"', html),
  'E4 count': html.count('E4'),
  'E0-E3 present': all(x in html for x in ('E0','E1','E2','E3')),
  'RFC 3161 count': html.count('RFC 3161'),
  'fail-closed wording': len(re.findall(r'fail.?closed', html, re.I)),
  'h1 count': len(re.findall(r'<h1', html)),
  'section balance': html.count('<section') - html.count('</section>'),
  'external http links': re.findall(r'href="(https?://[^"]+)"', html),
}
for k, v in checks.items():
    print(f"{k}: {v}")
