// service_worker.js

const CACHE_NAME    = 'superpig-v5';
const SHELL_CACHE   = 'superpig-shell-v2';


const STATIC_ASSETS = [
    '/manifest.json',
    '/static_m/images/logo/superpig_192_192.png',
    '/static_m/images/logo/superpig_512_512.png'
];

// App shell files (cached for offline)
const SHELL_FILES = [
    '/index_mob.html',
    '/app',
    '/en',
    '/bis',
    '/tag'
];


// Auth-related paths that should NEVER be cached
const AUTH_PATHS = [
    '/login',
    '/logout',
    '/user/verify_token'
];


// Install event - cache assets
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    event.waitUntil(
        Promise.all([
            // Cache static assets
            caches.open(CACHE_NAME).then((cache) => {
                return cache.addAll(STATIC_ASSETS);
            }),
            
            // Cache app shell for offline
            caches.open(SHELL_CACHE).then((cache) => {
                return cache.addAll(SHELL_FILES);
            })
        ])
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
        
        path.startsWith('/system/')             ||
        
        AUTH_PATHS.some(authPath => path === authPath || path.startsWith(authPath + '?'))
    ){
        // Don't intercept API calls
        return;
    }
    
    
    // --- 2. Handle HTML Navigation (Cache First) ---    
    if (request.mode === 'navigate') {
        event.respondWith(
            (async () => {
                // Get cached shell immediately (do this first)
                const cachedShell = await caches.match('/index_mob.html');
                
                // Check online status
                let isOnline = true;
                try {
                    // Quick online check
                    await fetch('/favicon.ico?t=' + Date.now(), { method: 'HEAD', cache: 'no-store', mode: 'no-cors' });
                } catch (e) {
                    isOnline = false;
                }
                
                // If offline, serve cache immediately
                if (!isOnline && cachedShell) {
                    console.log('SW: Offline - serving cached shell');
                    return cachedShell;
                }
                
                // Try network but with timeout
                try {
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), 2000);
                    
                    const networkResponse = await fetch(request, { signal: controller.signal });
                    clearTimeout(timeoutId);
                    
                    if (networkResponse && networkResponse.status === 200) {
                        const cache = await caches.open(SHELL_CACHE);
                        cache.put(request, networkResponse.clone());
                        return networkResponse;
                    }
                } catch (error) {
                    console.log('SW: Network timeout/error');
                }
                
                // Fallback to cache
                if (cachedShell) {
                    console.log('SW: Falling back to cached shell');
                    return cachedShell;
                }
                
                return new Response('App unavailable offline', { status: 503 });
            })()
        );
        return;
    }
        
    
    // --- 3. Handle static assets with STALE-WHILE-REVALIDATE (best for offline) ---
    event.respondWith(
        (async () => {
            const cache = await caches.open(CACHE_NAME);
            const cachedResponse = await cache.match(event.request);
            
            // Return cached response immediately if available
            if (cachedResponse) {
                // But update cache in background
                fetch(event.request).then(async (networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        await cache.put(event.request, networkResponse);
                    }
                }).catch(() => {
                    // Network error, keep using cached version
                });
                return cachedResponse;
            }
            
            // Not in cache, try network
            try {
                const networkResponse = await fetch(event.request);
                if (networkResponse && networkResponse.status === 200) {
                    await cache.put(event.request, networkResponse.clone());
                }
                return networkResponse;
            } catch (error) {
                // Network error and not in cache
                console.log('Failed to fetch:', event.request.url);
                return new Response('Resource not available offline', { status: 404 });
            }
        })()
    );
});


// Activate event - clean old caches AND check version
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating... v5');
    event.waitUntil(
        Promise.all([
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME && cacheName !== SHELL_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            // Ensure shell cache has minimum files
            caches.open(SHELL_CACHE).then(async (cache) => {
                const hasIndex = await cache.match('/index_mob.html');
                if (!hasIndex) {
                    console.log('Re-adding shell files to cache');
                    await cache.addAll(SHELL_FILES);
                }
            }),
            // Claim clients immediately
            self.clients.claim()
        ])
    );
});


// Listen for messages from the app
self.addEventListener('message', (event) => {
    if (event.data === 'skipWaiting') {
        self.skipWaiting();
    }
    
    if (event.data === 'clearAuthCache') {
        // Only clear auth-related caches, keep shell
        caches.open(SHELL_CACHE).then(cache => {
            cache.keys().then(keys => {
                keys.forEach(key => {
                    if (key.url.includes('/login') || 
                        key.url.includes('/user/')) {
                        cache.delete(key);
                    }
                });
            });
        });
    }
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
                    return clients.openWindow('/app');
                }
            })
    );
});


