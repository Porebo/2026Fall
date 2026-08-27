(function () {
  var config = window.RESEARCH_METHODS_LECTURES_CONFIG || {};
  var lecturesUrl = config.lecturesUrl || "data/research-methods-lectures.json";
  var linkPrefix = config.linkPrefix || "";

  var MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

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

  function resolveUrl(url) {
    if (!url || /^https?:\/\//.test(url)) {
      return url || "";
    }
    return linkPrefix + url;
  }

  function buildMeetingDates(schedule) {
    if (!schedule || !schedule.startDate || !schedule.endDate) {
      return {};
    }

    var map = {};
    var current = parseDate(schedule.startDate);
    var end = parseDate(schedule.endDate);
    var targetDay = typeof schedule.dayOfWeek === "number" ? schedule.dayOfWeek : 1;

    while (current.getDay() !== targetDay) {
      current.setDate(current.getDate() + 1);
    }

    while (current <= end) {
      map[formatDate(current)] = true;
      current.setDate(current.getDate() + 7);
    }

    return map;
  }

  function buildLectureMap(lectures) {
    var map = {};

    (lectures || []).forEach(function (lecture) {
      map[lecture.date] = lecture;
    });

    return map;
  }

  function renderScheduleHeader(container, schedule) {
    if (!schedule) {
      return;
    }

    var block = document.createElement("div");
    block.className = "lecture-channel__schedule";

    var title = document.createElement("p");
    title.className = "lecture-channel__schedule-title";
    title.textContent = "Weekly class meeting";
    block.appendChild(title);

    var central = document.createElement("p");
    central.className = "lecture-channel__schedule-time";
    central.textContent = schedule.displayCentral + " · " + schedule.location;
    block.appendChild(central);

    var pacific = document.createElement("p");
    pacific.className = "lecture-channel__schedule-time lecture-channel__schedule-time--local";
    pacific.textContent = schedule.displayPacific;
    block.appendChild(pacific);

    var legend = document.createElement("ul");
    legend.className = "lecture-channel__legend";
    legend.innerHTML =
      "<li><span class=\"lecture-channel__legend-box lecture-channel__legend-box--meeting\" aria-hidden=\"true\"></span> Class meeting</li>" +
      "<li><span class=\"lecture-channel__legend-box lecture-channel__legend-box--lecture\" aria-hidden=\"true\"></span> Notes posted</li>";
    block.appendChild(legend);

    container.appendChild(block);
  }

  function createDayCell(dateKey, dayNumber, meetingDates, lectureMap) {
    var isMeeting = !!meetingDates[dateKey];
    var lecture = lectureMap[dateKey];
    var cell;

    if (lecture && lecture.url) {
      cell = document.createElement("a");
      cell.href = resolveUrl(lecture.url);
      cell.title = lecture.title;
    } else {
      cell = document.createElement("span");
    }

    cell.className = "lecture-channel__day";
    if (isMeeting) {
      cell.classList.add("lecture-channel__day--meeting");
    }
    if (lecture) {
      cell.classList.add("lecture-channel__day--lecture");
    }

    cell.textContent = String(dayNumber);

    if (isMeeting && lecture) {
      cell.setAttribute("aria-label", "Class meeting with notes on day " + dayNumber);
    } else if (isMeeting) {
      cell.setAttribute("aria-label", "Class meeting on day " + dayNumber);
    } else if (lecture) {
      cell.setAttribute("aria-label", "Lecture notes on day " + dayNumber);
    } else {
      cell.setAttribute("aria-label", "Day " + dayNumber);
    }

    return cell;
  }

  function renderMonthGrid(monthNumber, year, meetingDates, lectureMap) {
    var grid = document.createElement("div");
    grid.className = "lecture-channel__day-grid";

    var weekdays = document.createElement("div");
    weekdays.className = "lecture-channel__weekdays";
    ["S", "M", "T", "W", "T", "F", "S"].forEach(function (label) {
      var cell = document.createElement("span");
      cell.textContent = label;
      weekdays.appendChild(cell);
    });
    grid.appendChild(weekdays);

    var daysWrap = document.createElement("div");
    daysWrap.className = "lecture-channel__days";

    var firstDay = new Date(year, monthNumber - 1, 1);
    var daysInMonth = new Date(year, monthNumber, 0).getDate();

    for (var blankIndex = 0; blankIndex < firstDay.getDay(); blankIndex += 1) {
      var blank = document.createElement("span");
      blank.className = "lecture-channel__day lecture-channel__day--blank";
      blank.setAttribute("aria-hidden", "true");
      daysWrap.appendChild(blank);
    }

    for (var day = 1; day <= daysInMonth; day += 1) {
      var dateKey = year + "-" + pad(monthNumber) + "-" + pad(day);
      daysWrap.appendChild(createDayCell(dateKey, day, meetingDates, lectureMap));
    }

    grid.appendChild(daysWrap);
    return grid;
  }

  function renderLectureList(monthLectures) {
    if (!monthLectures.length) {
      return null;
    }

    var listWrap = document.createElement("div");
    listWrap.className = "lecture-channel__notes";

    var listTitle = document.createElement("p");
    listTitle.className = "lecture-channel__notes-title";
    listTitle.textContent = "Posted lecture notes";
    listWrap.appendChild(listTitle);

    var list = document.createElement("ul");
    list.className = "lecture-channel__list";

    monthLectures.forEach(function (lecture) {
      var item = document.createElement("li");
      var link = document.createElement("a");
      link.className = "lecture-channel__link";
      link.href = resolveUrl(lecture.url);
      link.textContent = lecture.date.slice(5).replace("-", "/") + " — " + lecture.title;
      item.appendChild(link);
      list.appendChild(item);
    });

    listWrap.appendChild(list);
    return listWrap;
  }

  function renderChannel(container, data) {
    if (!container) {
      return;
    }

    var term = data.term || {};
    var year = term.year || 2026;
    var months = term.months || [8, 9, 10, 11, 12];
    var lectures = data.lectures || [];
    var meetingDates = buildMeetingDates(data.meetingSchedule);
    var lectureMap = buildLectureMap(lectures);

    container.innerHTML = "";

    var heading = document.createElement("h2");
    heading.className = "lecture-channel__title";
    heading.textContent = "Lecture Calendar";
    container.appendChild(heading);

    renderScheduleHeader(container, data.meetingSchedule);

    months.forEach(function (monthNumber) {
      var monthKey = year + "-" + pad(monthNumber);
      var monthSection = document.createElement("section");
      monthSection.className = "lecture-channel__month";
      monthSection.id = "lecture-month-" + monthKey;
      monthSection.setAttribute("aria-label", MONTH_NAMES[monthNumber - 1] + " " + year);

      var monthHeading = document.createElement("h3");
      monthHeading.className = "lecture-channel__month-title";
      monthHeading.textContent = MONTH_NAMES[monthNumber - 1] + " " + year;
      monthSection.appendChild(monthHeading);

      monthSection.appendChild(renderMonthGrid(monthNumber, year, meetingDates, lectureMap));

      var monthLectures = lectures
        .filter(function (lecture) {
          return lecture.date.slice(0, 7) === monthKey;
        })
        .sort(function (a, b) {
          return a.date.localeCompare(b.date);
        });

      var notes = renderLectureList(monthLectures);
      if (notes) {
        monthSection.appendChild(notes);
      }

      container.appendChild(monthSection);
    });
  }

  fetch(lecturesUrl)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Could not load lecture calendar.");
      }
      return response.json();
    })
    .then(function (data) {
      renderChannel(document.getElementById("lecture-channel"), data);
    })
    .catch(function (error) {
      var container = document.getElementById("lecture-channel");
      if (container) {
        container.innerHTML = "<p class=\"deadline-empty\">" + error.message + "</p>";
      }
    });
})();
