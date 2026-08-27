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

  function formatDisplayDate(dateValue) {
    return dateValue.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric"
    });
  }

  function parseDate(value) {
    var parts = value.split("-");
    return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  }

  function resolveUrl(url) {
    if (!url || /^https?:\/\//.test(url)) {
      return url || "";
    }
    return linkPrefix + url;
  }

  function groupByMonth(lectures, year, months) {
    var map = {};

    months.forEach(function (monthNumber) {
      var key = year + "-" + pad(monthNumber);
      map[key] = [];
    });

    lectures.forEach(function (lecture) {
      var monthKey = lecture.date.slice(0, 7);
      if (!map[monthKey]) {
        map[monthKey] = [];
      }
      map[monthKey].push(lecture);
    });

    Object.keys(map).forEach(function (key) {
      map[key].sort(function (a, b) {
        return a.date.localeCompare(b.date);
      });
    });

    return map;
  }

  function renderChannel(container, data) {
    if (!container) {
      return;
    }

    var term = data.term || {};
    var year = term.year || 2026;
    var months = term.months || [8, 9, 10, 11, 12];
    var lectures = data.lectures || [];
    var grouped = groupByMonth(lectures, year, months);

    container.innerHTML = "";

    var heading = document.createElement("h2");
    heading.className = "lecture-channel__title";
    heading.textContent = "Lecture Calendar";
    container.appendChild(heading);

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

      var monthLectures = grouped[monthKey] || [];

      if (!monthLectures.length) {
        var empty = document.createElement("p");
        empty.className = "lecture-channel__empty";
        empty.textContent = "No lectures posted yet.";
        monthSection.appendChild(empty);
      } else {
        var list = document.createElement("ul");
        list.className = "lecture-channel__list";

        monthLectures.forEach(function (lecture) {
          var item = document.createElement("li");
          var link = document.createElement("a");
          link.className = "lecture-channel__link";
          link.href = resolveUrl(lecture.url);

          var dateLine = document.createElement("span");
          dateLine.className = "lecture-channel__date";
          dateLine.textContent = formatDisplayDate(parseDate(lecture.date));

          var titleLine = document.createElement("span");
          titleLine.className = "lecture-channel__lecture-title";
          titleLine.textContent = lecture.title;

          link.appendChild(dateLine);
          link.appendChild(titleLine);
          item.appendChild(link);
          list.appendChild(item);
        });

        monthSection.appendChild(list);
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
