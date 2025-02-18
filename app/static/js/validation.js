import {
  setLoadingState, alert, showConfirmationDialog
} from "./helper.module.js";


const registerForm = document.querySelector("#registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const registerButton = document.querySelector("#registerButton");
    setLoadingState(registerButton, true);

    try {
      const response = await fetch("/register", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        alert("success", "top", data.message);

        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(registerButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("success", "top", error);
      setLoadingState(registerButton, false);
    }
  });
}

const loginForm = document.querySelector("#loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const loginButton = document.querySelector("#loginButton");
    setLoadingState(loginButton, true);

    try {
      const response = await fetch("/login", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
  
      if (response.ok) {
        alert("success", "top", data.message);

        setTimeout(() => {
          window.location.href = "/admin/dashboard";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(loginButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
      setLoadingState(loginButton, false);
    }
  });
}

const logout = document.querySelector("#logout");
if (logout) {
  logout.addEventListener("click", async (e) => {
    e.preventDefault(); // Prevent immediate form submission
    showConfirmationDialog(
      "Are you sure you want to log out?",
      "Yes",
      "No",
      async () => {
        try {
          const response = await fetch(`/logout`, {
            method: "POST",
          });
  
          const data = await response.json();
  
          if (!response.ok) {
            throw new Error(data.message || "Failed to delete category.");
          }
  
          alert("success", "top", data.message);
          window.location.href = "/login"
        } catch (error) {
          console.error("Error:", error);
          alert("error", "top", error.message);
        }
      },
      () => {
        
      }
    );

   
  });
}

