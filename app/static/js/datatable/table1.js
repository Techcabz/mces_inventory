$(document).ready(function () {
  $("#datatable_inventory_expired_modal").each(function () {
    var datatable_inventory_expired_modal = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE EXPIRED",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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
  });

  $("#datatable_inventory_soonexpired_modal").each(function () {
    var datatable_inventory_soonexpired_modal = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE SOON TO EXPIRED",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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
  });

   $("#datatable_inventory_available_modal").each(function () {
    var datatable_inventory_available_modal = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE AVAILABLE",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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
  });

  $("#datatable_inventory_zero_modal").each(function () {
    var datatable_inventory_zero_modal = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE ZERO COUNT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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
  });

  $("#datatable_inventory_orderlevel_modal").each(function () {
    var datatable_inventory_orderlevel_modal = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE ORDER LEVEL",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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
  });

  $("#datatable_individual").each(function () {
    var datatable_individual = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "INDIVIDUAL TREATMENT REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_individual;
    var filterType = $("#invfilter-type");
    var filterSY = $("#invfilter-sy");
    var nameFilter = $("#indv-filter");

    const inv_idRadio = document.querySelector('input[value="invid"]');
    const inv_lastnameRadio = document.querySelector(
      'input[value="invlastname"]'
    );
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var filterTypeValue = filterType.val();
      var filterSYValue = filterSY.val();
      var nameFilterValue = nameFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowDataType = rowData[1].toLowerCase();
      var rowDataID = rowData[2].toLowerCase();
      var rowDataSY = rowData[3].toLowerCase();
      var rowDataLastName = rowData[4].toLowerCase();

      if (nameFilterValue === "") {
        return false;
      } else {
        if (
          filterSYValue !== "" &&
          filterSYValue !== "all" &&
          !rowDataSY.endsWith(filterSYValue)
        ) {
          return false;
        }

        if (filterTypeValue === "student") {
          if (
            (inv_idRadio.checked &&
              (nameFilterValue === "" ||
                rowDataID.endsWith(nameFilterValue))) ||
            (inv_lastnameRadio.checked &&
              (nameFilterValue === "" ||
                rowDataLastName.endsWith(nameFilterValue)))
          ) {
            return rowDataType === "student";
          }
        } else if (
          filterTypeValue === "faculty" &&
          rowDataType === "faculty" &&
          inv_idRadio.checked
        ) {
          if (nameFilterValue === "" || rowDataID.endsWith(nameFilterValue)) {
            return true;
          }
        } else if (
          filterTypeValue === "employee" &&
          rowDataType === "employee" &&
          inv_idRadio.checked
        ) {
          if (nameFilterValue === "" || rowDataID.endsWith(nameFilterValue)) {
            return true;
          }
        }
      }
      return false;
    });

    filterSY.on("change", function () {
      table.draw();
    });

    filterType.on("change", function () {
      table.draw();
    });

    nameFilter.on("keyup", function () {
      var nameFilterValue = nameFilter.val().toLowerCase();
      if (nameFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  $("#datatable_resita").each(function () {
    var datatable_resita = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "RESITA ISSUED REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_resita;
    var filterType = $("#invfilter-type");
    var filterSY = $("#invfilter-sy");
    var nameFilter = $("#indv-filter");

    const inv_idRadio = document.querySelector('input[value="invid"]');
    const inv_lastnameRadio = document.querySelector(
      'input[value="invlastname"]'
    );
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var filterTypeValue = filterType.val();
      var filterSYValue = filterSY.val();
      var nameFilterValue = nameFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowDataType = rowData[1].toLowerCase();
      var rowDataID = rowData[2].toLowerCase();
      var rowDataSY = rowData[3].toLowerCase();
      var rowDataLastName = rowData[4].toLowerCase();

      if (nameFilterValue === "") {
        return false;
      } else {
        if (
          filterSYValue !== "" &&
          filterSYValue !== "all" &&
          !rowDataSY.endsWith(filterSYValue)
        ) {
          return false;
        }

        if (filterTypeValue === "student") {
          if (
            (inv_idRadio.checked &&
              (nameFilterValue === "" ||
                rowDataID.endsWith(nameFilterValue))) ||
            (inv_lastnameRadio.checked &&
              (nameFilterValue === "" ||
                rowDataLastName.endsWith(nameFilterValue)))
          ) {
            return rowDataType === "student";
          }
        } else if (
          filterTypeValue === "faculty" &&
          rowDataType === "faculty" &&
          inv_idRadio.checked
        ) {
          if (nameFilterValue === "" || rowDataID.endsWith(nameFilterValue)) {
            return true;
          }
        } else if (
          filterTypeValue === "employee" &&
          rowDataType === "employee" &&
          inv_idRadio.checked
        ) {
          if (nameFilterValue === "" || rowDataID.endsWith(nameFilterValue)) {
            return true;
          }
        }
      }
      return false;
    });

    filterSY.on("change", function () {
      table.draw();
    });

    filterType.on("change", function () {
      table.draw();
    });

    nameFilter.on("keyup", function () {
      var nameFilterValue = nameFilter.val().toLowerCase();
      if (nameFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });

  $("#datatable_inventory_report").each(function () {
    var datatable_inventory_report = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE INVENTORY REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_inventory_report;
    var filterOption = $("#filter-option");
    var fromFilter = $("#from-filter");
    var toFilter = $("#to-filter");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var filterOptionValue = filterOption.val();
      var fromFilterValue = fromFilter.val();
      var toFilterValue = toFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowExpiryDate = rowData[4];
      var rowBatchDate = rowData[3];
      var rowAvailability = rowData[7];
      var rowOrderLevel = rowData[8];

      if (filterOptionValue === "all") {
        return true;
      } else if (filterOptionValue === "expiry") {
        if (rowExpiryDate === "") {
          return false;
        }
        return isWithinDateRange(rowExpiryDate, fromFilterValue, toFilterValue);
      } else if (filterOptionValue === "below_order") {
        if (rowOrderLevel === "") {
          return false;
        }
        return isOrderBelow(
          rowOrderLevel,
          rowAvailability,
          rowBatchDate,
          fromFilterValue,
          toFilterValue
        );
      } else if (filterOptionValue === "out_of_stock") {
        if (rowAvailability === "") {
          return false;
        }
        return isOutStock(
          rowAvailability,
          rowBatchDate,
          fromFilterValue,
          toFilterValue
        );
      } else if (filterOptionValue === "available") {
        if (rowAvailability === "") {
          return false;
        }
        return isAvailable(
          rowAvailability,
          rowBatchDate,
          fromFilterValue,
          toFilterValue
        );
      }

      return false;
    });

    filterOption.on("change", function () {
      table.draw();
    });

    fromFilter.on("change", function () {
      table.draw();
    });

    toFilter.on("change", function () {
      table.draw();
    });

    function isOrderBelow(
      rowOrderLevel,
      rowAvailability,
      rowBatchDate,
      fromDate,
      toDate
    ) {
      var batchDate = new Date(rowBatchDate);
      var fromFilterValue = new Date(fromDate);
      var toFilterValue = new Date(toDate);
      return (
        batchDate >= fromFilterValue &&
        batchDate <= toFilterValue &&
        rowAvailability < rowOrderLevel
      );
    }

    function isOutStock(rowAvailability, rowBatchDate, fromDate, toDate) {
      var batchDate = new Date(rowBatchDate);
      var fromFilterValue = new Date(fromDate);
      var toFilterValue = new Date(toDate);
      return (
        batchDate >= fromFilterValue &&
        batchDate <= toFilterValue &&
        rowAvailability == 0
      );
    }

    function isAvailable(rowAvailability, rowBatchDate, fromDate, toDate) {
      var batchDate = new Date(rowBatchDate);
      var fromFilterValue = new Date(fromDate);
      var toFilterValue = new Date(toDate);
      return (
        batchDate >= fromFilterValue &&
        batchDate <= toFilterValue &&
        rowAvailability > 0
      );
    }

    function isWithinDateRange(date, fromDate, toDate) {
      var expiryDate = new Date(date);
      var fromFilterValue = new Date(fromDate);
      var toFilterValue = new Date(toDate);
      return expiryDate >= fromFilterValue && expiryDate <= toFilterValue;
    }

    table.draw();
  });

  // health
  $("#datatable_health_range").each(function () {
    var datatable_health_range = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "HEALTH SERVICES LOGS",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_health_range;
    var filterOption = $("#healthfilter-option");
    var fromFilter = $("#hfrom-filter");
    var toFilter = $("#hto-filter");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var filterOptionValue = filterOption.val().toLowerCase();
      var fromFilterValue = fromFilter.val();
      var toFilterValue = toFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowType = rowData[1].toLowerCase();
      var rowDate = rowData[5];

      if (filterOptionValue === "all") {
        return true;
      } else if (filterOptionValue === "student") {
        return (
          (rowType.includes(filterOptionValue) ||
            filterOptionValue === "all") &&
          isWithinDateRange(rowDate, fromFilterValue, toFilterValue)
        );
      } else if (filterOptionValue === "faculty") {
        return (
          (rowType.includes(filterOptionValue) ||
            filterOptionValue === "all") &&
          isWithinDateRange(rowDate, fromFilterValue, toFilterValue)
        );
      } else if (filterOptionValue === "employee") {
        return (
          (rowType.includes(filterOptionValue) ||
            filterOptionValue === "all") &&
          isWithinDateRange(rowDate, fromFilterValue, toFilterValue)
        );
      }
      return false;
    });

    filterOption.on("change", function () {
      table.draw();
    });

    fromFilter.on("change", function () {
      table.draw();
    });

    toFilter.on("change", function () {
      table.draw();
    });

    function isWithinDateRange(date, fromDate, toDate) {
      var dataDate = new Date(date);
      var fromFilterValue = new Date(fromDate);
      var toFilterValue = new Date(toDate);

      return dataDate >= fromFilterValue && dataDate <= toFilterValue;
    }

    table.draw();
  });

  $("#datatable_health_month").each(function () {
    var datatable_health_month = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "HEALTH SERVICES LOGS",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_health_month;
    var filterType = $("#hhfilter-option");
    var semesterFilter = $("#hhsemester");
    var yrFilter = $("#hhmonth");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var typefilterValue = filterType.val().toLowerCase();
      var semesterFilterValue = semesterFilter.val();
      var yrFilterValue = yrFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowOption = rowData[1];
      var rowSemester = rowData[2];
      var rowYr = rowData[6];
      let convertedMonth = convertDateToMonthName(rowYr).toLowerCase();

      if (
        typefilterValue === "all" &&
        semesterFilterValue === "all" &&
        yrFilterValue === "all"
      ) {
        return true;
      } else if (
        (typefilterValue === "student" ||
          typefilterValue === "faculty" ||
          typefilterValue === "employee") &&
        rowOption.toLowerCase().includes(typefilterValue)
      ) {
        if (semesterFilterValue === "all" && yrFilterValue === "all") {
          return true;
        } else if (semesterFilterValue === "all") {
          return convertedMonth === yrFilterValue;
        } else if (yrFilterValue === "all") {
          return rowSemester === semesterFilterValue;
        } else {
          return (
            rowSemester === semesterFilterValue &&
            convertedMonth === yrFilterValue
          );
        }
      } else if (typefilterValue === "all" && semesterFilterValue !== "all") {
        return rowSemester === semesterFilterValue;
      } else if (semesterFilterValue === "all" && yrFilterValue !== "all") {
        return convertedMonth === yrFilterValue;
      }

      return false;
    });

    function convertDateToMonthName(dateString) {
      var date = new Date(dateString);
      var options = { month: "long" };
      var monthName = date.toLocaleString("en-US", options);
      return monthName;
    }

    function checkYearRange(rowYear, filterYear) {
      var yearRange = filterYear.split("-");

      var startYear = parseInt(yearRange[0].trim());
      var endYear = parseInt(yearRange[1].trim());
      var rowYearValue = parseInt(rowYear.trim());

      return rowYearValue >= startYear && rowYearValue <= endYear;
    }
    filterType.on("change", function () {
      table.draw();
    });

    semesterFilter.on("change", function () {
      table.draw();
    });

    yrFilter.on("change", function () {
      table.draw();
    });

    table.draw();
  });

  // doctor
  $("#datatable_doctor").each(function () {
    var datatable_doctor = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "DOCTOR PER DUTY REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_doctor;
    var filterType = $("#hhfilter-option");
    var semesterFilter = $("#hhsemester");
    var yrFilter = $("#hhmonth");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var typefilterValue = filterType.val().toLowerCase();
      var semesterFilterValue = semesterFilter.val();
      var yrFilterValue = yrFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowOption = rowData[1];
      var rowSemester = rowData[2];
      var rowYr = rowData[6];
      let convertedMonth = convertDateToMonthName(rowYr).toLowerCase();

      if (
        typefilterValue === "all" &&
        semesterFilterValue === "all" &&
        yrFilterValue === "all"
      ) {
        return true;
      } else if (
        typefilterValue !== "all" &&
        rowOption.toLowerCase().includes(typefilterValue)
      ) {
        if (semesterFilterValue === "all" && yrFilterValue === "all") {
          return true;
        } else if (semesterFilterValue === "all") {
          return convertedMonth === yrFilterValue;
        } else if (yrFilterValue === "all") {
          return rowSemester === semesterFilterValue;
        } else {
          return (
            rowSemester === semesterFilterValue &&
            convertedMonth === yrFilterValue
          );
        }
      } else if (typefilterValue === "all" && semesterFilterValue !== "all") {
        return rowSemester === semesterFilterValue;
      } else if (semesterFilterValue === "all" && yrFilterValue !== "all") {
        return convertedMonth === yrFilterValue;
      }

      return false;
    });

    function convertDateToMonthName(dateString) {
      var date = new Date(dateString);
      var options = { month: "long" };
      var monthName = date.toLocaleString("en-US", options);
      return monthName;
    }

    filterType.on("change", function () {
      table.draw();
    });

    semesterFilter.on("change", function () {
      table.draw();
    });

    yrFilter.on("change", function () {
      table.draw();
    });

    table.draw();
  });

  $("#datatable_health_semester").each(function () {
    var datatable_health_semester = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "HEALTH SERVICES LOGS",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_health_semester;
    var filterType = $("#hhhfilter-option");
    var semesterFilter = $("#hhhsemester");
    var yrFilter = $("#hhhfilter-sy");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var typefilterValue = filterType.val().toLowerCase();
      var semesterFilterValue = semesterFilter.val();
      var yrFilterValue = yrFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowOption = rowData[1];
      var rowSemester = rowData[2];
      var rowYr = rowData[6];
      let convertedYr = convertDateToYear(rowYr);

      if (
        typefilterValue === "all" &&
        semesterFilterValue === "all" &&
        yrFilterValue === "all"
      ) {
        return true;
      } else if (
        typefilterValue === "student" ||
        typefilterValue === "faculty" ||
        typefilterValue === "employee"
      ) {
        if (rowOption.toLowerCase().includes(typefilterValue)) {
          if (semesterFilterValue === "all" && yrFilterValue === "all") {
            return true;
          } else if (semesterFilterValue === "all") {
            return parseInt(yrFilterValue) === parseInt(convertedYr);
          } else if (yrFilterValue === "all") {
            return rowSemester === semesterFilterValue;
          } else {
            return (
              rowSemester === semesterFilterValue &&
              parseInt(yrFilterValue) === parseInt(convertedYr)
            );
          }
        }
      } else if (typefilterValue === "all" && semesterFilterValue !== "all") {
        return rowSemester === semesterFilterValue;
      } else if (semesterFilterValue === "all" && yrFilterValue !== "all") {
        return parseInt(yrFilterValue) === parseInt(convertedYr);
      }

      return false;
    });

    function convertDateToYear(dateString) {
      var date = new Date(dateString);
      var year = date.getFullYear();
      return year;
    }

    filterType.on("change", function () {
      table.draw();
    });

    semesterFilter.on("change", function () {
      table.draw();
    });

    yrFilter.on("change", function () {
      table.draw();
    });

    table.draw();
  });

  // consultation
  $("#datatable_consulatation_report").each(function () {
    var datatable_consulatation_report = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "TOTAL CONSULTATION/TREATMENT REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_consulatation_report;
    var filterType = $("#clfilter-type");
    var semesterFilter = $("#clfilter-semester");
    var yrFilter = $("#clfilter-yr");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var typefilterValue = filterType.val().toLowerCase();
      var semesterFilterValue = semesterFilter.val();
      var yrFilterValue = yrFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowOption = rowData[1];
      var rowSemester = rowData[2];
      var rowYr = rowData[3];

      if (
        typefilterValue === "all" &&
        semesterFilterValue === "all" &&
        yrFilterValue === "all"
      ) {
        return true;
      } else if (
        (typefilterValue === "student" ||
          typefilterValue === "faculty" ||
          typefilterValue === "employee") &&
        rowOption.toLowerCase().includes(typefilterValue)
      ) {
        if (semesterFilterValue === "all" && yrFilterValue === "all") {
          return true;
        } else if (semesterFilterValue === "all") {
          return checkYearRange(rowYr, yrFilterValue);
        } else if (yrFilterValue === "all") {
          return rowSemester === semesterFilterValue;
        } else {
          return (
            rowSemester === semesterFilterValue &&
            checkYearRange(rowYr, yrFilterValue)
          );
        }
      } else if (typefilterValue === "all" && semesterFilterValue !== "all") {
        return rowSemester === semesterFilterValue;
      } else if (semesterFilterValue === "all" && yrFilterValue !== "all") {
        return checkYearRange(rowYr, yrFilterValue);
      }

      return false;
    });

    function checkYearRange(rowYear, filterYear) {
      var yearRange = filterYear.split("-");

      var startYear = parseInt(yearRange[0].trim());
      var endYear = parseInt(yearRange[1].trim());
      var rowYearValue = parseInt(rowYear.trim());

      return rowYearValue >= startYear && rowYearValue <= endYear;
    }
    filterType.on("change", function () {
      table.draw();
    });

    semesterFilter.on("change", function () {
      table.draw();
    });

    yrFilter.on("change", function () {
      table.draw();
    });

    table.draw();
  });

  // report per
  $("#datatable_per_stud").each(function () {
    var datatable_per_stud = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMED PER STUDENT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_per_stud;
    var nameFilter = $("#indv-filter");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var nameFilterValue = nameFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();

      if (nameFilterValue === "") {
        return false;
      } else {
        return rowDataFilter.endsWith(nameFilterValue);
      }
    });

    nameFilter.on("input keyup", function () {
      var nameFilterValue = nameFilter.val().toLowerCase();
      if (nameFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  $("#datatable_per_fac").each(function () {
    var datatable_per_fac = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMED PER FACULTY",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_per_fac;
    var nameFilter = $("#indv-filter");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var nameFilterValue = nameFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();

      if (nameFilterValue === "") {
        return false;
      } else {
        return rowDataFilter.endsWith(nameFilterValue);
      }
    });

    nameFilter.on("input keyup", function () {
      var nameFilterValue = nameFilter.val().toLowerCase();
      if (nameFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  $("#datatable_per_em").each(function () {
    var datatable_per_em = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMED PER EMPLOYEE",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_per_em;
    var nameFilter = $("#indv-filter");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var nameFilterValue = nameFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();

      if (nameFilterValue === "") {
        return false;
      } else {
        return rowDataFilter.endsWith(nameFilterValue);
      }
    });

    nameFilter.on("input keyup", function () {
      var nameFilterValue = nameFilter.val().toLowerCase();
      if (nameFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  $("#datatable_sum_day").each(function () {
    var datatable_sum_day = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMPTION SUMMARY PER DAY REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_sum_day;
    var dateFilter = $("#date-filter");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var dateFilterValue = dateFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1];

      if (dateFilter === "") {
        return false;
      } else {
        return rowDataFilter.endsWith(dateFilterValue);
      }
    });

    dateFilter.on("input keyup", function () {
      var dateFilterValue = dateFilter.val();
      if (dateFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  $("#datatable_month_day").each(function () {
    var datatable_month_day = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMPTION SUMMARY PER MONTH REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    const semesterMonths = {
      1: [
        { label: "June", value: "06" },
        { label: "July", value: "07" },
        { label: "August", value: "08" },
        { label: "September", value: "09" },
        { label: "October", value: "10" },
        { label: "November", value: "11" },
        { label: "December", value: "12" },
      ],
      2: [
        { label: "January", value: "01" },
        { label: "February", value: "02" },
        { label: "March", value: "03" },
        { label: "April", value: "04" },
        { label: "May", value: "05" },
      ],
    };

    function populateMonthDropdown(semester) {
      var monthDropdown = $("#mmonth");
      var months = semesterMonths[semester];

      monthDropdown.empty();
      months.forEach(function (month) {
        monthDropdown.append(new Option(month.label, month.value));
      });
    }

    var table = datatable_month_day;
    var semesterFilter = $("#month-semester");
    var syFilter = $("#month-sy");
    var monthFilter = $("#mmonth");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var semesterFilterValue = semesterFilter.val().toLowerCase();
      var syFilterValue = syFilter.val();
      var monthFilterValue = monthFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowSemesterDataFilter = rowData[1];
      var rowSYDataFilter = rowData[2];
      var rowMonthDataFilter = rowData[3];

      var semesterMatch =
        semesterFilterValue === "" ||
        rowSemesterDataFilter.endsWith(semesterFilterValue);
      var syMatch =
        syFilterValue === "" || rowSYDataFilter.endsWith(syFilterValue);
      var monthMatch =
        monthFilterValue === "" ||
        rowMonthDataFilter.endsWith(monthFilterValue);
      return semesterMatch && syMatch && monthMatch;
    });

    semesterFilter.on("change", function () {
      var semesterFilterValue = semesterFilter.val();
      if (semesterFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }

      populateMonthDropdown(semesterFilterValue);
      table.draw();
    });

    syFilter.on("change", function () {
      var syFilterValue = syFilter.val();
      if (syFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    monthFilter.on("change", function () {
      var monthFilterValue = monthFilter.val();

      if (monthFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  $("#datatable_semester_day").each(function () {
    var datatable_semester_day = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMPTION SUMMARY PER SEMESTER REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    var table = datatable_semester_day;
    var semesterFilter = $("#sum-semester");
    var syFilter = $("#sum-sy");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var semesterFilterValue = semesterFilter.val().toLowerCase();
      var syFilterValue = syFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowSemesterDataFilter = rowData[1];
      var rowSYDataFilter = rowData[2];

      var semesterMatch =
        semesterFilterValue === "" ||
        rowSemesterDataFilter.endsWith(semesterFilterValue);
      var syMatch =
        syFilterValue === "" || rowSYDataFilter.endsWith(syFilterValue);

      return semesterMatch && syMatch;
    });

    semesterFilter.on("change", function () {
      var semesterFilterValue = semesterFilter.val();
      if (semesterFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    syFilter.on("change", function () {
      var syFilterValue = syFilter.val();
      if (syFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  // illness
  $("#datatable_illness").each(function () {
    var datatable_illness = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "MEDICINE CONSUMPTION SUMMARY PER MONTH REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
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

    const semesterMonths = {
      1: [
        { label: "June", value: "06" },
        { label: "July", value: "07" },
        { label: "August", value: "08" },
        { label: "September", value: "09" },
        { label: "October", value: "10" },
        { label: "November", value: "11" },
        { label: "December", value: "12" },
      ],
      2: [
        { label: "January", value: "01" },
        { label: "February", value: "02" },
        { label: "March", value: "03" },
        { label: "April", value: "04" },
        { label: "May", value: "05" },
      ],
    };

    function populateMonthDropdown(semester) {
      var monthDropdown = $("#mmonth");
      var months = semesterMonths[semester];

      monthDropdown.empty();
      months.forEach(function (month) {
        monthDropdown.append(new Option(month.label, month.value));
      });
    }

    var table = datatable_illness;
    var semesterFilter = $("#month-semester");
    var syFilter = $("#month-sy");
    var monthFilter = $("#mmonth");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var semesterFilterValue = semesterFilter.val().toLowerCase();
      var syFilterValue = syFilter.val();
      var monthFilterValue = monthFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowSemesterDataFilter = rowData[1];
      var rowSYDataFilter = rowData[2];
      var rowMonthDataFilter = rowData[3];

      var semesterMatch =
        semesterFilterValue === "" ||
        rowSemesterDataFilter.endsWith(semesterFilterValue);
      var syMatch =
        syFilterValue === "" || rowSYDataFilter.endsWith(syFilterValue);
      var monthMatch =
        monthFilterValue === "" ||
        rowMonthDataFilter.endsWith(monthFilterValue);
      return semesterMatch && syMatch && monthMatch;
    });

    semesterFilter.on("change", function () {
      var semesterFilterValue = semesterFilter.val();
      if (semesterFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }

      populateMonthDropdown(semesterFilterValue);
      table.draw();
    });

    syFilter.on("change", function () {
      var syFilterValue = syFilter.val();
      if (syFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    monthFilter.on("change", function () {
      var monthFilterValue = monthFilter.val();

      if (monthFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }
      table.draw();
    });

    table.draw();
  });
  // total registered
  $("#datatable_reg_stud").each(function () {
    var datatable_reg_stud = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "TOTAL STUDENT REGISTERED",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
          customize: function (win) {
            $(win.document.body)
              .find("table")
              .addClass("display")
              .css("font-size", "16px");
            $(win.document.body)
              .find("tr:nth-child(odd) td")
              .each(function () {
                $(this).css("background-color", "#D0D0D0");
              });
            $(win.document.body)
              .find("h1")
              .css("text-align", "center")
              .css("font-size", "16px");
            $(win.document.body).find("h1").text("TOTAL STUDENT REGISTERED");
            $(win.document.body).find("h1").after("<hr>");
            $(win.document.body)
              .find("thead")
              .after('<tfoot><tr><th colspan="5"></th></tr></tfoot>');
            $(win.document.body).find("tfoot th").css("text-align", "left");

            var totalRegistered = table.rows({ search: "applied" }).count();
            $(win.document.body)
              .find("tfoot th")
              .text("Total Registered: " + totalRegistered)
              .css("font-weight", "bold");
          },
        },
      ],
      searching: true,
      lengthChange: true,
      info: true,

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

    var table = datatable_reg_stud;
    var regSemesterFilter = $("#reg-semester");
    var regSyFilter = $("#reg-sy");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var syFilterValue = regSyFilter.val();
      var semFilterValue = regSemesterFilter.val();
      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();

      var date = new Date(rowDataFilter);
      var month = date.getMonth() + 1;
      var year = date.toLocaleDateString("en-US", { year: "numeric" });
      var semester = "";

      if (month >= 1 && month <= 6) {
        semester = "1";
      } else if (month >= 7 && month <= 12) {
        semester = "2";
      }

      var semesterMatch =
        semFilterValue === "all" || semFilterValue === semester.toString(); // Compare with the string representation of semester
      var syMatch = syFilterValue === "all" || syFilterValue === year;

      return semesterMatch && syMatch;
    });

    regSemesterFilter.on("change", function () {
      var value = regSemesterFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total Registered: " + totalRegistered)
        .css("font-weight", "bold");
    });

    regSyFilter.on("change", function () {
      var value = regSyFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total Registered: " + totalRegistered)
        .css("font-weight", "bold");
    });

    table.draw();
  });

  $("#datatable_reg_fac").each(function () {
    var datatable_reg_fac = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "TOTAL FACULTY REGISTERED",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
          customize: function (win) {
            $(win.document.body)
              .find("table")
              .addClass("display")
              .css("font-size", "16px");
            $(win.document.body)
              .find("tr:nth-child(odd) td")
              .each(function () {
                $(this).css("background-color", "#D0D0D0");
              });
            $(win.document.body)
              .find("h1")
              .css("text-align", "center")
              .css("font-size", "16px");
            $(win.document.body).find("h1").text("TOTAL FACULTY REGISTERED");
            $(win.document.body).find("h1").after("<hr>");
            $(win.document.body)
              .find("thead")
              .after('<tfoot><tr><th colspan="5"></th></tr></tfoot>');
            $(win.document.body).find("tfoot th").css("text-align", "left");

            var totalRegistered = table.rows({ search: "applied" }).count();
            $(win.document.body)
              .find("tfoot th")
              .text("Total Registered: " + totalRegistered)
              .css("font-weight", "bold");
          },
        },
      ],
      searching: true,
      lengthChange: true,
      info: true,

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

    var table = datatable_reg_fac;
    var regSemesterFilter = $("#reg-semester");
    var regSyFilter = $("#reg-sy");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var syFilterValue = regSyFilter.val();
      var semFilterValue = regSemesterFilter.val().toLowerCase();
      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();
      var rowDataOfficeFilter = rowData[6].toLowerCase();

      var date = new Date(rowDataFilter);
      var year = date.toLocaleDateString("en-US", { year: "numeric" });

      var semesterMatch =
        semFilterValue === "all" ||
        rowDataOfficeFilter.endsWith(semFilterValue);
      var syMatch = syFilterValue === "all" || syFilterValue === year;

      return semesterMatch && syMatch;
    });

    regSemesterFilter.on("change", function () {
      var value = regSemesterFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total Registered: " + totalRegistered)
        .css("font-weight", "bold");
    });

    regSyFilter.on("change", function () {
      var value = regSyFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total Registered: " + totalRegistered)
        .css("font-weight", "bold");
    });

    table.draw();
  });
  $("#datatable_reg_em").each(function () {
    var datatable_reg_em = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "TOTAL EMPLOYEE REGISTERED",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
          customize: function (win) {
            $(win.document.body)
              .find("table")
              .addClass("display")
              .css("font-size", "16px");
            $(win.document.body)
              .find("tr:nth-child(odd) td")
              .each(function () {
                $(this).css("background-color", "#D0D0D0");
              });
            $(win.document.body)
              .find("h1")
              .css("text-align", "center")
              .css("font-size", "16px");
            $(win.document.body).find("h1").text("TOTAL EMPLOYEE REGISTERED");
            $(win.document.body).find("h1").after("<hr>");
            $(win.document.body)
              .find("thead")
              .after('<tfoot><tr><th colspan="5"></th></tr></tfoot>');
            $(win.document.body).find("tfoot th").css("text-align", "left");

            var totalRegistered = table.rows({ search: "applied" }).count();
            $(win.document.body)
              .find("tfoot th")
              .text("Total Registered: " + totalRegistered)
              .css("font-weight", "bold");
          },
        },
      ],
      searching: true,
      lengthChange: true,
      info: true,

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

    var table = datatable_reg_em;
    var regSemesterFilter = $("#reg-semester");
    var regSyFilter = $("#reg-sy");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var syFilterValue = regSyFilter.val();
      var semFilterValue = regSemesterFilter.val().toLowerCase();
      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();
      var rowDataOfficeFilter = rowData[6].toLowerCase();

      var date = new Date(rowDataFilter);
      var year = date.toLocaleDateString("en-US", { year: "numeric" });

      var semesterMatch =
        semFilterValue === "all" ||
        rowDataOfficeFilter.endsWith(semFilterValue);
      var syMatch = syFilterValue === "all" || syFilterValue === year;

      return semesterMatch && syMatch;
    });

    regSemesterFilter.on("change", function () {
      var value = regSemesterFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total Registered: " + totalRegistered)
        .css("font-weight", "bold");
    });

    regSyFilter.on("change", function () {
      var value = regSyFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total Registered: " + totalRegistered)
        .css("font-weight", "bold");
    });

    table.draw();
  });

  $("#datatable_report_consult").each(function () {
    var datatable_report_consult = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "Individual Treatement Report",
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

    var table = datatable_report_consult;
    var filterType = $("#invfilter-type");
    var nameFilter = $("#indv-filter");

    const inv_idRadio = document.querySelector('input[value="invid"]');
    const inv_lastnameRadio = document.querySelector(
      'input[value="invlastname"]'
    );
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var filterTypeValue = filterType.val();
      var nameFilterValue = nameFilter.val().toLowerCase();

      var rowData = table.row(dataIndex).data();
      var rowDataType = rowData[1].toLowerCase();
      var rowDataID = rowData[2].toLowerCase();
      var rowDataLastName = rowData[3].toLowerCase();

      if (nameFilterValue === "") {
        return false;
      } else {
        if (filterTypeValue === "student") {
          if (
            (inv_idRadio.checked &&
              (nameFilterValue === "" ||
                rowDataID.endsWith(nameFilterValue))) ||
            (inv_lastnameRadio.checked &&
              (nameFilterValue === "" ||
                rowDataLastName.endsWith(nameFilterValue)))
          ) {
            return rowDataType === "student";
          }
        } else if (
          filterTypeValue === "faculty" &&
          rowDataType === "faculty" &&
          inv_idRadio.checked
        ) {
          if (nameFilterValue === "" || rowDataID.endsWith(nameFilterValue)) {
            return true;
          }
        } else if (
          filterTypeValue === "employee" &&
          rowDataType === "employee" &&
          inv_idRadio.checked
        ) {
          if (nameFilterValue === "" || rowDataID.endsWith(nameFilterValue)) {
            return true;
          }
        }
      }
      return false;
    });

    filterType.on("change", function () {
      table.draw();
    });

    nameFilter.on("keyup", function () {
      var nameFilterValue = nameFilter.val().toLowerCase();

      if (nameFilterValue === "") {
        table.search("").draw(); // Clear the table search
        return;
      }

      table.draw();
      updatePrintButton();
    });
    table.draw();
  });

  $("#datatable_feedback").each(function () {
    var datatable_feedback = $(this).DataTable({
      dom: "Bfrtip",
      buttons: [
        {
          extend: "print",
          text: "Print",
          title: "FEEDBACK REPORT",
          exportOptions: {
            columns: ":not(.exclude-print)",
          },
          customize: function (win) {
            $(win.document.body)
              .find("table")
              .addClass("display")
              .css("font-size", "16px");
            $(win.document.body)
              .find("tr:nth-child(odd) td")
              .each(function () {
                $(this).css("background-color", "#D0D0D0");
              });
            $(win.document.body)
              .find("h1")
              .css("text-align", "center")
              .css("font-size", "16px");
            $(win.document.body).find("h1").text("FEEDBACK REPORT");
            $(win.document.body).find("h1").after("<hr>");
            $(win.document.body)
              .find("thead")
              .after('<tfoot><tr><th colspan="5"></th></tr></tfoot>');
            $(win.document.body).find("tfoot th").css("text-align", "left");

            var totalRegistered = table.rows({ search: "applied" }).count();
            $(win.document.body)
              .find("tfoot th")
              .text("Total FeedBack: " + totalRegistered)
              .css("font-weight", "bold");
          },
        },
      ],
      searching: true,
      lengthChange: true,
      info: true,

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

    var table = datatable_feedback;

    var rfedSyFilter = $("#feedback-sy");

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      var syFilterValue = rfedSyFilter.val();

      var rowData = table.row(dataIndex).data();
      var rowDataFilter = rowData[1].toLowerCase();
      var date = new Date(rowDataFilter);
      var year = date.toLocaleDateString("en-US", { year: "numeric" });
      var syMatch = syFilterValue === "all" || syFilterValue === year;

      return syMatch;
    });

    rfedSyFilter.on("change", function () {
      var value = rfedSyFilter.val();
      if (value === "") {
        table.search("").draw();
        return;
      }
      table.draw();

      var totalRegistered = table.rows({ search: "applied" }).count();
      $(this)
        .closest("table")
        .find("tfoot th")
        .text("Total FeedBack: " + totalRegistered)
        .css("font-weight", "bold");
    });

    table.draw();
  });
});
