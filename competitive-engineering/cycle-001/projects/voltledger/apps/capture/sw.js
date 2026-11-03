// Shell cache only. Test records never touch the network, so nothing here can lose one.
const VERSION = "voltledger-shell-v2";
const SHELL = [
  "./index.html", "./app.js", "./core.js", "./wasm-core.js",
  "./wire.js", "./core.wasm",
  "./manifest.webmanifest", "./icon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  event.respondWith(
    caches.match(request).then((hit) => hit || fetch(request).then((res) => {
      const copy = res.clone();
      caches.open(VERSION).then((c) => c.put(request, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match("./index.html"))),
  );
});
