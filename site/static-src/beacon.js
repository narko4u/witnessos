/* WitnessOS first-party traffic beacon.
 *
 * Privacy-first by construction, which matters more here than anywhere else:
 * WitnessOS sells verifiable compliance, so the site cannot itself ship a
 * third-party tracker. There is no Google Analytics, no cookie, no request to
 * any host other than this one.
 *
 *   - no cookies, no third-party requests, no fingerprinting
 *   - honours Do Not Track and Global Privacy Control (silent no-op if set)
 *   - sends only: page path, referrer HOST, an anonymous random visitor id,
 *     a per-session id and the data-cta id of a clicked element
 *   - never sends query strings, form values or anything typed by a user
 *
 * Endpoint is first-party (/api/ev on our own origin). Storage is a random id
 * in localStorage; if storage is unavailable the id degrades to per-page-load,
 * which undercounts rather than overcounts returning visitors.
 */
(function () {
  "use strict";

  var ENDPOINT = "/api/ev";
  var VID_KEY = "wo_vid";
  var SID_KEY = "wo_sid";

  function optedOut() {
    try {
      if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return true;
      if (navigator.globalPrivacyControl === true) return true;
    } catch (e) {}
    return false;
  }
  if (optedOut()) return;

  function randId() {
    try {
      var a = new Uint8Array(8);
      (window.crypto || window.msCrypto).getRandomValues(a);
      var s = "";
      for (var i = 0; i < a.length; i++) s += ("0" + a[i].toString(16)).slice(-2);
      return s;
    } catch (e) {
      return String(Date.now()) + Math.random().toString(16).slice(2, 10);
    }
  }

  function safeStore(name) {
    try {
      var s = window[name];
      if (!s) return null;
      s.getItem("__wo_t");
      return s;
    } catch (e) {
      return null;
    }
  }

  function readId(s, key) {
    if (!s) return randId();
    var v = null;
    try { v = s.getItem(key); } catch (e) {}
    if (!v) {
      v = randId();
      try { s.setItem(key, v); } catch (e) {}
    }
    return v;
  }

  var vid = readId(safeStore("localStorage"), VID_KEY);
  var sid = readId(safeStore("sessionStorage"), SID_KEY);

  function send(payload) {
    try {
      var body = JSON.stringify(payload);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "application/json" }));
      } else {
        var x = new XMLHttpRequest();
        x.open("POST", ENDPOINT, true);
        x.setRequestHeader("Content-Type", "application/json");
        x.send(body);
      }
    } catch (e) {}
  }

  function pagePath() {
    try { return (location.pathname || "/").slice(0, 120); } catch (e) { return "/"; }
  }

  function refHost() {
    try {
      if (!document.referrer) return "";
      var u = document.createElement("a");
      u.href = document.referrer;
      if (u.hostname === location.hostname) return "";
      return u.hostname.slice(0, 80);
    } catch (e) {
      return "";
    }
  }

  send({ t: "pv", p: pagePath(), r: refHost(), v: vid, s: sid });

  /* Capture-phase delegation: a click is recorded before any navigation starts,
   * and the listener never calls preventDefault, so behaviour is unchanged. */
  document.addEventListener("click", function (ev) {
    var el = ev.target;
    var depth = 0;
    while (el && el.nodeType === 1 && depth < 8) {
      if (el.getAttribute && el.getAttribute("data-cta")) {
        send({ t: "cta", p: pagePath(), c: el.getAttribute("data-cta").slice(0, 80), v: vid, s: sid });
        return;
      }
      el = el.parentNode;
      depth++;
    }
  }, true);

  /* Public tracking API, for anything on this site that wants to mark a step.
   *
   *   window.woTrack("cta", "pricing")
   *
   * Only "cta", "tool_start", "tool_complete" and "lead" are accepted and the
   * name is a short slug, never anything a visitor typed. */
  var TYPES = { cta: 1, tool_start: 1, tool_complete: 1, lead: 1 };

  function track(type, name) {
    if (!TYPES[type]) return;
    send({
      t: type,
      p: pagePath(),
      c: String(name || "").replace(/[^\w.-]/g, "").slice(0, 80),
      v: vid,
      s: sid
    });
  }

  window.woTrack = track;
})();
