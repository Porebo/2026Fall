(function () {
  var CLASSES = [
    { label: "Graduate Project", slug: "graduate-project", home: "home-graduate-project.html" },
    { label: "Principles of IQ", slug: "principles-of-iq", home: "home-principles-of-iq.html" },
    { label: "Research Methods", slug: "research-methods", home: "home-research-methods.html" },
    { label: "Master Thesis", slug: "master-thesis", home: "home-master-thesis.html" }
  ];

  function getRootPrefix() {
    var homeLink = document.querySelector(".breadcrumb a[href$=\"index.html\"]");
    if (!homeLink) {
      return "";
    }
    return homeLink.getAttribute("href").replace(/index\.html$/, "");
  }

  function isCurrentClass(slug) {
    return window.location.pathname.indexOf("/" + slug + "/") !== -1;
  }

  function buildClassNav(root) {
    var nav = document.createElement("nav");
    nav.className = "class-nav";
    nav.setAttribute("aria-label", "Class navigation");

    CLASSES.forEach(function (course) {
      var link = document.createElement("a");
      link.className = "class-nav__button";
      link.href = root + "classes/" + course.slug + "/" + course.home;
      link.textContent = course.label;

      if (isCurrentClass(course.slug)) {
        link.classList.add("class-nav__button--active");
        link.setAttribute("aria-current", "page");
      }

      nav.appendChild(link);
    });

    return nav;
  }

  function updateHeaderOffset() {
    var header = document.querySelector(".site-header");
    if (!header) {
      return;
    }

    document.documentElement.style.setProperty(
      "--site-header-offset",
      header.offsetHeight + "px"
    );
  }

  function wrapSiteHeader() {
    var breadcrumb = document.querySelector("main .breadcrumb");
    if (!breadcrumb || breadcrumb.closest(".site-header")) {
      updateHeaderOffset();
      return;
    }

    var parent = breadcrumb.parentNode;
    var root = getRootPrefix();
    var header = document.createElement("header");
    header.className = "site-header";

    var nextElement = breadcrumb.nextElementSibling;
    var existingNav = nextElement && nextElement.classList.contains("class-nav")
      ? nextElement
      : null;

    parent.insertBefore(header, breadcrumb);
    header.appendChild(breadcrumb);

    if (existingNav) {
      header.appendChild(existingNav);
    } else {
      header.appendChild(buildClassNav(root));
    }

    updateHeaderOffset();
  }

  function addVisitCounter() {
    var breadcrumb = document.querySelector(".breadcrumb");
    if (!breadcrumb || breadcrumb.querySelector(".visits")) {
      return;
    }

    var wrap = document.createElement("span");
    wrap.className = "visits";
    wrap.title = "Visits to this page";

    // GitHub Pages is static, so the per-page count comes from the free hits.sh badge service.
    var key = ((location.host || "local") + (location.pathname || "/"))
      .replace(/^\/+|\/+$/g, "");
    var badge = document.createElement("img");
    badge.className = "visits__badge";
    badge.alt = "Visits to this page";
    badge.height = 20;

    badge.onerror = function () {
      badge.hidden = true;
      var storageKey = "visits:" + key;
      var mine = Number(localStorage.getItem(storageKey) || 0) + 1;
      localStorage.setItem(storageKey, String(mine));
      var fallback = document.createElement("span");
      fallback.className = "visits__fallback";
      fallback.textContent = mine + " (this browser only)";
      wrap.appendChild(fallback);
    };

    badge.src = "https://hits.sh/" + encodeURI(key) +
      ".svg?style=flat-square&label=visits&color=174ea6";
    wrap.appendChild(badge);
    breadcrumb.appendChild(wrap);
  }

  wrapSiteHeader();
  addVisitCounter();
  window.addEventListener("resize", updateHeaderOffset);
})();
