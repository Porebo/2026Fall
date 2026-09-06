(function () {
  var lists = document.querySelectorAll("[data-checklist]");

  lists.forEach(function (list, listIndex) {
    var storageKey = "checklist:" + (list.id || window.location.pathname + ":" + listIndex);
    var saved = {};

    try {
      saved = JSON.parse(localStorage.getItem(storageKey)) || {};
    } catch (error) {
      saved = {};
    }

    list.querySelectorAll('input[type="checkbox"]').forEach(function (checkbox, itemIndex) {
      var itemKey = checkbox.id || String(itemIndex);
      checkbox.checked = saved[itemKey] === true;

      checkbox.addEventListener("change", function () {
        saved[itemKey] = checkbox.checked;
        localStorage.setItem(storageKey, JSON.stringify(saved));
      });
    });
  });
})();