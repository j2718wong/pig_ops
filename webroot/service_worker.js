// service_worker.js

// Add at the very first line
console.log('Service worker script starting...');

// Add error handler at the top
self.addEventListener('error', (e) => {
    console.error('SW Error:', e.error);
});

self.addEventListener('unhandledrejection', (e) => {
    console.error('SW Unhandled rejection:', e.reason);
});


const CACHE_NAME    = 'superpig-v26';
const SHELL_CACHE   = 'superpig-shell-v23';


const STATIC_ASSETS = [
    '/manifest.json',
    '/static_m/images/logo/superpig_192_192.png',
    '/static_m/images/logo/superpig_512_512.png',
    '/static_m/js/pwa-handler.js',
    
    
     // CSS files
    '/static_m/css/all.min.css',
    '/static_m/css/bootstrap.min.css',
    '/static_m/css/bootstrap-datepicker.min.css',
    '/static_m/css/bootstrap-icons.css',
    
    // JavaScript libraries
    '/static_m/js/jquery/jquery.min-3.7.1.js',
    '/static_m/js/jquery/jquery-ui.min-1.14.1.js',
    '/static_m/js/library/bootstrap.bundle.min.js',
    '/static_m/js/library/bootstrap-datepicker.min.js',
    
    // Images
    '/static_m/images/box_check.png',
    
    // MAR images
    '/static_m/images/mar/mar_home.png',
    '/static_m/images/mar/mar_sow_list.png',
    '/static_m/images/mar/mar_gesta.png',
    '/static_m/images/mar/mar_farrowing.png',
    '/static_m/images/mar/mar_lacta.png',
    '/static_m/images/mar/mar_pig_ops.png',
    '/static_m/images/mar/mar_fattening.png',
    '/static_m/images/mar/mar_feed_records.png',
    '/static_m/images/mar/mar_no_internet.png',
    '/static_m/images/mar/mar_report.png'
];


// App shell files (cached for offline)
const SHELL_FILES = [
    '/app',
    '/en',
    '/bis',
    '/tag',
    '/static_m/js/pwa-handler.js'
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
        (async () => {
            const cache = await caches.open(CACHE_NAME);
            
            // 1. Cache static assets (these don't change)
            try {
                await cache.addAll(STATIC_ASSETS);
                console.log('✅ Static assets cached');
            } catch (e) {
                console.error('Failed to cache static assets:', e);
            }
            
            // 2. Dynamically get current bundle names from manifest.json
            try {
                // Use a timeout to avoid hanging
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 5000);
                
                const manifestRes = await fetch('/static/js/manifest.json', {
                    signal: controller.signal,
                    cache: 'no-store'
                });
                clearTimeout(timeoutId);
                
                if (manifestRes.ok) {
                    const manifest = await manifestRes.json();
                    console.log('📦 Manifest loaded:', manifest);
                    
                    // Cache core bundle
                    if (manifest.core) {
                        const coreUrl = `/static/js/${manifest.core}`;
                        await cache.add(coreUrl);
                        console.log('✅ Cached core bundle:', manifest.core);
                    }
                    
                    // Cache login bundle  
                    if (manifest.login) {
                        const loginUrl = `/static/js/${manifest.login}`;
                        await cache.add(loginUrl);
                        console.log('✅ Cached login bundle:', manifest.login);
                    }
                    
                    // Cache CSS
                    if (manifest.main_css) {
                        const cssUrl = `/static/css/${manifest.main_css}`;
                        await cache.add(cssUrl);
                        console.log('✅ Cached CSS:', manifest.main_css);
                    }
                } else {
                    console.warn('Manifest not found, bundles may not be cached');
                }
            } catch (e) {
                console.error('Failed to cache dynamic bundles:', e);
                // Don't fail the entire install - static assets are cached
            }
        })()
    );
    self.skipWaiting();
});


