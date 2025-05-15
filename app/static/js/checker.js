import { alert, countdownAlert } from "./helper.module.js";

const COOLDOWN_MINUTES = 10;

function shouldShowAlert() {
  const lastShown = localStorage.getItem("lastPendingAlertTime");
  if (!lastShown) return true;

  const lastTime = new Date(parseInt(lastShown, 10));
  const now = new Date();
  const diffMinutes = (now - lastTime) / (1000 * 60);
  return diffMinutes >= COOLDOWN_MINUTES;
}

function updateLastShownTime() {
  localStorage.setItem("lastPendingAlertTime", Date.now().toString());
}

async function showCheckerUpdate() {
  try {
    if (!shouldShowAlert()) return;

    const response = await fetch(`/admin/pending_checker`, { method: "GET" });

    if (!response.ok) {
      throw new Error("Failed to fetch borrowing update.");
    }

    const data = await response.json();
    if (data.pending_count >= 1) {
      countdownAlert(`Borrowing pending: ${data.pending_count} request(s) need attention.`, 5, "center", "info");
      updateLastShownTime();  
    }
  } catch (error) {
    console.error("Error:", error);
    alert("error", "top", error);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  showCheckerUpdate();
});
