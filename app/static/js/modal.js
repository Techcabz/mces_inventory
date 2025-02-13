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

const inventoryForm = document.querySelector("#inventoryForm");
if (inventoryForm) {
  inventoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const button = document.querySelector("#inventoryButton");
    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/inventory", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/admin/inventory";
        });

        setTimeout(() => {
          window.location.href = "/admin/inventory";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(button, false);
    }
  });
}
const updateInventoryForm = document.querySelector("#updateInventoryForm");
if (updateInventoryForm) {
  updateInventoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const button = document.querySelector("#inventoryButtonUpdate");
    setLoadingState(button, true);
    const id = formData.get("id");
    try {
      const response = await fetch(`/admin/inventory/${id}`, {
        method: "PUT",
        body: formData,
      });

      const data = await response.json();
      console.log(formData.get("id"));
      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/admin/inventory";
        });

        setTimeout(() => {
          window.location.href = "/admin/inventory";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(button, false);
    }
  });
}
async function showInvUpdateForm(id) {
  document.getElementById("updatecategoryForm").querySelector("#id").value = id;

  try {
    const response = await fetch(`/admin/inventory/${id}`, { method: "GET" });

    if (!response.ok) {
      throw new Error("Failed to fetch inventory item.");
    }

    const data = await response.json();
    const form = document.getElementById("updateInventoryForm");

    form.querySelector("#title").value = data.title || "";
    form.querySelector("#category_id").value = data.category_id || "";
    form.querySelector("#property_no").value = data.property_no || "";
    form.querySelector("#date_acquired").value = data.date_acquired || "";
    form.querySelector("#cost").value = data.cost || "";
    form.querySelector("#fund_source").value = data.fund_source || "";
    form.querySelector("#officer").value = data.officer || "";
    form.querySelector("#school").value = data.school || "";
    form.querySelector("#qty").value = data.quantity || "";
    form.querySelector("#unit").value = data.unit || "";
    form.querySelector("#id").value = data.id || "";

    var updateModal = new bootstrap.Modal(
      document.getElementById("updateInventory")
    );
    updateModal.show();
  } catch (error) {
    console.error("Error:", error);
    notyf.error("An unexpected error occurred.");
  }
}
function deleteInventory(id) {
  if (confirm("Are you sure you want to delete this inventory?")) {
    fetch(`/admin/inventory/${id}`, {
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
          alert("Inventory deleted successfully!");
          location.reload();
        } else {
          alert("Error deleting inventory.");
        }
      });
  }
}


const borrowForm = document.querySelector("#borrowForm");
if (borrowForm) {
  borrowForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const button = document.querySelector("#borrowingButton");
    const uuid = borrowForm.querySelector("#inventory_uuid").value;
    setLoadingState(button, true);

    console.log(uuid)
    try {
      const response = await fetch(`/users/item/${uuid}`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        const notification = notyf.success(data.message);
        setTimeout(() => {
          window.location.href = "/users/history_item";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(button, false);
    }
  });
}

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

  document.querySelectorAll(".edit-inventory").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      // const name = this.dataset.name;
      showInvUpdateForm(id);
    });
  });

  document.querySelectorAll(".delete-inventory").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      deleteInventory(id);
    });
  });
});
