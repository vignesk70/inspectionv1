var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/inspect'
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
      if ((requestUrl.pathname === '/')) {
        event.respondWith(caches.match('/inspect'));
        return;
      }
    }
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
});

self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open(staticCacheName).then(function(cache) {
        return cache.addAll([
          '/inspection'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(event) {
    var requestUrl = new URL(event.request.url);
      if (requestUrl.origin === location.origin) {
        if ((requestUrl.pathname === '/')) {
          event.respondWith(caches.match('/inspection'));
          return;
        }
      }
      event.respondWith(
        caches.match(event.request).then(function(response) {
          return response || fetch(event.request);
        })
      );
  });

  self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open(staticCacheName).then(function(cache) {
        return cache.addAll([
          '/listsites'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(event) {
    var requestUrl = new URL(event.request.url);
      if (requestUrl.origin === location.origin) {
        if ((requestUrl.pathname === '/')) {
          event.respondWith(caches.match('/listsites'));
          return;
        }
      }
      event.respondWith(
        caches.match(event.request).then(function(response) {
          return response || fetch(event.request);
        })
      );
  });