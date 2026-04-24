const CACHE_NAME = 'superpig-v1';
const urlsToCache = [
    '/',
    '/index_mob.html',
    '/manifest.json',
    '/static_m/images/logo/superpig_192_192.png',
    '/static_m/images/logo/superpig_512_512.png'
];


// Install event - cache assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return Promise.allSettled(
                urlsToCache.map((url) => {
                    return cache.add(url).catch((error) => {
                        console.warn(`Failed to cache ${url}:`, error);
                    });
                })
            );
        })
    );
});


// Fetch event - serve cached or network
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Return cached response if found
                if (response) {
                    return response;
                }
                // Otherwise fetch from network
                return fetch(event.request);
            })
    );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});
