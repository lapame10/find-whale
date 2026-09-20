/* ==========================================================================
   FIND WHALE — service worker
   --------------------------------------------------------------------------
   Esto es lo que hace que la app ABRA SIN RED. Muy importante: si estas en
   una ladera sin cobertura y abres la app, tiene que funcionar igual.
   Guarda una copia de la app y de las librerias (mapa) en el telefono.
   ========================================================================== */

const CACHE = 'findwhale-v10';
const ESENCIAL = [
  './',
  './index.html',
  './manifest.json',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-database-compat.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ESENCIAL).catch(() => {})).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = e.request.url;

  /* los datos de Firebase y los mapas: SIEMPRE a la red, y si falla, nada.
     (las posiciones las guarda la propia app en su cola, aqui no se cachean) */
  if (url.includes('firebaseio.com') || url.includes('tile.opentopomap.org')
      || url.includes('tile.openstreetmap.org')) return;

  /* lo demas: primero la copia guardada, y si no está, la red */
  e.respondWith(
    caches.match(e.request).then(hit => {
      if (hit) {
        /* y de paso refresco en segundo plano si hay red */
        fetch(e.request).then(r => {
          if (r && r.ok) caches.open(CACHE).then(c => c.put(e.request, r));
        }).catch(() => {});
        return hit;
      }
      return fetch(e.request).then(r => {
        if (r && r.ok && e.request.method === 'GET') {
          const copia = r.clone();
          caches.open(CACHE).then(c => c.put(e.request, copia));
        }
        return r;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
