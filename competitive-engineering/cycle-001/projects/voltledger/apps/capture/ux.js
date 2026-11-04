// VoltLedger field presentation only. No business rules, storage, or sync logic here.
// Existing app.js still owns indexedDB persistence and the Rust/JS engine decision.
function ready(fn) {
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn, { once: true });
  else fn();
}
ready(() => {
  const $ = (s) => document.querySelector(s);
  const all = (s) => [...document.querySelectorAll(s)];
  const home = $("#home");
  const counts = $("#counts");
  const outbox = $("#outbox");
  const items = $("#items");
  const search = $("#searchAssets");
  const navs = all("[data-nav]");
  const badge = $("#engineLabel");
  const today = $("#todayLabel");

  today.textContent = new Date().toLocaleDateString("en-AU", {
    weekday: "short", day: "numeric", month: "short",
  }).toUpperCase();

  function inspectUiState() {
    const bodyText = counts.textContent || "";
    const values = Object.fromEntries(
      ["overdue", "due soon", "current", "untested"].map((key) => {
        const re = new RegExp("(\\d+)\\s+" + key.replace(" ", "\\s+"), "i");
        const match = bodyText.match(re);
        return [key, match ? Number(match[1]) : 0];
      }),
    );
    const total = values.overdue + values["due soon"] + values.current + values.untested;
    const saved = Number.parseInt(outbox.textContent, 10) || 0;
    $("#assetTotal").textContent = String(total);
    $("#attentionTotal").textContent = String(values.overdue + values["due soon"]);
    $("#savedTotal").textContent = String(saved);
    $("#attentionTotal").parentElement.classList.toggle("has-attention", values.overdue + values["due soon"] > 0);

    const engine = document.body.dataset.engine;
    if (engine === "rust-wasm") {
      badge.textContent = "Rust-WASM core active";
      badge.style.color = "var(--ok)";
    } else if (engine === "js-fallback") {
      badge.textContent = "JavaScript fallback active — verify before field use";
      badge.style.color = "var(--warn)";
    } else {
      badge.textContent = "Loading local rule engine";
    }
    filterItems();
  }

  function filterItems() {
    const query = search.value.trim().toLocaleLowerCase("en-AU");
    const rows = all("#items li.row");
    for (const row of rows) {
      const matches = !query || row.textContent.toLocaleLowerCase("en-AU").includes(query);
      row.hidden = !matches;
      row.style.display = matches ? "" : "none";
    }
  }

  let scheduled = false;
  function scheduleInspect() {
    if (scheduled) return;
    scheduled = true;
    queueMicrotask(() => {
      scheduled = false;
      inspectUiState();
    });
  }
  new MutationObserver(scheduleInspect).observe(counts, { childList: true, characterData: true, subtree: true });
  new MutationObserver(scheduleInspect).observe(outbox, { childList: true, characterData: true, subtree: true });
  new MutationObserver(scheduleInspect).observe(items, { childList: true, subtree: false });
  new MutationObserver(scheduleInspect).observe(document.body, { attributes: true, attributeFilter: ["data-engine"] });
  search.addEventListener("input", filterItems);
  scheduleInspect();

  function setNav(sectionId) {
    for (const a of navs) {
      const selected = a.dataset.nav === sectionId;
      a.classList.toggle("nav-current", selected);
      if (selected) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    }
  }
  navs.forEach((a) => a.addEventListener("click", () => setNav(a.dataset.nav)));
  const observer = new IntersectionObserver(
    (entries) => {
      const ranked = entries.filter((e) => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (ranked[0]) setNav(ranked[0].target.id);
    },
    { rootMargin: "-20% 0px -50% 0px", threshold: [0, 0.1, 0.3, 0.5] },
  );
  ["home", "capture", "register", "reports"].forEach((id) => observer.observe(document.getElementById(id)));

  const quick = $("#quickScan");
  quick.addEventListener("click", () => setTimeout(() => $("#tag").focus({ preventScroll: true }), 250));

  let deferredPrompt = null;
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
  });
  const install = $("#install");
  const info = (message) => {
    const banner = $("#banner");
    banner.textContent = message;
    banner.className = "banner warn";
    setTimeout(() => {
      if (banner.textContent === message) banner.className = "banner hidden";
    }, 9000);
  };
  install.addEventListener("click", async () => {
    if (window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true) {
      info("VoltLedger is already running as an installed app.");
      return;
    }
    if (deferredPrompt) {
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
      return;
    }
    const isIos = /iPhone|iPad|iPod/i.test(navigator.userAgent);
    info(isIos
      ? "On iPhone: open Share in Safari, then choose Add to Home Screen."
      : "In Chrome or your browser menu, choose Install app or Add to Home screen. An HTTPS or localhost address is required.");
  });
  window.addEventListener("appinstalled", () => { install.textContent = "Installed"; install.disabled = true; });

  // Keep the actual native browser-install workflow separate from QR distribution.
  // A printable QR code is generated from the eventual approved HTTPS URL.
  if (window.matchMedia("(display-mode: standalone)").matches) {
    install.textContent = "Installed"; install.disabled = true;
  }
});
