(function () {
  var config = window.TERM_CALENDAR_CONFIG || {};
  var deadlinesUrl = config.deadlinesUrl || "data/deadlines.json";
  var courseFilter = config.course || null;
  var linkPrefix = config.linkPrefix || "";
  var compact = config.compact === true;

  var TYPE_LABELS = {
    homework: "Homework",
    exam: "Exam",
    admin: "Admin",
    event: "Event"
  };

  var MONTHS = [
    "August", "September", "October", "November", "December"
  ];

  var MONTH_NUMBERS = [8, 9, 10, 11, 12];

  function pad(value) {
    return String(value).padStart(2, "0");
  }

  function parseDate(value) {
    var parts = value.split("-");
    return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  }

  function formatDate(dateValue) {
    return dateValue.getFullYear() + "-" + pad(dateValue.getMonth() + 1) + "-" + pad(dateValue.getDate());
  }

  function formatDisplayDate(dateValue) {
    return dateValue.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric"
    });
  }

  function getCourseName(courses, courseKey) {
    var course = courses[courseKey];
    if (!course) {
      return courseKey;
    }
    return typeof course === "string" ? course : course.name;
  }

  function getCourseHome(courses, courseKey) {
    var course = courses[courseKey];
    if (!course || typeof course === "string") {
      return "";
    }
    return course.home || "";
  }

  function compareDeadlines(a, b) {
    var dateCompare = a.date.localeCompare(b.date);
    if (dateCompare !== 0) {
      return dateCompare;
    }
    var typeOrder = { homework: 0, exam: 1, admin: 2, event: 3 };
    return (typeOrder[a.type] || 9) - (typeOrder[b.type] || 9);
  }

  function expandDeadlineDates(deadline) {
    if (!deadline.endDate || deadline.endDate === deadline.date) {
      return [deadline.date];
    }

    var dates = [];
    var current = parseDate(deadline.date);
    var end = parseDate(deadline.endDate);

    while (current <= end) {
      dates.push(formatDate(current));
      current.setDate(current.getDate() + 1);
    }

    return dates;
  }

  function filterDeadlines(deadlines) {
    return deadlines
      .filter(function (deadline) {
        return !courseFilter || deadline.course === courseFilter;
      })
      .sort(compareDeadlines);
  }

  function resolveUrl(url) {
    if (!url) {
      return "";
    }
    if (/^https?:\/\//.test(url)) {
      return url;
    }
    return linkPrefix + url;
  }

  function isPast(deadline) {
    var today = formatDate(new Date());
    var endDate = deadline.endDate || deadline.date;
    return endDate < today;
  }

  function createDeadlineLink(deadline, label) {
    var link = document.createElement("a");
    link.href = resolveUrl(deadline.url);
    link.textContent = label || deadline.title;
    return link;
  }

  function renderDeadlineItem(deadline, courses, options) {
    options = options || {};
    var li = document.createElement("li");
    li.className = "deadline-item deadline-item--" + deadline.type;

    if (isPast(deadline)) {
      li.classList.add("deadline-item--past");
    }

    var dateLine = document.createElement("p");
    dateLine.className = "deadline-item__date";
    dateLine.textContent = formatDisplayDate(parseDate(deadline.date));
    if (deadline.endDate && deadline.endDate !== deadline.date) {
      dateLine.textContent += " – " + formatDisplayDate(parseDate(deadline.endDate));
    }
    if (deadline.timeDisplay) {
      dateLine.textContent += " · " + deadline.timeDisplay;
    }
    li.appendChild(dateLine);

    var titleLine = document.createElement("p");
    titleLine.className = "deadline-item__title";

    if (deadline.url) {
      titleLine.appendChild(createDeadlineLink(deadline, deadline.title));
    } else {
      titleLine.textContent = deadline.title;
    }
    li.appendChild(titleLine);

    if (!courseFilter && deadline.course && getCourseName(courses, deadline.course)) {
      var courseLine = document.createElement("p");
      courseLine.className = "deadline-item__course";
      var courseHome = getCourseHome(courses, deadline.course);

      if (courseHome) {
        var courseLink = document.createElement("a");
        courseLink.href = resolveUrl(courseHome);
        courseLink.textContent = getCourseName(courses, deadline.course);
        courseLine.appendChild(courseLink);
      } else {
        courseLine.textContent = getCourseName(courses, deadline.course);
      }
      li.appendChild(courseLine);
    }

    if (options.showType !== false) {
      var typeLine = document.createElement("p");
      typeLine.className = "deadline-item__type";
      typeLine.textContent = TYPE_LABELS[deadline.type] || deadline.type;
      li.appendChild(typeLine);
    }

    if (deadline.url && options.showActionLink !== false) {
      var actionLine = document.createElement("p");
      actionLine.className = "deadline-item__action";
      var actionLink = createDeadlineLink(deadline, "Open page");
      actionLink.className = "deadline-item__action-link";
      actionLine.appendChild(actionLink);
      li.appendChild(actionLine);
    }

    return li;
  }

  function renderList(container, deadlines, courses, emptyMessage, filterFn) {
    if (!container) {
      return;
    }

    container.innerHTML = "";
    var filtered = filterDeadlines(deadlines).filter(filterFn || function () {
      return true;
    });

    if (!filtered.length) {
      var empty = document.createElement("p");
      empty.className = "deadline-empty";
      empty.textContent = emptyMessage;
      container.appendChild(empty);
      return;
    }

    var list = document.createElement("ul");
    list.className = "deadline-list";

    filtered.forEach(function (deadline) {
      list.appendChild(renderDeadlineItem(deadline, courses));
    });

    container.appendChild(list);
  }

  function buildDateMap(deadlines) {
    var map = {};

    filterDeadlines(deadlines).forEach(function (deadline) {
      expandDeadlineDates(deadline).forEach(function (dateKey) {
        if (!map[dateKey]) {
          map[dateKey] = [];
        }
        map[dateKey].push(deadline);
      });
    });

    return map;
  }

  function createCalendarMarker(deadline) {
    if (deadline.url) {
      var markerLink = document.createElement("a");
      markerLink.className = "calendar-marker calendar-marker--" + deadline.type;
      markerLink.href = resolveUrl(deadline.url);
      markerLink.title = deadline.title;
      markerLink.setAttribute("aria-label", deadline.title);
      markerLink.addEventListener("click", function (event) {
        event.stopPropagation();
      });
      return markerLink;
    }

    var marker = document.createElement("span");
    marker.className = "calendar-marker calendar-marker--" + deadline.type;
    marker.title = deadline.title;
    return marker;
  }

  function renderCalendar(container, deadlines, courses) {
    if (!container) {
      return;
    }

    container.innerHTML = "";
    container.classList.toggle("calendar--compact", compact);
    var dateMap = buildDateMap(deadlines);
    var todayKey = formatDate(new Date());
    var year = 2026;

    MONTHS.forEach(function (monthName, index) {
      var monthNumber = MONTH_NUMBERS[index];
      var monthSection = document.createElement("section");
      monthSection.className = "calendar-month";
      monthSection.setAttribute("aria-label", monthName + " " + year);

      var heading = document.createElement("h3");
      heading.className = "calendar-month__title";
      heading.textContent = monthName + " " + year;
      monthSection.appendChild(heading);

      var weekdayRow = document.createElement("div");
      weekdayRow.className = "calendar-weekdays";
      ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].forEach(function (day) {
        var cell = document.createElement("span");
        cell.textContent = day;
        weekdayRow.appendChild(cell);
      });
      monthSection.appendChild(weekdayRow);

      var grid = document.createElement("div");
      grid.className = "calendar-grid";

      var firstDay = new Date(year, monthNumber - 1, 1);
      var daysInMonth = new Date(year, monthNumber, 0).getDate();

      for (var blankIndex = 0; blankIndex < firstDay.getDay(); blankIndex += 1) {
        var blank = document.createElement("span");
        blank.className = "calendar-day calendar-day--blank";
        blank.setAttribute("aria-hidden", "true");
        grid.appendChild(blank);
      }

      for (var day = 1; day <= daysInMonth; day += 1) {
        var dateKey = year + "-" + pad(monthNumber) + "-" + pad(day);
        var dayItems = dateMap[dateKey] || [];
        var dayCell = document.createElement("button");
        dayCell.type = "button";
        dayCell.className = "calendar-day";
        dayCell.dataset.date = dateKey;

        var dayNumber = document.createElement("span");
        dayNumber.className = "calendar-day__number";
        dayNumber.textContent = String(day);
        dayCell.appendChild(dayNumber);

        if (dateKey === todayKey) {
          dayCell.classList.add("calendar-day--today");
        }

        if (dayItems.length) {
          dayCell.classList.add("calendar-day--has-deadline");
          dayCell.setAttribute(
            "aria-label",
            formatDisplayDate(parseDate(dateKey)) + ", " + dayItems.length + " item(s)"
          );

          var markers = document.createElement("span");
          markers.className = "calendar-day__markers";
          dayItems.forEach(function (deadline) {
            markers.appendChild(createCalendarMarker(deadline));
          });
          dayCell.appendChild(markers);
        } else {
          dayCell.setAttribute("aria-label", formatDisplayDate(parseDate(dateKey)));
        }

        dayCell.addEventListener("click", (function (selectedDate, selectedItems) {
          return function () {
            showCalendarDetail(container, selectedDate, selectedItems, courses);
          };
        })(dateKey, dayItems));

        grid.appendChild(dayCell);
      }

      monthSection.appendChild(grid);
      container.appendChild(monthSection);
    });

    var detail = document.createElement("div");
    detail.className = "calendar-detail";
    detail.id = "calendar-detail-panel";
    detail.innerHTML = "<p class=\"calendar-detail__hint\">Select a marked day to see linked items, or click a colored marker to open its page directly.</p>";
    container.appendChild(detail);

    var agendaHost = document.getElementById("term-calendar-agenda") || container;
    agendaHost.innerHTML = "";
    renderCalendarAgenda(agendaHost, deadlines, courses);
  }

  function renderCalendarAgenda(container, deadlines, courses) {
    var agenda = document.createElement("div");
    agenda.className = "calendar-agenda";
    agenda.id = "calendar-agenda-list";

    var heading = document.createElement("h3");
    heading.className = "calendar-agenda__title";
    heading.textContent = "All Term Dates";
    if (container.id !== "term-calendar-agenda") {
      agenda.appendChild(heading);
    } else {
      agenda.classList.add("calendar-agenda--bare");
    }

    var list = document.createElement("ul");
    list.className = "deadline-list";

    filterDeadlines(deadlines).forEach(function (deadline) {
      list.appendChild(renderDeadlineItem(deadline, courses, { showActionLink: false }));
    });

    if (!list.children.length) {
      var empty = document.createElement("p");
      empty.className = "deadline-empty";
      empty.textContent = "No dates listed for this view.";
      agenda.appendChild(empty);
      container.appendChild(agenda);
      return;
    }

    agenda.appendChild(list);
    container.appendChild(agenda);
  }

  function showCalendarDetail(container, dateKey, items, courses) {
    var detail = container.querySelector("#calendar-detail-panel");
    if (!detail) {
      return;
    }

    detail.innerHTML = "";
    var heading = document.createElement("h3");
    heading.className = "calendar-detail__title";
    heading.textContent = formatDisplayDate(parseDate(dateKey));
    detail.appendChild(heading);

    if (!items.length) {
      var empty = document.createElement("p");
      empty.textContent = "No deadlines on this date.";
      detail.appendChild(empty);
      return;
    }

    var list = document.createElement("ul");
    list.className = "deadline-list";

    items.sort(compareDeadlines).forEach(function (deadline) {
      list.appendChild(renderDeadlineItem(deadline, courses));
    });

    detail.appendChild(list);
  }

  function init(data) {
    var deadlines = data.deadlines || [];
    var courses = data.courses || {};
    var today = formatDate(new Date());

    renderList(
      document.getElementById("upcoming-deadlines"),
      deadlines,
      courses,
      courseFilter ? "No upcoming items for this class." : "No upcoming deadlines for the term.",
      function (deadline) {
        var endDate = deadline.endDate || deadline.date;
        return endDate >= today && deadline.type !== "event";
      }
    );

    renderList(
      document.getElementById("assignments-list"),
      deadlines,
      courses,
      "No assignments listed yet.",
      function (deadline) {
        return deadline.type === "homework";
      }
    );

    renderCalendar(document.getElementById("term-calendar"), deadlines, courses);
  }

  fetch(deadlinesUrl)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Could not load deadlines.");
      }
      return response.json();
    })
    .then(init)
    .catch(function (error) {
      ["upcoming-deadlines", "assignments-list", "term-calendar", "term-calendar-agenda"].forEach(function (id) {
        var container = document.getElementById(id);
        if (container) {
          container.innerHTML = "<p class=\"deadline-empty\">" + error.message + "</p>";
        }
      });
    });
})();
