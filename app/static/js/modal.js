import {
  setLoadingState,
  alert,
  showConfirmationDialog,
} from "./helper.module.js";

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

      if (response.ok) {
        alert("success", "top", data.message);

        setTimeout(() => {
          window.location.href = "/admin/category";
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(categoryButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
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

      if (response.ok) {
        alert("success", "top", data.message);

        setTimeout(() => {
          window.location.href = "/admin/category";
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(categoryButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
      setLoadingState(categoryButton, false);
    }
  });
}

function showUpdateForm(id, name) {
  document.getElementById("updatecategoryForm").querySelector("#cu_id").value = id;
  document.getElementById("updatecategoryForm").querySelector("#cu_name").value =
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
          alert("sucess", "top", "Category deleted successfully!");
          location.reload();
        } else {
          alert("warning", "top", "Error deleting category.");
        }
      });
  }
}

function deleteUser(id) {
  Swal.fire({
    title: "Are you sure?",
    text: "Deleting this user will also remove all related data (e.g., borrowing, reports). This cannot be undone.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "Cancel",
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(`/admin/users/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            alert("success", "top", "User deleted successfully!");
            location.reload();
          } else {
            alert("warning", "top", "Error deleting user.");
          }
        });
    }
  });
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

      if (response.ok) {
        alert("success", "top", data.message);

        setTimeout(() => {
          window.location.href = "/admin/inventory";
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
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
      if (response.ok) {
        alert("success", "top", data.message);

        setTimeout(() => {
          window.location.href = "/admin/inventory";
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
      setLoadingState(button, false);
    }
  });
}
async function showInvUpdateForm(id) {
  try {
    const response = await fetch(`/admin/inventory/${id}`, { method: "GET" });

    if (!response.ok) {
      throw new Error("Failed to fetch inventory item.");
    }

    const data = await response.json();
    const form = document.getElementById("updateInventoryForm");
    form.querySelector("#u_title").value = data.title || "";
    form.querySelector("#u_category_id").value = data.category_id || "";
    form.querySelector("#u_property_no").value = data.property_no || "";
    form.querySelector("#u_date_acquired").value = data.date_acquired || "";
    form.querySelector("#u_cost").value = data.cost || "";
    form.querySelector("#u_fund_source").value = data.fund_source || "";
    form.querySelector("#u_officer").value = data.officer || "";
    form.querySelector("#u_school").value = data.school || "";
    form.querySelector("#u_qty").value = data.quantity || "";
    form.querySelector("#u_unit").value = data.unit || "";
    form.querySelector("#u_id").value = data.id || "";
    form.querySelector("#u_inv_tag").value = data.inv_tag || "";

    var updateModal = new bootstrap.Modal(
      document.getElementById("updateInventory")
    );
    updateModal.show();
  } catch (error) {
    console.error("Error:", error);
    alert("error", "top", error);
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
          alert("success", "top", "Deleted successfully");
          location.reload();
        } else {
          alert("error", "top", "Error deleting inventory.");
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
    setLoadingState(button, true);
    try {
      const response = await fetch("/users/borrow_item", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          location.reload();
        }, 2000);
        setLoadingState(button, false);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
      setLoadingState(button, false);
    }
  });
}

const cartForm = document.querySelector("#cartForm");
if (cartForm) {
  cartForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const button = document.querySelector("#borrowingButton");
    const uuid = cartForm.querySelector("#inventory_uuid").value;
    setLoadingState(button, true);

    try {
      const response = await fetch(`/users/cart/${uuid}`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        const uuid = data.inventory_uuid;
        setTimeout(() => {
          window.location.href = `/users/item/${uuid}`;
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", error);
      setLoadingState(button, false);
    }
  });
}

const profileForm = document.querySelector("#profileForm");
if (profileForm) {
  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileForm.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/users/update_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const profileFormUserAdmin = document.querySelector("#profileFormUserAdmin");
if (profileFormUserAdmin) {
  profileFormUserAdmin.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileFormUserAdmin.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/update_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const profileFormUserAdminAdd = document.querySelector(
  "#profileFormUserAdminAdd"
);
if (profileFormUserAdminAdd) {
  profileFormUserAdminAdd.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileFormUserAdminAdd.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/add_admin_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const profileFormUpdateAdmin = document.querySelector(
  "#profileFormUpdateAdmin"
);
if (profileFormUpdateAdmin) {
  profileFormUpdateAdmin.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileFormUpdateAdmin.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/update_admin_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const profileUpdateAdmin = document.querySelector("#profileUpdateAdmin");
if (profileUpdateAdmin) {
  profileUpdateAdmin.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileUpdateAdmin.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/update_admin_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

function showUpdateUser(id, name) {
  fetch(`/admin/get_profile_admin/${id}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("profile_user_id").value = data.user.id;

        document.getElementById("ausername").value =
          data.user.username || "N/A";
        document.getElementById("afname").value = data.user.firstname || "N/A";
        document.getElementById("amname").value = data.user.middlename || "N/A";
        document.getElementById("alname").value = data.user.lastname || "N/A";
        document.getElementById("aemail").value = data.user.email || "N/A";
       
        document.getElementById("aaddress").value = data.user.address || "N/A";
        document.getElementById("acontact").value = data.user.contact || "N/A";

        let sexSelect = document.getElementById("asex");
        if (sexSelect) {
          for (let option of sexSelect.options) {
            if (option.value.toLowerCase() === data.user.sex.toLowerCase()) {
              option.selected = true;
              break;
            }
          }
        } else {
          console.error("Element with ID 'asex' not found.");
        }

        var updateModal = new bootstrap.Modal(
          document.getElementById("profileUserAdminModal")
        );
        updateModal.show();
      } else {
        alert("warning", "top", "Failed to load profile data.");
      }
    })
    .catch((error) => {
      console.error("Error fetching profile data:", error);
      alert("warning", "top", "Error fetching profile data.");
    });
}

