export function setLoadingState(button, isLoading) {
  if (isLoading) {
    const loadingText = button.getAttribute("data-loading-text");
    button.setAttribute("data-original-text", button.textContent);
    button.textContent = loadingText;
    button.disabled = true;
    button.classList.add("opacity-50", "cursor-not-allowed");
  } else {
    button.textContent = button.getAttribute("data-original-text");
    button.removeAttribute("data-original-text");
    button.disabled = false;
    button.classList.remove("opacity-50", "cursor-not-allowed");
  }
}



export function alert(icon, position, title) {
  const Toast = Swal.mixin({
    toast: true,
    position: position,
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });

  Toast.fire({
    icon: icon,
    title: title,
  });
}

export function showConfirmationDialog(title, confirmText, denyText, onConfirm, onDeny) {
  Swal.fire({
    title: title,
    showCancelButton: true,
    confirmButtonText: confirmText,
    denyButtonText: denyText,
  }).then((result) => {
    if (result.isConfirmed) {
      if (typeof onConfirm === "function") onConfirm();
    } else if (result.isDenied) {
      if (typeof onDeny === "function") onDeny();
    }
  });
}

export function countdownAlert(message, seconds = 3, position = "top-end") {
  let timerInterval;

  Swal.fire({
    title: message,
    html: "This will close in <b></b> seconds.",
    toast: true,
    position: position,
    timer: seconds * 1000,
    timerProgressBar: true,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
      const timerEl = Swal.getPopup().querySelector("b");
      timerInterval = setInterval(() => {
        timerEl.textContent = Math.ceil(Swal.getTimerLeft() / 1000);
      }, 100);
    },
    willClose: () => {
      clearInterval(timerInterval);
    }
  }).then((result) => {
    if (result.dismiss === Swal.DismissReason.timer) {
      console.log("⏳ Countdown alert auto-closed.");
    }
  });
}

