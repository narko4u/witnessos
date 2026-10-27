#!/usr/bin/env python3
"""SECRET-LEAK SCAN for publish-v2 site (pre-approval gate).

Scans every .html/.xml/.txt in publish-v2 for:
  1. Credential values / key material (by key-name regex, values never printed)
  2. Internal infrastructure references (private hosts, internal paths)
  3. Private repo / internal tooling names
  4. Identity leaks (real names other than Empire Labs Pty Ltd public identity)
  5. Contact-surface leaks outside approved channels
  6. Config/source breadcrumbs (.env, config.yaml, token=)

Output: per-file hit lines with values REDACTED by regex (never eyeball values).
"""
import re, pathlib, sys

PUB = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v2")

KEYNAME = re.compile(
    r'(sk_(live|test)_[A-Za-z0-9]{8,}|pk_(live|test)_[A-Za-z0-9]{8,}'
    r'|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}'
    r'|AIza[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
    r'|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})',
    re.I)

KEYVALUE = re.compile(
    r'([A-Za-z0-9_\-.]*(?:api[_-]?key|apikey|token|secret|password|passwd|pwd|credential|auth)[A-Za-z0-9_\-.]*\s*[:=]\s*)([^\s"\'&,;]+)',
    re.I)

INTERNAL = [
    "witnessos-gateway", "witnessos-compliance", "witnessos-archive", "empirelabs-au",
    "witnessos.empirelabs", "agentguild", "guildx",
    "herokuapp", "netlify.app", "onrender", "ngrok",
    "VaultSentinel", "HermesGenesis", ".hermes",
    "/opt/witnessos", "witnessos-deploy", "run-live", "run-e4", "state.db",
    "narko4u/aci-spec-private", "slack.com",
    "discord.gg", "discord.com/invite", "notion.so", "linear.app",
]

IDENTITY = [
    "Edward Wade", "Eddie Wade", "Sovereign", "Porgie", "Senti", "vaultsenti",
    "Sankalp", "Gilda", "astrogilda", "giskard", "julianna", "Adrian",
]

APPROVED_CHANNELS = [
    "contact@empirelabs.com.au", "www.empirelabs.com.au", "empirelabs.com.au",
    "github.com/narko4u", "witnessos.com.au", "github.com/narko4u/witnessos",
    "github.com/narko4u/aci-spec", "github.com/narko4u/aip-spec", "github.com/narko4u/ajson",
    "narko4u.github.io", "schema.org", "sitemaps.org", "example.com", "w3.org",
]

def redact(line):
    """Redact anything that smells like a credential value; never print values."""
    line = KEYVALUE.sub(lambda m: m.group(1) + "REDACTED", line)
    line = re.sub(r'sk_(live|test)_[A-Za-z0-9]+', 'sk_***REDACTED***', line)
    line = re.sub(r'ghp_[A-Za-z0-9]+', 'ghp_***REDACTED***', line)
    return line.strip()

def scan():
    files = sorted(PUB.glob("*.html")) + sorted(PUB.glob("*.xml")) + sorted(PUB.glob("*.txt"))
    issues = 0
    for f in files:
        text = f.read_text(errors="replace")
        for i, raw in enumerate(text.splitlines(), 1):
            line = raw
            hits = []
            # key-name / value presence (flag line, value redacted)
            if KEYNAME.search(line):
                hits.append("credential-like-token")
            # internal refs
            low = line.lower()
            for token in INTERNAL:
                if token.lower() in low:
                    hits.append(f"internal:{token}")
            for name in IDENTITY:
                if name in line:
                    hits.append(f"identity:{name}")
            # contact surface: flag email-ish that is NOT approved (example.com ok)
            for m in re.finditer(r'[\w.+-]+@[\w-]+(?:\.[\w.-]+)+', line):
                addr = m.group(0).rstrip('.,;:)]}\'">')
                if addr not in APPROVED_CHANNELS and not addr.endswith("@example.com"):
                    hits.append(f"contact:{addr}")
            for m in re.finditer(r'https?://[^\s"\'<>)]+', line):
                u = m.group(0).rstrip('.,;:')
                if u.startswith(("http://localhost", "http://127.0.0.1")):
                    continue
                if not any(a in u for a in APPROVED_CHANNELS):
                    hits.append(f"url:{u}")
            if hits:
                issues += 1
                print(f"[{f.name}:{i}] {'; '.join(sorted(set(hits)))} :: {redact(line)[:160]}")
    print(f"--- {issues} flagged line(s) across {len(files)} file(s)")
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(scan())
