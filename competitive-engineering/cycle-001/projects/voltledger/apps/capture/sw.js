// Immutable app shell cache. IndexedDB captures remain local and are never transferred by this worker.
const VERSION = "voltledger-shell-ux-v1";
const SHELL = [
  "./index.html", "./ui.css", "./ux.js", "./app.js", "./core.js",
  "./wasm-core.js", "./wire.js", "./core.wasm",
  "./manifest.webmanifest", "./icon.svg",
];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(VERSION).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((key) => key.startsWith("voltledger-shell-") && key !== VERSION).map((key) => caches.delete(key)))).then(() => self.clients.claim()),
  );
});
self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;
  event.respondWith(caches.match(request).then((hit) => hit || fetch(request)));
});
