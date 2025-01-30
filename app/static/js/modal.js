import { setLoadingState } from "./helper.module.js";

var notyf = new Notyf();

// categoryForm
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
  document.getElementById("updatecategoryForm").querySelector("#name").value =
    name;

  var updateModal = new bootstrap.Modal(
    document.getElementById("updateCategory")
  );
  updateModal.show();
}

function deleteCategory(id) {
  if (confirm("Are you sure you want to delete this category?")) {
    fetch("/admin/category", {
      method: "DELETE",
      body: new URLSearchParams({
        id: id,
      }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Category deleted successfully!");
          location.reload();
        } else {
          alert("Error deleting category.");
        }
      });
  }
}
// categoryForm END





// dom calling
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit-category").forEach((button) => {
      button.addEventListener("click", function () {
        const id = this.dataset.id;
        const name = this.dataset.name;
        showUpdateForm(id, name);
      });
    });

    document.querySelectorAll(".delete-category").forEach((button) => {
        button.addEventListener("click", function () {
          const id = this.dataset.id;
          deleteCategory(id);
        });
      });
  });