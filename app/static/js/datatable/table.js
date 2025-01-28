$(document).ready(function () {
  var protocol = window.location.protocol;
  var hostname = window.location.hostname;
  var firstPath = window.location.pathname.split("/")[1];
  var fullUrl = protocol + "//" + hostname + "/" + firstPath;

  var table = $("#datatable").DataTable({
    dom: "l<br>Bfrtip",
    buttons: [
      {
        extend: "print",
        text: "Print",
        autoPrint: true,
        exportOptions: {
          columns: ":visible",
          rows: function (idx, data, node) {
            var dt = new $.fn.dataTable.Api("#example");
            var selected = dt.rows({ selected: true }).indexes().toArray();
            if (selected.length === 0 || $.inArray(idx, selected) !== -1) {
              return true;
            } else {
              return false;
            }
          },
        },

        customize: function (win) {
          $(win.document.body)
            .find("table")
            .addClass("display")
            .css("font-size", "9px");
          $(win.document.body)
            .find("tr:nth-child(odd) td")
            .each(function (index) {
              $(this).css("background-color", "#D0D0D0");
            });
          $(win.document.body).find("h1").css("text-align", "center");
        },
      },

      "excel",
      "pdf",
      "colvis",
    ],
    responsive: {
      details: true,
      breakpoints: [
        { name: "desktop", width: Infinity },
        { name: "tablet", width: 1024 },
        { name: "fablet", width: 768 },
        { name: "phone", width: 480 },
      ],
    },
    language: {
      paginate: {
        first: "First",
        previous: "Previous",
        next: "Next",
        last: "Last",
      },
    },
    select: true,
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50, 100],
    columnDefs: [{ orderable: false, targets: "_all" }],
  });

  $("#datatable tfoot th").each(function (i) {
    if ($(this).text() !== "") {
      var isStatusColumn = $(this).text() == "Status" ? true : false;
      var select = $('<select><option value=""></option></select>')
        .appendTo($(this).empty())
        .on("change", function () {
          var val = $(this).val();

          table
            .column(i)
            .search(val ? "^" + $(this).val() + "$" : val, true, false)
            .draw();
        });

      // Get the Status values a specific way since the status is a anchor/image
      if (isStatusColumn) {
        var statusItems = [];

        /* ### IS THERE A BETTER/SIMPLER WAY TO GET A UNIQUE ARRAY OF <TD> data-filter ATTRIBUTES? ### */
        table
          .column(i)
          .nodes()
          .to$()
          .each(function (d, j) {
            var thisStatus = $(j).attr("data-filter");
            if ($.inArray(thisStatus, statusItems) === -1)
              statusItems.push(thisStatus);
          });

        statusItems.sort();

        $.each(statusItems, function (i, item) {
          select.append('<option value="' + item + '">' + item + "</option>");
        });
      }
      // All other non-Status columns (like the example)
      else {
        table
          .column(i)
          .data()
          .unique()
          .sort()
          .each(function (d, j) {
            select.append('<option value="' + d + '">' + d + "</option>");
          });
      }
    }
  });

  var personnelTable = $("#personnelTable").DataTable({
    searching: false, // Disable search bar
    lengthChange: false, // Disable show entries
    info: false, // Disable showing information about the table
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50, 100],
  });

  $("#personnelTable tbody").on("click", "tr", function () {
    var data = personnelTable.row(this).data();
    var rowId = data[1];

    let fdata = new FormData();
    fdata.append("get_personnel", "item");
    fdata.append("patient_id", rowId);

    let personnelForm = document.getElementById("personnelForm");

    const path = "../ajax/admin/get.php";
    fetch(path, {
      method: "POST",
      body: fdata,
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        data = JSON.parse(data);
     
        personnelForm["patient_pass_id"].value = data.patient_id;
        personnelForm["username"].value = data.username;
        personnelForm["lname"].value = data.patient_lname;
        personnelForm["fname"].value = data.patient_fname;
        personnelForm["mname"].value = data.patient_mname;
        personnelForm["gender"].value = data.patient_gender;
        personnelForm["usertype"].value = data.patient_type;
        personnelForm["cancelPersonnel"].disabled = false;

        personnelForm["save_personnel_action"].disabled = true;
        personnelForm["update_personnel_action"].disabled = false;

        if (data.patient_type === "admin") {
          personnelForm["savePersonnel"].disabled = true;
          personnelForm["newPersonnel"].disabled = false;

          personnelForm["username"].disabled = true;
          personnelForm["password"].disabled = true;

          personnelForm["lname"].disabled = true;
          personnelForm["fname"].disabled = true;
          personnelForm["mname"].disabled = true;
          personnelForm["gender"].disabled = true;
          personnelForm["usertype"].disabled = true;

          personnelForm["activate"].disabled = true;
          personnelForm["consultation"].disabled = true;
          personnelForm["reports"].disabled = true;
          personnelForm["rp_consultation"].disabled = true;
          personnelForm["rp_individual"].disabled = true;
          personnelForm["rp_medicine"].disabled = true;
          personnelForm["rp_registered"].disabled = true;
          personnelForm["rp_health"].disabled = true;
          personnelForm["inventory"].disabled = true;
          personnelForm["inv_medicine"].disabled = true;
          personnelForm["inv_equipment"].disabled = true;
          personnelForm["inv_stocks"].disabled = true;
          personnelForm["management"].disabled = true;
          personnelForm["mn_students"].disabled = true;
          personnelForm["mn_faculty"].disabled = true;
          personnelForm["mn_employee"].disabled = true;
          personnelForm["mn_personnel"].disabled = true;
          personnelForm["setup"].disabled = true;
          personnelForm["st_college"].disabled = true;
          personnelForm["st_course"].disabled = true;
          personnelForm["st_office"].disabled = true;
          personnelForm["st_illness"].disabled = true;
          personnelForm["st_nurse"].disabled = true;
          personnelForm["updatePersonnel"].disabled = true;
        } else {
          personnelForm["newPersonnel"].disabled = true;
          personnelForm["updatePersonnel"].disabled = false;
          personnelForm["deletePersonnel"].disabled = false;
          personnelForm["updatePersonnel"].classList.remove("d-none");
          personnelForm["savePersonnel"].classList.add("d-none");

          personnelForm["lname"].disabled = false;
          personnelForm["fname"].disabled = false;
          personnelForm["mname"].disabled = false;
          personnelForm["gender"].disabled = false;
          personnelForm["usertype"].disabled = false;

          personnelForm["activate"].disabled = false;
          personnelForm["consultation"].disabled = false;
          personnelForm["reports"].disabled = false;
          personnelForm["rp_consultation"].disabled = false;
          personnelForm["rp_individual"].disabled = false;
          personnelForm["rp_medicine"].disabled = false;
          personnelForm["rp_registered"].disabled = false;
          personnelForm["rp_health"].disabled = false;
          personnelForm["inventory"].disabled = false;
          personnelForm["inv_medicine"].disabled = false;
          personnelForm["inv_equipment"].disabled = false;
          personnelForm["inv_stocks"].disabled = false;
          personnelForm["management"].disabled = false;
          personnelForm["mn_students"].disabled = false;
          personnelForm["mn_faculty"].disabled = false;
          personnelForm["mn_employee"].disabled = false;
          personnelForm["mn_personnel"].disabled = false;
          personnelForm["setup"].disabled = false;
          personnelForm["st_college"].disabled = false;
          personnelForm["st_course"].disabled = false;
          personnelForm["st_office"].disabled = false;
          personnelForm["st_illness"].disabled = false;
          personnelForm["st_nurse"].disabled = false;
        }

        personnelForm["activate"].checked = data.activation === "1";
        personnelForm["consultation"].checked = data.per_consultation === "1";
        personnelForm["reports"].checked = data.per_reports === "1";
        personnelForm["rp_consultation"].checked =
          data.rep_consultation === "1";
        personnelForm["rp_individual"].checked = data.rep_individual === "1";
        personnelForm["rp_medicine"].checked = data.rep_medicine === "1";
        personnelForm["rp_registered"].checked = data.rep_registered === "1";
        personnelForm["rp_health"].checked = data.rep_health === "1";
        personnelForm["inventory"].checked = data.per_inventory === "1";
        personnelForm["inv_medicine"].checked = data.inv_medicine === "1";
        personnelForm["inv_equipment"].checked = data.inv_equipment === "1";
        personnelForm["inv_stocks"].checked = data.inv_stocks === "1";
        personnelForm["management"].checked = data.per_management === "1";
        personnelForm["mn_students"].checked = data.mn_students === "1";
        personnelForm["mn_faculty"].checked = data.mn_faculty === "1";
        personnelForm["mn_employee"].checked = data.mn_employee === "1";
        personnelForm["mn_personnel"].checked = data.mn_personnel === "1";
        personnelForm["setup"].checked = data.per_setup === "1";
        personnelForm["st_college"].checked = data.st_college === "1";
        personnelForm["st_course"].checked = data.st_course === "1";
        personnelForm["st_office"].checked = data.st_office === "1";
        personnelForm["st_illness"].checked = data.st_illness === "1";
        personnelForm["st_nurse"].checked = data.st_nurse === "1";
      })
      .catch(console.error);
  });

  var consulTable = $("#consulTable").DataTable({
    searching: true, // Disable search bar
    lengthChange: false, // Disable show entries
    info: false, // Disable showing information about the table
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50, 100],
    responsive: {
      details: true,
      breakpoints: [
        { name: "desktop", width: Infinity },
        { name: "tablet", width: 1024 },
        { name: "fablet", width: 768 },
        { name: "phone", width: 480 },
      ],
    },
  });

  var medicineTable = $("#medicineTable").DataTable({
    searching: false, // Disable search bar
    lengthChange: false, // Disable show entries
    info: false, // Disable showing information about the table
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50, 100],
  });

  $("#medicineTable tbody").on("click", "tr", function () {
    var data = medicineTable.row(this).data();
    var rowId = data[0];
    // alert(rowId);
    // deleteRow(rowId);
  });

  var mStockTable = $("#mStockTable").DataTable({
    searching: false, // Disable search bar
    lengthChange: false, // Disable show entries
    info: false, // Disable showing information about the table
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50, 100],
    responsive: {
      details: true,
      breakpoints: [
        { name: "desktop", width: Infinity },
        { name: "tablet", width: 1024 },
        { name: "fablet", width: 768 },
        { name: "phone", width: 480 },
      ],
    },
  });

  $("#mStockTable tbody").on("click", "tr", function () {
    var data = mStockTable.row(this).data();
    var rowId = data[1];

    let fdata = new FormData();
    fdata.append("get_inv_medicine", "item");
    fdata.append("inv_id", rowId);

    let mstocks_form = document.getElementById("mstocks_form");

    const path = "../ajax/admin/get.php";
    fetch(path, {
      method: "POST",
      body: fdata,
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        data = JSON.parse(data);

        document.querySelector('input[name="bdate"]').removeAttribute("min");
        document.querySelector('input[name="edate"]').removeAttribute("min");

        mstocks_form["gname"].value = data.med_brand;
        mstocks_form["bname"].value = data.med_generic;
        mstocks_form["dosage"].value = data.med_dose;
        mstocks_form["type"].value = data.med_type;
        mstocks_form["description"].value = data.med_desc;

        mstocks_form["saveStocks"].disabled = true;
        mstocks_form["updateStocks"].disabled = false;
        mstocks_form["cancelStocks"].disabled = false;

        mstocks_form["bdate"].disabled = false;
        mstocks_form["edate"].disabled = false;
        mstocks_form["tcount"].disabled = false;
        // mstocks_form['tissued'].disabled = false;
        mstocks_form["tavailable"].disabled = true;
        mstocks_form["olevel"].disabled = false;

        mstocks_form["bdate"].value = data.inv_batchdate;
        mstocks_form["edate"].value = data.inv_expiration;
        mstocks_form["tcount"].value = data.inv_totalcount;
        mstocks_form["tissued"].value = data.inv_issued;
        mstocks_form["tavailable"].value = data.inv_remaining;
        mstocks_form["olevel"].value = data.inv_orderlevel;

        if (mstocks_form["saveStocksSubmit"]) {
          mstocks_form.removeChild(mstocks_form["saveStocksSubmit"]);
        }

        var inputElement1 = document.querySelector(
          'input[name="updateStocksSubmit"]'
        );
        var inputElement2 = document.querySelector('input[name="inv_id"]');
        var inputElement3 = document.querySelector('input[name="med_id"]');

        if (!inputElement1) {
          inputElement1 = document.createElement("input");
          inputElement1.type = "hidden";
          inputElement1.name = "updateStocksSubmit";

          mstocks_form.appendChild(inputElement1);
        }

        if (!inputElement2) {
          inputElement2 = document.createElement("input");
          inputElement2.type = "hidden";
          inputElement2.name = "inv_id";
          inputElement2.value = data.inv_id;

          mstocks_form.appendChild(inputElement2);
        }

        if (!inputElement3) {
          inputElement3 = document.createElement("input");
          inputElement3.type = "hidden";
          inputElement3.name = "med_id";
          inputElement3.value = data.inv_med_id;

          mstocks_form.appendChild(inputElement3);
        }
      })
      .catch(console.error);
  });

  var itemCounter = 1;

  $("#addButton").click(function () {
    var medicine = $('select[name="cmedicine"]').val();
    var qty = $('input[name="cqty"]').val();

    let new_m = medicine.split("/");
    let stock_id = new_m[0];
    let stock_qty = new_m[1];

    let fdata = new FormData();
    fdata.append("get_inv_medicine", "item");
    fdata.append("inv_id", stock_id);

    const path = "../ajax/admin/get.php";
    fetch(path, {
      method: "POST",
      body: fdata,
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        data = JSON.parse(data);

        var totalQty = getTotalQuantity(); // Get the total quantity in the table
        var remainingStock = parseInt(stock_qty) - totalQty; // Calculate the remaining stock

        if (qty <= remainingStock) {
          if (medicine && qty) {
            // Check if medicine already exists in the table
            var existingRow = $("#cmedicineTable tbody tr").filter(function () {
              return (
                $(this).find(".medicine").text() ===
                `${data.med_generic}, ${data.med_brand}`
              );
            });

            if (existingRow.length > 0) {
              var existingQty = parseInt(existingRow.find(".qty").text());
              var updatedQty = existingQty + parseInt(qty);
              existingRow.find(".qty").text(updatedQty);
            } else {
              var newRow =
                "<tr>" +
                '<td class="item-number">' +
                itemCounter +
                "</td>" +
                '<td class="medicine">' +
                `${data.med_generic}, ${data.med_brand}` +
                "</td>" +
                '<td class="qty">' +
                qty +
                "</td>" +
                '<td class="inv_id d-none">' +
                data.inv_id +
                "</td>" +
                '<td><button type="button" class="btn btn-sm btn-danger delete-button">Delete</button></td>' +
                "</tr>";

              $("#cmedicineTable tbody").append(newRow);
              itemCounter++;
            }

            //   $('#select-field').val('');
            // $('input[name="cqty"]').val('');
          }
        } else {
          alert(
            "warning",
            "center",
            `The quantity is greater than the remaining stock. Stock Available: ${remainingStock}`
          );
          // alert();
        }
      })
      .catch(console.error);
  });

  // Delete button click event
  $(document).on("click", ".delete-button", function () {
    $(this).closest("tr").remove();
    updateItemNumbers();
  });

  // Function to update item numbers
  function updateItemNumbers() {
    $(".item-number").each(function (index) {
      $(this).text(index + 1);
    });

    itemCounter = $(".item-number").length + 1;
  }

  // Function to calculate the total quantity in the table
  function getTotalQuantity() {
    var totalQty = 0;
    $(".qty").each(function () {
      totalQty += parseInt($(this).text());
    });
    return totalQty;
  }
});