function showUpdateAdmin(id, name) {
  fetch(`/admin/get_profile_admin/${id}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("aueprofile_user_id").value = data.user.id;
        document.getElementById("auesername").value =
          data.user.username || "N/A";

        var updateModal = new bootstrap.Modal(
          document.getElementById("profileUAdminEditModal")
        );
        updateModal.show();
      } else {
        alert("warning", "top", "Failed to load profile data.");
      }
    })
    .catch((error) => {
      console.error("Error fetching profile data:", error);
      alert("warning", "top", "Error fetching profile data.");
    });
}

// dom calling
document.addEventListener("DOMContentLoaded", function () {
  const searchBar = document.getElementById("search-bar");
  const categoriesContainer = document.getElementById("default-card");
  const searchResultsContainer = document.getElementById(
    "search-results-container"
  );
  const searchResultsList = document.getElementById("search-results-list");
  let currentQuery = "";
  if (searchBar) {
    searchBar.addEventListener("input", async function () {
      const query = searchBar.value.trim();

      currentQuery = query;

      if (query.length > 0) {
        categoriesContainer.style.display = "none";
        searchResultsContainer.style.display = "block";

        try {
          // Fetch search results
          const response = await fetch(`/search-items?q=${query}`);
          const data = await response.json();

          if (currentQuery === query) {
            // Clear previous results
            searchResultsList.innerHTML = "";

            if (data.length > 0) {
              data.forEach((item) => {
                searchResultsList.innerHTML += `
                  <div class="col">
                    <a href="/users/item/${item.uuid}">
                      <div class="card">
                        <img class="card-img-top" src="${
                          item.image_url
                        }" alt="${item.title}">
                        <div class="card-body">
                          <span class="card-title d-flex justify-content-between">
                            <strong>${item.title}</strong>
                          </span>
                          <div class="d-flex justify-content-between align-items-center">
                            <p class="card-text m-0">Qty: <strong>${
                              item.quantity
                            }</strong></p>
                            <span class="badge ${getStatusClass(
                              item.status
                            )}">${item.status}</span>
                          </div>
                        </div>
                      </div>
                    </a>
                  </div>
                `;
              });
            } else {
              searchResultsList.innerHTML = "<p>No items found</p>";
            }
          }
        } catch (error) {
          console.error("Error fetching search results:", error);
          searchResultsList.innerHTML =
            "<p>Error loading results. Please try again.</p>";
        }
      } else {
        categoriesContainer.style.display = "block";
        searchResultsContainer.style.display = "none";
        searchResultsList.innerHTML = "";
      }
    });
  }

  function getStatusClass(status) {
    switch (status) {
      case "Available":
        return "bg-success";
      case "Borrowed":
        return "bg-primary";
      case "Reserved":
        return "bg-warning";
      case "Damaged":
        return "bg-danger";
      default:
        return "bg-secondary";
    }
  }

  const cartTable = document.getElementById("datatablefix");
  if (cartTable) {
    // Update Quantity
    cartTable.addEventListener("change", function (event) {
      if (event.target.classList.contains("cart-quantity")) {
        let cartId = event.target.dataset.cartId;
        let newQuantity = event.target.value;

        fetch("/users/cart_update", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ cart_id: cartId, quantity: newQuantity }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert("success", "top", "Cart updated successfully!");
              location.reload();
            } else {
              alert("warning", "top", data.message);
              location.reload();
            }
          })
          .catch((error) => console.error("Error updating cart:", error));
      }
    });

    // Remove Item
    cartTable.addEventListener("click", function (event) {
      if (event.target.classList.contains("remove-cart-item")) {
        let cartId = event.target.dataset.cartId;

        fetch("/users/cart_remove", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ cart_id: cartId }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert("success", "top", "Item removed from cart.");
              location.reload(); // Remove row from table
            } else {
              alert("danger", "top", data.message);
            }
          })
          .catch((error) => console.error("Error removing cart item:", error));
      }
    });
  }

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

  document.querySelectorAll(".edit-profile-user").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      const name = this.dataset.name;
      showUpdateUser(id, name);
    });
  });

  document.querySelectorAll(".edit-profile-admin").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      const name = this.dataset.name;
      showUpdateAdmin(id, name);
    });
  });

  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("bUserA")) {
      let userID = event.target.getAttribute("data-user-id");

      showConfirmationDialog(
        "Are you sure you want to approved this user?",
        "Yes",
        "No",
        async () => {
          try {
            const response = await fetch(`/admin/users/approved/${userID}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ status: 1 }),
            });

            const data = await response.json();

            if (!response.ok) {
              throw new Error(data.message);
            }

            alert("success", "top", data.message);
            window.location.reload();
          } catch (error) {
            console.error("Error:", error);
            alert("error", "top", error.message);
          }
        },
        () => {}
      );
    }

    if (event.target.classList.contains("bUserD")) {
      let userID = event.target.getAttribute("data-user-id");

      showConfirmationDialog(
        "Are you sure you want to disapprove this user? This will delete the user from our records. Do you want to continue?",
        "Yes",
        "No",
        async () => {
          try {
            const response = await fetch(`/admin/users/disapproved/${userID}`, {
              method: "DELETE",
              headers: { "Content-Type": "application/json" },
            });

            const data = await response.json();

            if (!response.ok) {
              throw new Error(data.message);
            }

            alert("success", "top", data.message);
            window.location.reload();
          } catch (error) {
            console.error("Error:", error);
            alert("error", "top", error.message);
          }
        },
        () => {}
      );
    }

    if (event.target.classList.contains("bDone")) {
      let borrowingId = event.target.getAttribute("data-borrowing-id");

      Swal.fire({
        title: "Mark this borrowing as done?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonText: "No",
        confirmButtonText: "Yes!",
        width: "300px",
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(`/admin/borrowing/done/${borrowingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "completed" }),
          })
            .then((response) => response.json())
            .then((data) => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch((error) => console.error("Error:", error));
        }
      });
    }

    if (event.target.classList.contains("bApproved")) {
      let borrowingId = event.target.getAttribute("data-borrowing-id");

      Swal.fire({
        title: "Approve this borrowing?",
        icon: "question",
        showCancelButton: false,
        confirmButtonColor: "#3085d6",
        confirmButtonText: "Yes!",
        width: "300px",
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(`/admin/borrowing/status/${borrowingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "approved" }),
          })
            .then((response) => response.json())
            .then((data) => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch((error) => console.error("Error:", error));
        }
      });
    }

    if (event.target.classList.contains("bDisapproved")) {
      let borrowingId = event.target.getAttribute("data-borrowing-id");

      Swal.fire({
        title: "Cancel Request",
        text: "Please provide a reason:",
        input: "textarea",
        inputPlaceholder: "Enter your reason here...",
        showCancelButton: true,
        confirmButtonText: "Submit",
        cancelButtonText: "Cancel (No Reason)",
      }).then((result) => {
        if (result.isConfirmed) {
          let reason = result.value;
          fetch(`/admin/borrowing/cancel_reason/${borrowingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "cancelled", reason: reason }),
          })
            .then((response) => response.json())
            .then((data) => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch((error) => console.error("Error:", error));
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          // Only trigger cancel if the cancel button is clicked

          fetch(`/admin/borrowing/cancel/${borrowingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "cancelled" }),
          })
            .then((response) => response.json())
            .then((data) => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch((error) => console.error("Error:", error));
        }
      });
    }

    if (event.target.classList.contains("bCancel")) {
      let borrowingId = event.target.getAttribute("data-borrowing-id");

      Swal.fire({
        title: "Confirm Cancellation",
        text: "  Are you sure you want to cancel this borrowing? This action cannot be undone.",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(`/users/borrowed/status/${borrowingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "cancelled" }),
          })
            .then((response) => response.json())
            .then((data) => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch((error) => console.error("Error:", error));
        }
      });
    }
  });

  document.querySelectorAll(".delete-admin").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      deleteUser(id);
    });
  });

  document.querySelectorAll(".delete-user").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      deleteUser(id);
    });
  });
});
