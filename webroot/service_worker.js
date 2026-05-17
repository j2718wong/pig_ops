// service_worker.js

const CACHE_NAME = 'superpig-v1';
const urlsToCache = [
    '/',
    '/app',
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
    const url       = new URL(event.request.url);
    const path      = url.pathname;
    const request   = event.request;
    
    // 1.) Skip API calls - let them fail normally; app handles offline
    if (path.startsWith('/country/')            ||
        path.startsWith('/lookup/')             ||
        path.startsWith('/pig_farm/')           ||
        path.startsWith('/account/')            ||
        path.startsWith('/user/')               ||
        path.startsWith('/sow_boar/')           ||
        path.startsWith('/pig_prod/')           ||
        
        
        path.startsWith('/access_code/')        ||
        path.startsWith('/account_bill/')       ||
        path.startsWith('/account_medvac/')     ||
        path.startsWith('/account_pig_buyer/')  ||
        path.startsWith('/account_pig_ops/')    ||
        
        path.startsWith('/address/')            ||
        
        path.startsWith('/b/')                  ||
        
        path.startsWith('/supplier/')           ||
        path.startsWith('/customer/')           ||
        
        path.startsWith('/feed_balance/')       ||
        path.startsWith('/feed_brand/')         ||
        path.startsWith('/feed_buy/')           ||
        
        path.startsWith('/medvac_brand/')       ||
        path.startsWith('/medvac_type/')        ||
        
        path.startsWith('/pf_feed_buy/')        ||
        path.startsWith('/pf_feed_buy_item/')   ||
        path.startsWith('/pig_farm_staff/')     ||
        path.startsWith('/pig_medvac/')         ||
        
        path.startsWith('/pig_prod_feed/')      ||
        path.startsWith('/pig_prod_notes/')     ||
        path.startsWith('/prod_pig_dead/')      ||
        path.startsWith('/pig_prod_pig_ops/')   ||
        path.startsWith('/prod_harvest/')       ||
        
        path.startsWith('/report/')             ||
        path.startsWith('/semen_sup_semen/')    ||
        
        path.startsWith('/boar_ext_mate/')      ||
        path.startsWith('/sow_boar_mate/')      ||
        
        path.startsWith('/system/')
    )
    
    {
        // Don't intercept API calls
        return;
    }
    
    
    // --- 2. Handle HTML Navigation (Cache First) ---
    if (request.mode === 'navigate') {
        event.respondWith(
            fetch(request).catch(() => {
                // If the network request fails (offline), serve the cached SPA shell.
                return caches.match('/index_mob.html');
            })
        );
        return;
    }
    
    
    // --- 3. Handle static assets (Cache First) ---
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


