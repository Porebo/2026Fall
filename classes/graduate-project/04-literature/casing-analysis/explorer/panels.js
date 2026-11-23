function makeSplitter(handle, container, panel, property, vertical) {
  function availableSize() {
    const style = getComputedStyle(container);
    return vertical
      ? container.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight)
      : container.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);
  }

  function bounds(size) {
    const min = Math.min(vertical ? 280 : 160, size * .35);
    const otherMin = Math.min(vertical ? 330 : 120, size * .35);
    const handleSize = vertical ? handle.offsetWidth : handle.offsetHeight;
    return { min, max: Math.max(min, size - otherMin - handleSize) };
  }

  function setSize(value) {
    const available = availableSize();
    if (!available) return;
    const { min, max } = bounds(available);
    const size = Math.max(min, Math.min(max, value));
    const percent = size / available * 100;
    container.style.setProperty(property, percent + "%");
    handle.setAttribute("aria-valuemin", String(Math.round(min / available * 100)));
    handle.setAttribute("aria-valuemax", String(Math.round(max / available * 100)));
    handle.setAttribute("aria-valuenow", String(Math.round(percent)));
  }

  let drag = null;
  handle.addEventListener("pointerdown", event => {
    if (event.button !== 0 || drag) return;
    event.preventDefault();
    handle.focus();
    handle.setPointerCapture(event.pointerId);
    drag = {
      id: event.pointerId,
      coordinate: vertical ? event.clientX : event.clientY,
      size: vertical ? panel.offsetWidth : panel.offsetHeight
    };
  });
  handle.addEventListener("pointermove", event => {
    if (!drag || drag.id !== event.pointerId) return;
    setSize(drag.size + (vertical ? event.clientX : event.clientY) - drag.coordinate);
  });
  function endDrag(event) {
    if (drag && drag.id === event.pointerId) drag = null;
  }
  handle.addEventListener("pointerup", endDrag);
  handle.addEventListener("pointercancel", endDrag);
  handle.addEventListener("lostpointercapture", endDrag);
  handle.addEventListener("keydown", event => {
    const negative = vertical ? "ArrowLeft" : "ArrowUp";
    const positive = vertical ? "ArrowRight" : "ArrowDown";
    if (event.key !== negative && event.key !== positive) return;
    event.preventDefault();
    const current = vertical ? panel.offsetWidth : panel.offsetHeight;
    const step = event.shiftKey ? 80 : 20;
    setSize(current + (event.key === positive ? step : -step));
  });
  setSize(vertical ? panel.offsetWidth : panel.offsetHeight);
}

export function setupPanels() {
  const workspace = document.getElementById("workspace");
  const rightPanels = document.getElementById("right-panels");
  const diagramPanel = document.getElementById("diagram-panel");
  const queryPanel = document.getElementById("query-panel");
  const resultsPanel = document.getElementById("results-panel");
  const diagramSplitter = document.getElementById("diagram-splitter");
  const querySplitter = document.getElementById("query-splitter");

  document.querySelectorAll(".panel-toggle").forEach(button => {
    const name = button.dataset.panel;
    const panel = document.getElementById(name + "-panel");
    const content = document.getElementById(name + "-content");
    button.addEventListener("click", () => {
      const collapsed = button.getAttribute("aria-expanded") === "true";
      panel.classList.toggle("is-collapsed", collapsed);
      content.hidden = collapsed;
      button.setAttribute("aria-expanded", String(!collapsed));
      button.setAttribute("aria-label", (collapsed ? "Expand " : "Collapse ") + name + " panel");
      button.title = button.getAttribute("aria-label");
      button.textContent = collapsed ? "+" : "\u2212";
      diagramSplitter.hidden = diagramPanel.classList.contains("is-collapsed");
      querySplitter.hidden = queryPanel.classList.contains("is-collapsed") || resultsPanel.classList.contains("is-collapsed");
      rightPanels.classList.toggle("results-collapsed", resultsPanel.classList.contains("is-collapsed"));
    });
  });

  makeSplitter(diagramSplitter, workspace, diagramPanel, "--diagram-size", true);
  makeSplitter(querySplitter, rightPanels, queryPanel, "--query-size", false);
}