// Fetch event - serve cached or network
self.addEventListener('fetch', (event) => {
    const url       = new URL(event.request.url);
    const path      = url.pathname;
    const request   = event.request;
    
    
    // Dont include timestamped requests
    if (url.search && (url.search.includes('t=') || url.search.includes('timestamp'))) {
        // Don't intercept or cache - let browser handle normally
        return;
    }
    
    // Skip OAuth and authentication endpoints
    if (url.pathname.startsWith('/auth/') || 
        url.pathname.startsWith('/login') ||
        url.pathname.startsWith('/logout') ||
        url.hostname.includes('accounts.google.com') ||
        url.hostname.includes('googleapis.com')) {
        // Don't intercept - let the browser handle normally
        return;
    }
    
    
    if (request.method !== 'GET') {
        // Don't cache POST, PUT, DELETE, etc.
        return;
    }
    
    
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
        path.startsWith('/acc_sow_due_chklst')  ||
        
        path.startsWith('/address/')            ||
        
        path.startsWith('/b/')                  ||
        
        path.startsWith('/supplier/')           ||
        path.startsWith('/customer/')           ||
        
        path.startsWith('/feed_balance/')       ||
        path.startsWith('/feed_balance_all/')   ||
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
                const cachedShell = await caches.match('/app');
                
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
            try {
                const cache = await caches.open(CACHE_NAME);
                const cachedResponse = await cache.match(event.request);
                
                // Return cached response immediately if available
                if (cachedResponse) {
                    // But update cache in background (don't await, don't crash)
                    fetch(event.request).then(async (networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            await cache.put(event.request, networkResponse.clone());
                        }
                    }).catch((err) => {
                        // Silently fail - we have cache
                        console.log('Background update failed:', err.message);
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
                    console.log('Failed to fetch:', event.request.url);
                    // Return a simple error response instead of crashing
                    return new Response('Resource not available offline', { 
                        status: 404,
                        headers: { 'Content-Type': 'text/plain' }
                    });
                }
            } catch (error) {
                // Catch any unexpected errors in the whole handler
                console.error('Service worker fetch error:', error);
                console.error('Failed URL:', event.request.url);
                
                // Try network as fallback
                try {
                    return await fetch(event.request);
                } catch (e) {
                    return new Response('Service worker error', { status: 500 });
                }
            }
        })()
    );
});



// Activate event - clean old caches AND check version
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating... v5');
    event.waitUntil(
        (async () => {
            // 1. Delete old caches
            const cacheNames = await caches.keys();
            await Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== SHELL_CACHE) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
            
            // 2. Ensure shell cache has minimum files
            const shellCache = await caches.open(SHELL_CACHE);
            const hasIndex = await shellCache.match('/app');
            if (!hasIndex) {
                console.log('Re-adding shell files to cache');
                await shellCache.addAll(SHELL_FILES);
            }

            
            // Fetch fresh /app and update cache
            try {
                console.log('Attempting to fetch fresh /app...');
                const freshApp = await fetch('/app', { 
                    cache: 'no-store',
                    credentials: 'include'  // Important: send cookies
                });
                console.log('Fetch /app response status:', freshApp.status);
                console.log('Fetch /app response ok:', freshApp.ok);
                
                if (freshApp.ok) {
                    // Get the HTML to check version
                    const html = await freshApp.text();
                    const versionMatch = html.match(/APP_VERSION = '([^']+)'/);
                    console.log('Fresh /app version:', versionMatch ? versionMatch[1] : 'not found');
                    
                    // Put it back (need to recreate response because text() consumed it)
                    await shellCache.put('/app', new Response(html, {
                        headers: freshApp.headers
                    }));
                    console.log('✅ Updated /app cache to latest version');
                } else {
                    console.log('Fetch /app failed with status:', freshApp.status);
                }
            } catch (e) {
                console.log('Could not refresh /app cache:', e);
                console.log('Error details:', e.message);
            }

                    
            // 3. Clean old bundles and versioned files from main cache
            try {
                const manifestRes = await fetch('/static/js/manifest.json');
                const mainCache = await caches.open(CACHE_NAME);
                const keys = await mainCache.keys();
                
                // Get current bundle names from manifest if available
                let currentBundles = [];
                if (manifestRes.ok) {
                    const manifest = await manifestRes.json();
                    currentBundles = [manifest.core, manifest.login];
                    console.log('📦 Current bundles:', currentBundles);
                }
                
                for (const key of keys) {
                    const url = key.url;
                    let shouldDelete = false;
                    
                    // Delete old bundles not in current manifest
                    if (url.includes('/static/js/bundle.') && currentBundles.length > 0) {
                        if (!currentBundles.some(bundle => url.includes(bundle))) {
                            shouldDelete = true;
                            console.log('Deleting old bundle:', url);
                        }
                    }
                    
                    // Delete any cached file that has a query parameter (?v= or ?t=)
                    if (url.includes('?v=') || url.includes('?t=')) {
                        shouldDelete = true;
                        console.log('Deleting versioned file:', url);
                    }
                    
                    if (shouldDelete) {
                        await mainCache.delete(key);
                    }
                }
            } catch (e) {
                console.log('Could not clean old bundles/versioned files:', e);
            }
            
            // 4. Claim clients immediately
            await self.clients.claim();
        })()
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


