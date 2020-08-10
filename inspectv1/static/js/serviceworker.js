var staticCacheName = 'djangopwa-v1.1';

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function (cache) {
      return cache.addAll([
        '/',
      ]);
    })
  );
});

const cachNameToKeep = 'myCache';

//Deletion should only occur at the activate event
self.addEventListener('activate', event => {
  var cacheKeeplist = [cachNameToKeep];
  //console.log(event.request.url);
  if (event.request.url.indexOf('/accounts/') === -1) {
    event.waitUntil(
      caches.keys().then(keyList => {
        return Promise.all(keyList.map(key => {
          console.log('delete' + key);
          if (cacheKeeplist.indexOf(key) === -1) {
            return caches.delete(key);
          }
        }));
      })
        .then(self.clients.claim())); //this line is important in some contexts
  }
});



self.addEventListener('fetch', function (event) {

  if (event.request.url.match('^.*(\/accounts\/).*$')) {
    return false;
  }
  // OR
  if (event.request.url.match('^.*(\/listsites\/).*$')) {
    return false;
  }
  if (event.request.url.match('^.*(\/dashboard\/).*$')) {
    return false;
  }
  if (event.request.url.indexOf('/accounts/') !== -1) {
    return false;
  }

  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        if (response) {
          return response;
        }
        var fetchRequest = event.request.clone();
        return fetch(fetchRequest).then(
          function (response) {
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            var responseToCache = response.clone();
            caches.open(staticCacheName)
              .then(function (cache) {
                cache.put(event.request, responseToCache);
              });
            return response;
          }
        );
      })
  );
});

