# WitnessOS public website

The maintained source of `https://witnessos.com.au`, served from this directory of the
public WitnessOS repository. It previously lived in `narko4u/witnessos-site`, which is
archived with its history intact; this copy is the live one.

## Preview

Open `dist/index.html` directly in a browser. No build command, package manager, web
server, external font or CDN is required.

## Configuration

- Public domain constant in visible copy: `WitnessOS.com.au`
- CTA email: `contact@empirelabs.com.au`
- Netlify publish directory: `dist`
- Netlify build command: `python3 build_and_verify.py` (set in `netlify.toml`)
- Netlify project that serves witnessos.com.au: `4bdc4cd1-fa6b-4283-9eb8-937081514401`

Search the built page for either constant to update it. Keep the public evidence ladder
closed at E4. Do not publish internal architecture, repository paths or implementation
details.


## Build and deploy

`dist` is generated. Edit `_bodies/` and the page metadata in `assemble.py`, never the built HTML.

```
python3 build_and_verify.py     # assemble from _bodies/ into publish-v2/, then dist/
```

The build fails on a missing beacon, an untagged call to action or a content security policy hash that no longer matches the pages it covers.

Run `npm ci` before deploying. The `/api/ev` beacon function imports
`@netlify/blobs`, and a manual `--dir dist` deploy packages the function from
the local tree. Without `node_modules`, Netlify ships `ev.mjs` with an import it
cannot resolve and the endpoint answers 502 while every page still renders, so
the failure is invisible unless you probe the endpoint.

Deploy to production:

```
netlify deploy --prod --site 4bdc4cd1-fa6b-4283-9eb8-937081514401
```

Always pass `--site`. The repository's `.netlify/state.json` pointed at an unrelated
Netlify project for a period, so a bare `netlify deploy --prod` published to the wrong
site and reported success while witnessos.com.au stayed unchanged. The id above is the
one that serves witnessos.com.au.

Verify every deploy against the live domain rather than the deploy log. The log reporting
"Deploy is live!" says nothing about which domain received the files. The host rewrites
internal links to extensionless pretty URLs at the edge, so compare a canonicalised form
rather than raw bytes when checking that a build matches production.

## Launch gate

Do not deploy or attach the custom domain until the scope owner approves the final
review build.

