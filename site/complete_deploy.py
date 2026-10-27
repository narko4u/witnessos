#!/usr/bin/env python3
"""Complete deploy 6aac0defd0dab9983e619ef4.

`required` came back as DIGESTS (not paths) because the deploy was created with a
files map. Exactly one digest is required, and it equals the sha1 of the new
sitemap.xml -- i.e. the single file we actually changed. Nothing else is needed,
which is the whole point of the digest-preserving approach.

Uploads that one file by path and waits for the deploy to go ready.
"""
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

SITE = "4bdc4cd1-fa6b-4283-9eb8-937081514401"
DEPLOY = "6aac0defd0dab9983e619ef4"
STAGE = pathlib.Path("/home/vault/witnessos-site-work/publish-v2")
MANIFEST = pathlib.Path("/tmp/sitefiles.json")
API = "https://api.netlify.com/api/v1"
TOK = os.environ["NETLIFY_AUTH_TOKEN"]
HDRS = {"Authorization": f"Bearer {TOK}", "User-Agent": "sovereign-deploy/1.0"}


def call(method, path, body=None, ctype="application/json"):
    data = None
    if body is not None:
        data = json.dumps(body).encode() if ctype == "application/json" else body
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Content-Type", ctype)
    for k, v in HDRS.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            raw = r.read()
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} on {method} {path}: {e.read()[:600].decode(errors='replace')}")
        raise


new_bytes = (STAGE / "sitemap.xml").read_bytes()
new_sha = hashlib.sha1(new_bytes).hexdigest()
old = {f["path"]: f["sha"] for f in json.loads(MANIFEST.read_text())}

d = call("GET", f"/deploys/{DEPLOY}")
required = d.get("required") or []
print(f"deploy {DEPLOY}\n  state    = {d.get('state')}\n  required = {required}")

# Every required digest must map to a path we deliberately changed.
changed = {p: s for p, s in {**old, "/sitemap.xml": new_sha}.items() if old.get(p) != s}
print(f"  changed paths: {changed}")

unexplained = [r for r in required if r not in changed.values()]
if unexplained:
    sys.exit(f"STOPPING: deploys wants content we did not change: {unexplained}")

print(f"\nuploading /sitemap.xml ({len(new_bytes)} bytes, sha1 {new_sha[:12]}) ...")
call("PUT", f"/deploys/{DEPLOY}/files/sitemap.xml", new_bytes, ctype="application/octet-stream")
print("uploaded; waiting for it to go live")

for _ in range(60):
    d = call("GET", f"/deploys/{DEPLOY}")
    st = d.get("state")
    if st in ("ready", "error", "rejected"):
        print(f"final state = {st}")
        print(f"ssl_url      = {d.get('ssl_url')}")
        print(f"deploy_time  = {d.get('deploy_time')}s")
        print(f"published_at = {d.get('published_at')}")
        sys.exit(0 if st == "ready" else 3)
    time.sleep(3)

sys.exit("timed out waiting for readiness")
