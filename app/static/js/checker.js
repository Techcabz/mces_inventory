import { alert, countdownAlert } from "./helper.module.js";

async function showCheckerUpdate() {
  try {
    const response = await fetch(`/admin/pending_checker`, { method: "GET" });

    if (!response.ok) {
      throw new Error("Failed to fetch borrowing update.");
    }
    const data = await response.json();
    if (data.pending_count >= 1) {
      countdownAlert(`Borrowing pending: ${data.pending_count} request(s) need attention.`, 10, "center", "info");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("error", "top", error);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  showCheckerUpdate();
});
