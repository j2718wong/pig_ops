const CACHE_NAME = 'superpig-v1';
const urlsToCache = [
    '/',
    '/en',
    '/bis',
    '/tag',
    '/index_mob.html',
    '/manifest.json',
    '/static_m/images/logo/superpig_192_192.png',
    '/static_m/images/logo/superpig_512_512.png'
];


// Install event - cache assets
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
    self.skipWaiting(); // Force activation
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
    console.log('Service Worker activating...');
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
    return self.clients.claim(); // Take control immediately
});


// Listen for push notifications from the server
self.addEventListener('push', (event) => {
    // Parse the notification data sent from your backend
    let data = {};
    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data = {
                title: 'SuperPig',
                body: event.data.text()
            };
        }
    }

    // Default values if server didn't send specific data
    const title = data.title || 'SuperPig';
    const options = {
        body: data.body || 'You have a new notification.',
        icon: '/static_m/images/logo/superpig_192_192.png',
        badge: '/static_m/images/logo/superpig_192_192.png',
        tag: data.tag || 'default', // Prevents duplicate notifications
        data: {
            url: data.url || '/' // Where to take the user when they click
        }
    };

    // Show the notification to the user
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Handle user clicking on the notification
self.addEventListener('notificationclick', (event) => {
    event.notification.close(); // Close the notification popup

    // Open or focus the SuperPig app
    event.waitUntil(
        clients.matchAll({
            type: 'window',
            includeUncontrolled: true
        })
        .then(windowClients => {
            // If app window is already open, focus it
            for (let client of windowClients) {
                if (client.url === event.notification.data.url && 'focus' in client) {
                    return client.focus();
                }
            }
            // Otherwise open a new window/tab
            if (clients.openWindow) {
                return clients.openWindow(event.notification.data.url);
            }
        })
    );
});



