import { setLoadingState, alert, showConfirmationDialog } from "./helper.module.js";

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
      console.log(data);
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
          alert("sucess", "top", "Category deleted successfully!");
          location.reload();
        } else {
          alert("warning", "top", "Error deleting category.");
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
      console.log(formData.get("id"));
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
    const uuid = borrowForm.querySelector("#inventory_uuid").value;
    setLoadingState(button, true);

    try {
      const response = await fetch(`/users/item/${uuid}`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        const borrowingUuid = data.borrowing_uuid;
        setTimeout(() => {
          window.location.href = `/users/borrowed/item/${borrowingUuid}`;
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
                        <img class="card-img-top" src="${item.image_url}" alt="${item.title}">
                        <div class="card-body">
                          <span class="card-title d-flex justify-content-between">
                            <strong>${item.title}</strong>
                          </span>
                          <div class="d-flex justify-content-between align-items-center">
                            <p class="card-text m-0">Qty: <strong>${item.quantity}</strong></p>
                            <span class="badge ${getStatusClass(item.status)}">${item.status}</span>
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
          searchResultsList.innerHTML = "<p>Error loading results. Please try again.</p>";
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
        () => {

        }
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
              headers: { "Content-Type": "application/json" }
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
        () => {

        }
      );
    }

    if (event.target.classList.contains("bDone")) {
      let borrowingId = event.target.getAttribute("data-borrowing-id");
      let inventoryId = event.target.getAttribute("data-inventory-id");
      let inventoryQty = event.target.getAttribute("data-inventory-qty");

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
            body: JSON.stringify({ status: "done", inventory_id: inventoryId, quantity: inventoryQty }),
          })
            .then(response => response.json())
            .then(data => {
              console.log(data.message);
              alert("success", "top", data.message);
              location.reload();
            })
            .catch(error => console.error("Error:", error));
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
            .then(response => response.json())
            .then(data => {
              console.log(data.message);
              alert("success", "top", data.message);
              location.reload();
            })
            .catch(error => console.error("Error:", error));
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
            .then(response => response.json())
            .then(data => {
              console.log(data.message);
              alert("success", "top", data.message);
              location.reload();
            })
            .catch(error => console.error("Error:", error));
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          // Only trigger cancel if the cancel button is clicked

          fetch(`/admin/borrowing/status/${borrowingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "cancelled" }),
          })
            .then(response => response.json())
            .then(data => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch(error => console.error("Error:", error));
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
            .then(response => response.json())
            .then(data => {
              alert("success", "top", data.message);
              location.reload();
            })
            .catch(error => console.error("Error:", error));
        }
      });
    }
  });


});
