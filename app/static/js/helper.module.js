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
  