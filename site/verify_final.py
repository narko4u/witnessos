import re
html = open('/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/dist/index.html', encoding='utf-8').read()

# anchor targets vs href="#..." ids
ids = re.findall(r'id="([^"]+)"', html)
hrefs = re.findall(r'href="#([^"]+)"', html)
missing = [h for h in hrefs if h not in ids]
print('anchor targets missing:', missing if missing else 'none')

# structure
print('doctype:', html.lstrip().lower().startswith('<!doctype html>'))
print('single h1:', len(re.findall(r'<h1', html)) == 1)
print('lang:', 'lang="en"' in html)
print('viewport:', 'name="viewport"' in html)
print('meta description:', 'name="description"' in html)

# final link state
print('aci link now:', 'empirelabs.com.au/aci/' in html)
print('no WitnessOS.com.au/aci self-404:', 'WitnessOS.com.au/aci/' not in html)
print('contact mailto present:', 'contact@empirelabs.com.au' in html)
print('no external fonts/CDN:', all(x not in html for x in ['fonts.googleapis','cdn.jsdelivr','unpkg.com']))
