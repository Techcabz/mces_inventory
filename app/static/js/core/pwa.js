let serviceWorkerRegistration = null;

window.addEventListener("load", function () {
  if (!("serviceWorker" in navigator)) {
    return;
  }
  navigator.serviceWorker
    .register("./csw.js")
    .catch(function (error) {
      console.error("Unable to register service worker.", error);
    });
});
