const CACHE = 'tap-rush-worlds-1';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil((async () => { for (const key of await caches.keys()) if (key.startsWith('tap-rush-') && key !== CACHE) await caches.delete(key); await self.clients.claim(); })()));
self.addEventListener('fetch', event => {
 if (event.request.method !== 'GET' || !event.request.url.startsWith(self.registration.scope)) return;
 event.respondWith(fetch(event.request).then(response => { if(response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(event.request,copy));}return response; }).catch(async()=>{const hit=await caches.match(event.request);if(hit)return hit;if(event.request.mode==='navigate'){const home=await caches.match(self.registration.scope);if(home)return home;}return Response.error();}));
});
