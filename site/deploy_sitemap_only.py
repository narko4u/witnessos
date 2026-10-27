#!/usr/bin/env python3
"""Digest-preserving Netlify production deploy.

Reuses every blob already in the live deploy (declared by Netlify's own sha1
digests) and uploads ONLY the sitemap.xml we changed. Nothing else -- pages,
assets, robots.txt, netlify.toml -- is re-uploaded or reinterpreted, so the
deployed bytes for every other path stay identical.

Safety: prints the required-upload set before uploading. If Netlify asks for
anything other than /sitemap.xml we stop without uploading.
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
STAGE = pathlib.Path("/home/vault/witnessos-site-work/publish-v2")
MANIFEST = pathlib.Path("/tmp/sitefiles.json")
CFG = pathlib.Path(os.path.expanduser("~/.config/netlify/config.json"))
API = "https://api.netlify.com/api/v1"


def token() -> str:
    # The CLI is authenticated via NETLIFY_AUTH_TOKEN in this environment.
    env = os.environ.get("NETLIFY_AUTH_TOKEN", "").strip()
    if len(env) > 20:
        return env

    cfg = json.loads(CFG.read_text())

    def walk(o):
        if isinstance(o, dict):
            if "token" in o and isinstance(o["token"], str) and len(o["token"]) > 20:
                return o["token"]
            for v in o.values():
                r = walk(v)
                if r:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = walk(v)
                if r:
                    return r
        return None

    t = walk(cfg)
    if not t:
        sys.exit("could not locate a Netlify token in config.json")
    return t


TOK = token()
HDRS = {"Authorization": f"Bearer {TOK}", "User-Agent": "sovereign-deploy/1.0"}


def call(method: str, path: str, body=None, ctype="application/json"):
    data = None
    if body is not None:
        data = json.dumps(body).encode() if ctype == "application/json" else body
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Content-Type", ctype)
    for k, v in HDRS.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} on {method} {path}: {e.read()[:600].decode(errors='replace')}")
        raise


# 1. digest map = live deploy's shas, with the new sitemap swapped in
old = {f["path"]: f["sha"] for f in json.loads(MANIFEST.read_text())}
new_bytes = (STAGE / "sitemap.xml").read_bytes()
new_sha = hashlib.sha1(new_bytes).hexdigest()
if old.get("/sitemap.xml") == new_sha:
    sys.exit("refusing: sitemap digest unchanged, nothing to deploy")
print(f"old sitemap sha1: {old['/sitemap.xml']}")
print(f"new sitemap sha1: {new_sha}  ({len(new_bytes)} bytes)")

files = dict(old)
files["/sitemap.xml"] = new_sha

# 2. create the deploy
print(f"\ncreating deploy with {len(files)} declared paths...")
dep = call(
    "POST",
    f"/sites/{SITE}/deploys",
    {
        "files": files,
        "title": "fix(seo): add products, passport, instructions and pricing to sitemap.xml",
    },
)
did = dep["id"]
required = dep.get("required") or []
print(f"deploy id: {did}\nstate: {dep.get('state')}\nrequired uploads ({len(required)}): {required}")

if required != ["/sitemap.xml"]:
    print("\nSTOPPING: Netlify asked for something other than /sitemap.xml.")
    print("No upload performed, so the live deploy is untouched.")
    sys.exit(2)

# 3. upload the one changed file
print("\nuploading /sitemap.xml ...")
call("PUT", f"/deploys/{did}/files/sitemap.xml", new_bytes, ctype="application/octet-stream")
print("uploaded")

# 4. wait for it to go live
for i in range(40):
    d = call("GET", f"/deploys/{did}")
    st = d.get("state")
    if st in ("ready", "error", "rejected"):
        print(f"final state: {st}  (ssl_url={d.get('ssl_url')})")
        print("deploy time:", d.get("deploy_time"), "| published_at:", d.get("published_at"))
        if st != "ready":
            sys.exit(3)
        break
    time.sleep(3)
else:
    sys.exit("timed out waiting for deploy to become ready")
