function urlBase64ToUint8Array(base64String) {
    var padding = '='.repeat((4 - base64String.length % 4) % 4);
    var base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    var rawData = atob(base64);
    var outputArray = new Uint8Array(rawData.length);

    for (var i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

 self.addEventListener("activate", async (e)=>{
  const subscription=await self.registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array("Public_Key") // Add public key
  })
  console.log(subscription);
  const response = await fetch('http://127.0.0.1:8000/management/save-subscription/', {
     method: 'POST',
     headers: {
         'Content-Type': 'application/json'
     },
     body: JSON.stringify(subscription)
 });
 
 console.log('Subscription saved:', response.ok);
 });


 self.addEventListener('push', function(event) {
    // const data = event.data;
    // console.log(event)
    self.registration.showNotification("You've got a new notification! Tap to view the details");
});

// Handle notification click events
self.addEventListener('notificationclick', function(event) {
    event.notification.close(); // Close the notification when clicked

    // Check if there is a URL in the notification data
    const url = "http://127.0.0.1:8000/management/notifications/";

    if (url) {
        // Open the URL in a new tab/window
        event.waitUntil(
            clients.openWindow(url)
        );
    }
});
