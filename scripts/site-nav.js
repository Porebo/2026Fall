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

  wrapSiteHeader();
  addVisitCounter();
  addCopyButtons();
  addCollapsibleSubsections();
  addCollapsibleCards();
  window.addEventListener("resize", updateHeaderOffset);
})();
