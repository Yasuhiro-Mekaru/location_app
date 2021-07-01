const CACHE_NAME = 'v6';

const CACHE_FILES = [
	'/',
	'/static/cache.html'
];


self.addEventListener('install', function(event){
    console.log('Service Worker is installed');

    event.waitUntil(caches.open(CACHE_NAME).then(function(cache){
    	console.log('Service Worker caches');
    	console.log('cache', cache);

    	return cache.addAll(CACHE_FILES);
    }));

    self.skipWaiting();
});

self.addEventListener('activate', function(event){
	console.log('Service Worker is activate');

	event.waitUntil(caches.keys().then(function(keyList){
		return Promise.all(keyList.map(function(key){
			if (key !== CACHE_NAME){
				console.log('Service Worker remove old cache', key);
				return caches.delete(key);
			}
		}));
	}));
	return self.clients.claim();
});

self.addEventListener('fetch', function(event){
	console.log('Service Worker is fetching', event.request.url);
	console.log('event.request.mode', event.request.mode);

	// event.respondWith(caches.match(event.request).then(function(response){
	// 	console.log('response', response);
	// 	fetched = fetch(event.request);
	// 	console.log('fetched', fetched);

	// 	return response || fetched;
	// }));

	event.respondWith(fetch(event.request).catch(() => {
		return caches.open(CACHE_NAME).then((cache) => {
			console.log('cache', cache);
			return cache.match('cache.html');
		});
	}));
});



// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here. Other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/8.3.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.3.2/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
	apiKey: "AIzaSyBg9IYpPXlLv6xsC1NkX-mqc1rFyt29uT8",
	authDomain: "location-app-project-310607.firebaseapp.com",
	projectId: "location-app-project-310607",
	storageBucket: "location-app-project-310607.appspot.com",
	messagingSenderId: "304992216180",
	appId: "1:304992216180:web:0bfadc47213641dd941d21",
	measurementId: "G-LFQK2FP3MP"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();


messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle,
    notificationOptions);
});