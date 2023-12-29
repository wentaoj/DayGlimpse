function buildCalendar(data) {
    var calendar = $("#calendar-grid");
    calendar.empty();
  
    var months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    var header = $("<h3>").addClass("text-center").text(months[data.month-1] + " " + data.year);
    calendar.append(header);
  
    var table = $("<table>").addClass("mx-auto");
    var weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    var thead = $("<thead>");
  
    var tr = $("<tr>");
    for (var i = 0; i < weekdays.length; i++) {
        var th = $("<th>").text(weekdays[i]);
        tr.append(th);
    }
    thead.append(tr);
    table.append(thead);
  
    var tbody = $("<tbody>");
    for (var i = 0; i < data.calendar.length; i++) {
        var week = data.calendar[i];
        var tr = $("<tr>");
        for (var j = 0; j < week.length; j++) {
            var day = week[j];
            var td = $("<td>").text(day === 0 ? "-" : day);
            if (day !== 0) {
                // clickable event listener
                td.click(function() {
                    var year = data.year;
                    var month = data.month;
                    var dayText = $(this).text().padStart(2, "0");
                    var date = year + "-" + month + "-" + dayText;
                    window.location.href = "/calendar/reminders/" + date;
                });
            }
            tr.append(td);
        }
        tbody.append(tr);
    }
    
    table.append(tbody);
    calendar.append(table);
  
    var prevButton = $("<button>")
        .addClass("btn btn-primary cal-btn")
        .text(" < Back ")
        .click(function() {
            var year = data.year;
            var month = data.month;
            if (month == 1) {
                year--;
                month = 12;
            } else {
                month--;
            }
            var date = year + "-" + month.toString().padStart(2, "0") + "-01";
            $.ajax({
                url: "/calendar-data/" + date,
                success: function(data) {
                buildCalendar(data);
                }
            });
        });

    var nextButton = $("<button>")
        .addClass("btn btn-primary cal-btn")
        .text(" Foward > ")
        .click(function() {
            var year = data.year;
            var month = data.month;
            if (month == 12) {
                year++;
                month = 1;
            } else {
                month++;
            }
            var date = year + "-" + month.toString().padStart(2, "0") + "-01";
            $.ajax({
                url: "/calendar-data/" + date,
                success: function(data) {
                    buildCalendar(data);
                }
            });
        });
    // prev is on the left, next is on the right
    calendar.prepend(nextButton);
    calendar.prepend(prevButton);
  }
  