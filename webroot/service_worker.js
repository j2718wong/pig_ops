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
            action: data.data?.action,
            payload: data.data?.payload
        }
    };

    // Show the notification to the user
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});


// Handle user clicking on the notification
self.addEventListener('notificationclick', async (event) => {
    console.log('🔔 Notification clicked');
    console.log('Notification data:', event.notification.data);
    
    event.notification.close();
    
    const action = event.notification.data?.action;
    const payload = event.notification.data?.payload;

    console.log('Action:', action);
    console.log('Payload:', payload);

    const data_to_client = { action, payload };
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then(async (clientList) => {
                if (clientList.length > 0) {
                    // App is open - send message
                    console.log('📨 Sending message to client:', data_to_client);
                    clientList[0].postMessage(data_to_client);
                    return clientList[0].focus();
                } else {
                    // App not open - store pending action
                    console.log('📦 No clients, storing pending action');
                    if (data_to_client && data_to_client.action) {
                        const cache = await caches.open('superpig-pending');
                        await cache.put('pending-action', new Response(JSON.stringify(data_to_client)));
                    }
                    return clients.openWindow('/');
                }
            })
    );
});


