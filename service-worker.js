const CACHE_NAME = 'health-ai-app-final';
const urlsToCache = [
  '/health-and-wellness-Ai-1/',
  '/health-and-wellness-Ai-1/index.html',
  '/health-and-wellness-Ai-1/manifest.json',
  '/health-and-wellness-Ai-1/icons/icon-192.png',
  '/health-and-wellness-Ai-1/icons/icon-512.png'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache opened');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
