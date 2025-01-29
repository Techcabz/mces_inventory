var notyf = new Notyf();

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
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/login";
        });

        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(registerButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
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
      console.log(data);

      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/admin/dashboard";
        });

        setTimeout(() => {
          window.location.href = "/admin/dashboard";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(loginButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(loginButton, false);
    }
  });
}

const logout = document.querySelector("#logout");

if (logout) {
  logout.addEventListener("click", async (e) => {
    e.preventDefault(); // Prevent immediate form submission

    const confirmLogout = confirm("Are you sure you want to log out?");

    if (confirmLogout) {
      try {
        const response = await fetch("/logout", { method: "POST" });
        const data = await response.json();
        console.log(data);
        if (response.ok) {
          alert(data.message); // Show a basic alert message
          window.location.href = "/login"; // Redirect after logout
        } else {
          alert("Error: " + data.message);
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred.");
      }
    }
  });
}

const categoryForm = document.querySelector("#categoryForm");
if (categoryForm) {
  categoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const categoryButton = document.querySelector("#categoryButton");
    setLoadingState(categoryButton, true);

    try {
      const response = await fetch("/admin/category", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/admin/category";
        });

        setTimeout(() => {
          window.location.href = "/admin/category";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(categoryButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(categoryButton, false);
    }
  });
}
const updatecategoryForm = document.querySelector("#updatecategoryForm");
if (updatecategoryForm) {
  updatecategoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const categoryButton = document.querySelector("#categoryButtonUpdate");
    setLoadingState(categoryButton, true);

    try {
      const response = await fetch("/admin/category", {
        method: "PUT",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/admin/category";
        });

        setTimeout(() => {
          window.location.href = "/admin/category";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(categoryButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(categoryButton, false);
    }
  });
}
function showUpdateForm(id, name) {
  document.getElementById("updatecategoryForm").querySelector("#id").value = id;
  document.getElementById("updatecategoryForm").querySelector("#name").value = name;
  
  var updateModal = new bootstrap.Modal(document.getElementById('updateCategory'));
  updateModal.show();
}

function deleteCategory(id) {
  if (confirm('Are you sure you want to delete this category?')) {
      fetch('/admin/category', {
          method: 'DELETE',
          body: new URLSearchParams({
              'id': id
          }),
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Category deleted successfully!');
              location.reload();
          } else {
              alert('Error deleting category.');
          }
      });
  }
}

function setLoadingState(button, isLoading) {
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
