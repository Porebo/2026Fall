(function () {
  var siteRoot = new URL("../", document.currentScript.src).href;
  var CLASSES = [
    { label: "Graduate Project", slug: "graduate-project", home: "home-graduate-project.html",
      icon: "<path d=\"M3 7h7l2 2h9v10H3z\"/><path d=\"m9 14 2 2 4-4\"/>" },
    { label: "Principles of IQ", slug: "principles-of-iq", home: "home-principles-of-iq.html",
      icon: "<path d=\"M12 3 20 6v5c0 5-3 8-8 10-5-2-8-5-8-10V6z\"/><path d=\"m8.5 12 2.5 2.5 4.5-5\"/>" },
    { label: "Research Methods", slug: "research-methods", home: "home-research-methods.html",
      icon: "<path d=\"m10 3 4 2-3 6-4-2zM9 10l-1 2M14 7a6 6 0 0 1-1 11H7M5 21h14M5 18h10\"/><circle cx=\"14\" cy=\"7\" r=\"1\"/>" },
    { label: "Master Thesis", slug: "master-thesis", home: "home-master-thesis.html",
      icon: "<path d=\"M12 6c-2-2-5-2-9-2v14c4 0 7 0 9 2 2-2 5-2 9-2V4c-4 0-7 0-9 2zM12 6v14\"/>" }
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

  function setActivityIconAndLabel(element, label, icon) {
    element.setAttribute("aria-label", label);
    element.innerHTML = "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\">" + icon + "</svg>";

    var tooltip = document.createElement("span");
    tooltip.className = "activity-bar__tooltip";
    tooltip.setAttribute("aria-hidden", "true");
    tooltip.textContent = label;
    element.appendChild(tooltip);
  }

  function createActivityLink(label, href, icon) {
    var link = document.createElement("a");
    link.className = "activity-bar__link";
    link.href = href;
    setActivityIconAndLabel(link, label, icon);
    return link;
  }

  function addActivityBar() {
    var root = siteRoot;
    var storageKey = "activity-bar-expanded:" + new URL(root).pathname;
    var nav = document.createElement("nav");
    nav.className = "activity-bar";
    nav.setAttribute("aria-label", "Site navigation");

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "activity-bar__link activity-bar__toggle";
    nav.appendChild(toggle);

    var home = createActivityLink("Home", root + "index.html",
      "<path d=\"M3 11.5 12 4l9 7.5M5.5 10v9h5v-5h3v5h5v-9\"/>");
    if (home.pathname.replace(/\/index\.html$/, "/") === window.location.pathname.replace(/\/index\.html$/, "/")) {
      home.classList.add("activity-bar__link--active");
      home.setAttribute("aria-current", "page");
    }
    nav.appendChild(home);

    CLASSES.forEach(function (course) {
      var link = createActivityLink(course.label, root + "classes/" + course.slug + "/" + course.home, course.icon);
      if (isCurrentClass(course.slug)) {
        link.classList.add("activity-bar__link--active");
        if (link.pathname === window.location.pathname) {
          link.setAttribute("aria-current", "page");
        }
      }
      nav.appendChild(link);
    });

    document.body.insertBefore(nav, document.body.firstChild);
    document.body.classList.add("has-activity-bar");

    function setExpanded(expanded) {
      document.body.classList.toggle("has-activity-bar--expanded", expanded);
      toggle.setAttribute("aria-expanded", String(expanded));
      setActivityIconAndLabel(toggle, expanded ? "Collapse navigation" : "Expand navigation",
        expanded ? "<path d=\"m15 5-7 7 7 7\"/>" : "<path d=\"m9 5 7 7-7 7\"/>");
      updateHeaderOffset();
    }

    var saved = null;
    try {
      saved = window.localStorage.getItem(storageKey);
    } catch (error) {
      console.warn("Could not read the navigation preference:", error);
    }
    if (saved !== null && saved !== "true" && saved !== "false") {
      console.warn("Invalid navigation preference:", saved);
    }
    setExpanded(saved === "true");

    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") !== "true";
      setExpanded(expanded);
      try {
        window.localStorage.setItem(storageKey, String(expanded));
      } catch (error) {
        console.warn("Could not save the navigation preference:", error);
      }
    });

    window.addEventListener("storage", function (event) {
      if (event.key === storageKey || event.key === null) {
        setExpanded(event.newValue === "true");
      }
    });
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

    wrap.appendChild(badge);

    if (location.protocol === "file:") {
      badge.onerror();
    } else {
      badge.src = "https://hits.sh/" + encodeURI(key) +
        ".svg?style=flat-square&label=visits&color=174ea6";
    }

    breadcrumb.appendChild(wrap);
  }

  function addCopyButtons() {
    document.querySelectorAll(".sourceCode").forEach(function (codeBlock) {
      if (codeBlock.parentElement.closest(".sourceCode") ||
          codeBlock.querySelector(".copy-code-button")) {
        return;
      }

      var button = document.createElement("button");
      button.className = "copy-code-button";
      button.type = "button";
      button.textContent = "Copy SQL";
      codeBlock.insertBefore(button, codeBlock.firstChild);
    });

    document.querySelectorAll(".copy-code-button").forEach(function (button) {
      button.addEventListener("click", function () {
        var targetId = button.getAttribute("data-copy-target");
        var target = targetId ? document.getElementById(targetId) : null;
        var text = target ? target.value : button.parentNode.querySelector("code").textContent;
        if (!text) {
          return;
        }

        function showCopied() {
          button.textContent = "Copied";
          window.setTimeout(function () {
            button.textContent = "Copy SQL";
          }, 1500);
        }

        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(showCopied);
          return;
        }

        var fallback = document.createElement("textarea");
        fallback.value = text;
        fallback.setAttribute("readonly", "");
        fallback.style.position = "fixed";
        fallback.style.opacity = "0";
        document.body.appendChild(fallback);
        fallback.select();
        document.execCommand("copy");
        fallback.remove();
        window.getSelection().removeAllRanges();
        showCopied();
      });
    });
  }

  function addCollapsibleSubsections() {
    document.querySelectorAll(".entity-subsection").forEach(function (section) {
      var heading = section.querySelector("h4");
      if (!heading) {
        return;
      }

      var toggle = document.createElement("button");
      toggle.className = "subsection-toggle";
      toggle.type = "button";
      toggle.setAttribute("aria-expanded", "true");
      toggle.textContent = heading.textContent;
      heading.replaceWith(toggle);

      toggle.addEventListener("click", function () {
        var isCollapsed = section.classList.toggle("is-collapsed");
        toggle.setAttribute("aria-expanded", String(!isCollapsed));
      });
    });
  }

  function addCollapsibleCards() {
    document.querySelectorAll(".constraint-card").forEach(function (card) {
      var heading = card.querySelector(":scope > h3");
      if (!heading || heading.querySelector(".card-toggle")) {
        return;
      }

      var title = heading.textContent.trim();
      var toggle = document.createElement("button");
      toggle.className = "card-toggle";
      toggle.type = "button";
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Collapse " + title);
      heading.appendChild(toggle);

      toggle.addEventListener("click", function () {
        var isCollapsed = card.classList.toggle("is-collapsed");
        toggle.setAttribute("aria-expanded", String(!isCollapsed));
        toggle.setAttribute(
          "aria-label",
          (isCollapsed ? "Expand " : "Collapse ") + title
        );
      });
    });
  }

  addActivityBar();
  if (document.querySelector(".breadcrumb")) {
    wrapSiteHeader();
    addVisitCounter();
    addCopyButtons();
    addCollapsibleSubsections();
    addCollapsibleCards();
  }
  window.addEventListener("resize", updateHeaderOffset);
})();
