$(document).ready(function () {
  var protocol = window.location.protocol;
  var hostname = window.location.hostname;
  var firstPath = window.location.pathname.split("/")[1];
  var fullUrl = protocol + "//" + hostname + "/" + firstPath;

  var table = $("#datatable").DataTable({
    dom: "l<br>Brtip",
    buttons: [
    
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


});
