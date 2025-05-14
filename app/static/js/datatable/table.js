$(document).ready(function () {
  let tableIds = [
    "datatablefix",
    "datatable",
    "datatable0",
    "datatable1",
    "datatable2",
    "datatable-pending",
    "datatable-approved",
    "datatable-cancelled",
    "datatable-completed",
  ];

  tableIds.forEach((id) => {
    if ($.fn.DataTable.isDataTable(`#${id}`)) {
      $(`#${id}`).DataTable().destroy();
    }

    if (document.getElementById(id)) {
      $(`#${id}`).DataTable({
        dom: id === "datatablefix" ? "lfrtip" : "l<br>Bfrtip",
        buttons:
          id === "datatablefix"
            ? []
            : [
                {
                  extend: "print",
                  text: "Print",
                  autoPrint: true,
                  exportOptions: {
                    columns: ":visible",
                    rows: function (idx, data, node) {
                      var dt = new $.fn.dataTable.Api("#example");
                      var selected = dt
                        .rows({ selected: true })
                        .indexes()
                        .toArray();
                      return (
                        selected.length === 0 || $.inArray(idx, selected) !== -1
                      );
                    },
                  },
                  customize: function (win) {
                    $(win.document.body)
                      .find("table")
                      .addClass("display")
                      .css("font-size", "9px");
                    $(win.document.body)
                      .find("tr:nth-child(odd) td")
                      .each(function () {
                        $(this).css("background-color", "#D0D0D0");
                      });
                    $(win.document.body).find("h1").css("text-align", "center");
                  },
                },
                "excel",
                "pdf",
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
    }
  });

  let tableIDReport = [
    "datatable_report",
    "datatable_report1",
    "datatable_report2",
    "datatable_report3",
  ];

  tableIDReport.forEach(function (id) {
    var table = $("#" + id).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MCES BORROWING REPORT",
          exportOptions: { columns: ":not(.exclude-print)" },
        },
      ],
      searching: true,
      lengthChange: true,
      info: false,
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

    if (id === "datatable_report") {
      var filterType = $("#filter-status");
      var monthFilter = $("#month");
      var weekFilter = $("#week-filter");

      $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        // Make sure this filter only applies to the correct table
        if (settings.nTable.id !== "datatable_report") return true;

        var typefilterValue = filterType.val().toLowerCase();
        var monthFilterValue = monthFilter.val().toLowerCase();
        var weekFilterValue = weekFilter.val();

        var rowData = data; // data is passed directly
        var rowStatus = rowData[5].toLowerCase();
        var rowDate = new Date(rowData[3]);
        var rowMonth = convertDateToMonthName(rowDate).toLowerCase();
        var rowWeek = getWeekNumber(rowDate);

        if (typefilterValue !== "all" && !rowStatus.includes(typefilterValue)) {
          return false;
        }

        if (monthFilterValue !== "all" && rowMonth !== monthFilterValue) {
          return false;
        }

        if (
          weekFilterValue !== "all" &&
          rowWeek !== parseInt(weekFilterValue)
        ) {
          return false;
        }

        return true;
      });

      function convertDateToMonthName(date) {
        return date.toLocaleString("en-US", { month: "long" });
      }

      function getWeekNumber(date) {
        var firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1);
        var dayOfWeek = firstDayOfMonth.getDay();
        var weekNumber = Math.ceil((date.getDate() + dayOfWeek) / 7);
        return weekNumber;
      }

      filterType.on("change", function () {
        table.draw();
      });
      monthFilter.on("change", function () {
        table.draw();
      });
      weekFilter.on("change", function () {
        table.draw();
      });

      table.draw();
    }

    if (id === "datatable_report1") {
      var returnFilter = $("#filter-status-return");
      var returnBorrower1 = $("#filter-borrower1");

      $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        if (settings.nTable.id !== "datatable_report1") return true;
        console.log(data);
        var returnFilterValue = returnFilter.val().toLowerCase().trim();
        var returnBorrower1Value = returnBorrower1.val().toLowerCase().trim();
        var rowReturn = data[5].toLowerCase(); 
        var rowBor = data[3].toLowerCase(); 
        
        if (returnFilterValue) {
          const normalizedReturnStatus = rowReturn.trim().toLowerCase();
          const normalizedFilterValue = returnFilterValue.trim().toLowerCase();

          if (normalizedReturnStatus !== normalizedFilterValue) {
            return false;
          }
        }

        if (returnBorrower1Value && !rowBor.includes(returnBorrower1Value)) {
          return false;
        }

        return true;
      });

      returnFilter.on("change", function () {
        table.draw();
      });

      returnBorrower1.on("change", function () {
        table.draw();
      });

      table.draw();
    }

    if (id === "datatable_report2") {
      var borrowerFilter = $("#filter-borrower");

      $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        if (settings.nTable.id !== "datatable_report2") return true;

        var borrowerValue = borrowerFilter.val().toLowerCase().trim();
        var rowBorrower = data[1].toLowerCase(); // Column 1 = Borrower

        if (borrowerValue && !rowBorrower.includes(borrowerValue)) {
          return false;
        }

        return true;
      });

      borrowerFilter.on("change", function () {
        table.draw();
      });

      table.draw();
    }

    if (id === "datatable_report3") {
      var officerFilter = $("#filter-officer");
      var startDateFilter = $("#filter-start-date");
      var endDateFilter = $("#filter-end-date");

      $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        if (settings.nTable.id !== "datatable_report3") return true;

        var officerValue = officerFilter.val().toLowerCase().trim();
        var startDateValue = startDateFilter.val();
        var endDateValue = endDateFilter.val();

        var rowOfficer = data[4].toLowerCase();
        var rowDate = new Date(data[7]); // Column 7 = Date Acquired

        // Officer match
        if (officerValue && !rowOfficer.includes(officerValue)) {
          return false;
        }

        // Date Acquired range match
        if (startDateValue) {
          var start = new Date(startDateValue);
          if (rowDate < start) {
            return false;
          }
        }
        if (endDateValue) {
          var end = new Date(endDateValue);
          if (rowDate > end) {
            return false;
          }
        }

        return true;
      });

      officerFilter.on("change", function () {
        table.draw();
      });
      startDateFilter.on("change", function () {
        table.draw();
      });
      endDateFilter.on("change", function () {
        table.draw();
      });

      table.draw();
    }
  });
});
