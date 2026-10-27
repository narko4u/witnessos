/* First-party traffic collector for witnessos.com.au.
 *
 * Accepts POST /api/ev with a small JSON body from /beacon.js and aggregates it
 * into Netlify Blobs. There is no public read path: the aggregates are read
 * back with tools/stats.mjs using an authenticated token, so no visitor data is
 * ever exposed through the site.
 *
 * Privacy: the only identifiers stored are an anonymous random visitor id and a
 * session id, both generated in the browser. No cookies, no IP addresses, no
 * user agent strings, no query strings are persisted.
 *
 * Failure mode is deliberately silent: anything malformed or oversized returns
 * 204 and is dropped, so the beacon can never surface an error to a visitor.
 */
import { getStore } from "@netlify/blobs";

const STORE_NAME = "traffic";
const MAX_BODY_BYTES = 2048;
const TYPES = new Set(["pv", "cta", "tool_start", "tool_complete", "lead"]);

function dayKey() {
  return new Date().toISOString().slice(0, 10);
}

/* Keep only characters that belong in a path or slug. Anything else is a sign
 * of a malformed or hostile payload, so it is stripped rather than escaped. */
function clean(value, max) {
  if (typeof value !== "string") return "";
  return value.replace(/[^\w\-./:@ ]+/g, "").slice(0, max);
}

/* Compare-and-set increment. Netlify Blobs has no atomic add, so this reads the
 * current etag and writes back conditionally, retrying when it loses a race.
 * MORE_ATTEMPTS than the empirelabs collector: a lost race used to drop the
 * increment silently, which undercounts page views. */
const ATTEMPTS = 8;

async function bump(store, key, delta) {
  for (let attempt = 0; attempt < ATTEMPTS; attempt++) {
    let current = null;
    try {
      current = await store.getWithMetadata(key, { type: "json" });
    } catch (err) {
      current = null;
    }
    const n = current && current.data && typeof current.data.n === "number"
      ? current.data.n
      : 0;
    try {
      const next = { n: n + delta };
      if (current && current.etag) {
        await store.setJSON(key, next, { onlyIfMatch: current.etag });
      } else {
        await store.setJSON(key, next, { onlyIfNew: true });
      }
      return true;
    } catch (err) {
      /* lost the race or the key appeared underneath us: retry */
    }
  }
  /* Out of attempts. Record the loss rather than pretending it did not happen,
   * so a systematic undercount is visible instead of invisible. */
  try {
    await bumpDropped(store);
  } catch (err) {}
  return false;
}

/* Separate counter for dropped increments, bumped with the same discipline but
 * without recursing into bump(). */
async function bumpDropped(store) {
  const key = `d/${dayKey()}/dropped/increment`;
  for (let attempt = 0; attempt < 4; attempt++) {
    let current = null;
    try {
      current = await store.getWithMetadata(key, { type: "json" });
    } catch (err) {
      current = null;
    }
    const n = current && current.data && typeof current.data.n === "number"
      ? current.data.n
      : 0;
    try {
      const next = { n: n + 1 };
      if (current && current.etag) {
        await store.setJSON(key, next, { onlyIfMatch: current.etag });
      } else {
        await store.setJSON(key, next, { onlyIfNew: true });
      }
      return true;
    } catch (err) {
      /* retry */
    }
  }
  return false;
}

/* One marker key per visitor per day, so the count of these keys is the count of
 * daily unique visitors. Writing with onlyIfNew means repeat views do not churn. */
async function markUnique(store, key) {
  try {
    const existing = await store.get(key);
    if (existing !== null) return;
    await store.set(key, "1", { onlyIfNew: true });
  } catch (err) {
    /* a duplicate marker is harmless */
  }
}

/* Synthetic health-check traffic. verify_traffic.py posts a known visitor id
 * and a known path so it can assert the collector is reachable. Those events
 * are acknowledged and then dropped, because a health check must never be able
 * to inflate a number a human is later asked to trust. */
const PROBE_VISITOR = "verifyprobe";
const PROBE_PATH_PREFIX = "/__verify__";

export default async (req) => {
  if (req.method !== "POST") {
    return new Response(null, { status: 405, headers: { Allow: "POST" } });
  }

  let raw = "";
  try {
    const buf = await req.arrayBuffer();
    if (!buf || buf.byteLength === 0 || buf.byteLength > MAX_BODY_BYTES) {
      return new Response(null, { status: 204 });
    }
    raw = new TextDecoder().decode(buf);
  } catch (err) {
    return new Response(null, { status: 204 });
  }

  let event;
  try {
    event = JSON.parse(raw);
  } catch (err) {
    return new Response(null, { status: 204 });
  }

  const type = TYPES.has(event && event.t) ? event.t : null;
  if (!type) return new Response(null, { status: 204 });

  const path = clean(event.p, 120) || "/";
  const visitor = clean(event.v, 32);
  const label = clean(event.c, 80);
  const referrer = clean(event.r, 80);
  const day = dayKey();
  const store = getStore(STORE_NAME);

  if (visitor === PROBE_VISITOR || path.startsWith(PROBE_PATH_PREFIX)) {
    return new Response(null, { status: 204 });
  }

  if (type === "pv") {
    const work = [bump(store, `d/${day}/pv/${path}`, 1)];
    if (referrer) work.push(bump(store, `d/${day}/ref/${referrer}`, 1));
    if (visitor) work.push(markUnique(store, `d/${day}/uv/${visitor}`));
    await Promise.all(work);
    return new Response(null, { status: 204 });
  }

  await bump(store, `d/${day}/${type}/${label || "unknown"}`, 1);
  return new Response(null, { status: 204 });
};

export const config = { path: "/api/ev", method: "POST" };
