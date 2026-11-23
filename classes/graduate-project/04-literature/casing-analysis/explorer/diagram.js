function textValue(value) {
  return value === null || value === undefined ? "NULL" : String(value);
}

function cardinalityText(cardinality) {
  if (cardinality.max === 1) return cardinality.min ? "exactly one" : "zero or one";
  return cardinality.min ? "one or many" : "zero or many";
}

export function createDiagram(schema, onColumnChange) {
  const tables = new Map(schema.tables.map(table => [table.name, table]));
  const slots = new Map();
  const positions = new Map();
  const collapsed = new Set();
  const reservedHeights = new Map();
  const selected = new Set();
  const board = document.getElementById("board");
  const viewport = document.getElementById("diagram-viewport");
  const sizer = document.getElementById("board-sizer");
  const svg = document.getElementById("connectors");
  const tooltip = document.getElementById("sample-tooltip");
  const descriptions = document.getElementById("relationship-descriptions");
  const picker = document.getElementById("table-picker");
  const status = document.getElementById("status");
  const clearTables = document.getElementById("clear-tables");
  const zoomOut = document.getElementById("zoom-out");
  const zoomIn = document.getElementById("zoom-in");
  let zoom = 100;
  let layer = 1;
  let sampleField = null;
  let drawPending = false;

  function scheduleDraw() {
    if (drawPending) return;
    drawPending = true;
    requestAnimationFrame(() => { drawPending = false; drawConnectors(); });
  }

  function resizeBoard() {
    let width = Math.max(1100, viewport.clientWidth);
    let height = 850;
    slots.forEach((slot, name) => {
      const position = positions.get(name);
      width = Math.max(width, position.x + slot.offsetWidth + 80);
      height = Math.max(height, position.y + slot.offsetHeight + 80);
    });
    const scale = zoom / 100;
    board.style.width = width + "px";
    board.style.height = height + "px";
    board.style.transform = `scale(${scale})`;
    sizer.style.width = width * scale + "px";
    sizer.style.height = height * scale + "px";
    scheduleDraw();
    positionSample();
  }

  function setZoom(value) {
    const oldScale = zoom / 100;
    const left = viewport.scrollLeft / oldScale;
    const top = viewport.scrollTop / oldScale;
    zoom = Math.max(50, Math.min(200, value));
    document.getElementById("zoom-level").textContent = zoom + "%";
    zoomOut.disabled = zoom === 50;
    zoomIn.disabled = zoom === 200;
    resizeBoard();
    viewport.scrollLeft = left * zoom / 100;
    viewport.scrollTop = top * zoom / 100;
  }

  function place(slot, name, near) {
    const height = Math.max(slot.offsetHeight, reservedHeights.get(name) || 0);
    const rects = [...slots.entries()].filter(([other]) => other !== name && positions.has(other)).map(([other, element]) => ({
      ...positions.get(other), width: element.offsetWidth,
      height: Math.max(element.offsetHeight, reservedHeights.get(other) || 0)
    }));
    const start = near ? Math.max(0, Math.round((near.x - 20) / 380) + 1) % 5 : 0;
    for (let y = near ? Math.max(20, near.y) : 20; ; y += 40) {
      for (let offset = 0; offset < 5; offset++) {
        const x = 20 + ((start + offset) % 5) * 380;
        if (rects.every(rect => x + slot.offsetWidth + 30 <= rect.x ||
          x >= rect.x + rect.width + 30 || y + height + 30 <= rect.y ||
          y >= rect.y + rect.height + 30)) {
          positions.set(name, { x, y });
          slot.style.left = x + "px";
          slot.style.top = y + "px";
          return;
        }
      }
    }
  }

  function move(name, dx, dy) {
    const position = positions.get(name);
    position.x = Math.max(0, position.x + dx);
    position.y = Math.max(0, position.y + dy);
    const slot = slots.get(name);
    slot.style.left = position.x + "px";
    slot.style.top = position.y + "px";
    resizeBoard();
  }

  function makeDraggable(handle, slot, name) {
    let drag = null;
    handle.addEventListener("pointerdown", event => {
      if (event.button !== 0 || drag) return;
      event.preventDefault();
      handle.focus();
      handle.setPointerCapture(event.pointerId);
      drag = { id: event.pointerId, x: event.clientX, y: event.clientY };
      slot.style.zIndex = String(++layer);
      slot.classList.add("table-slot--dragging");
    });
    handle.addEventListener("pointermove", event => {
      if (!drag || event.pointerId !== drag.id) return;
      move(name, (event.clientX - drag.x) / (zoom / 100), (event.clientY - drag.y) / (zoom / 100));
      drag.x = event.clientX;
      drag.y = event.clientY;
    });
    function end(event) {
      if (!drag || event.pointerId !== drag.id) return;
      drag = null;
      slot.classList.remove("table-slot--dragging");
    }
    handle.addEventListener("pointerup", end);
    handle.addEventListener("pointercancel", end);
    handle.addEventListener("lostpointercapture", end);
    handle.addEventListener("keydown", event => {
      const directions = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
      const direction = directions[event.key];
      if (!direction) return;
      event.preventDefault();
      slot.style.zIndex = String(++layer);
      const step = event.shiftKey ? 40 : 10;
      move(name, direction[0] * step, direction[1] * step);
    });
  }

  function hideSample() {
    if (sampleField) sampleField.removeAttribute("aria-describedby");
    sampleField = null;
    tooltip.hidden = true;
  }

  function positionSample() {
    if (!sampleField || tooltip.hidden) return;
    const field = sampleField.getBoundingClientRect();
    const preferred = window.innerWidth - field.right >= tooltip.offsetWidth ? field.right : field.left - tooltip.offsetWidth;
    tooltip.style.left = Math.max(8, Math.min(preferred, window.innerWidth - tooltip.offsetWidth - 8)) + "px";
    tooltip.style.top = Math.max(8, Math.min(field.top, window.innerHeight - tooltip.offsetHeight - 8)) + "px";
  }

  function showSample(field, table, column) {
    if (sampleField && sampleField !== field) sampleField.removeAttribute("aria-describedby");
    sampleField = field;
    field.setAttribute("aria-describedby", tooltip.id);
    const heading = document.createElement("h2");
    heading.textContent = "Data sample - " + table.name + "." + column.name;
    const description = document.createElement("p");
    description.textContent = `Showing ${table.sample.length} of ${table.rowCount} rows in this table.`;
    tooltip.replaceChildren(heading, description);
    if (table.sample.length) {
      const list = document.createElement("ol");
      table.sample.forEach(row => {
        const item = document.createElement("li");
        item.textContent = textValue(row[column.name]);
        list.appendChild(item);
      });
      tooltip.appendChild(list);
    } else {
      const empty = document.createElement("p");
      empty.textContent = "This table has no rows.";
      tooltip.appendChild(empty);
    }
    tooltip.hidden = false;
    positionSample();
  }

  function showRelated(tableName, columnName) {
    const matches = schema.relationships.filter(relationship =>
      (relationship.parent === tableName && relationship.columns.some(column => column.to === columnName)) ||
      (relationship.child === tableName && relationship.columns.some(column => column.from === columnName)));
    if (!matches.length) {
      status.textContent = `No declared foreign keys are connected to ${tableName}.${columnName}.`;
      return;
    }
    const near = positions.get(tableName);
    matches.forEach(relationship => addTable(relationship.child === tableName ? relationship.parent : relationship.child, near));
    status.textContent = `Showing declared relationships for ${tableName}.${columnName}.`;
    scheduleDraw();
  }

  function makeTable(table) {
    const slot = document.createElement("div");
    slot.className = "table-slot";
    slot.dataset.table = table.name;
    const element = document.createElement("table");
    element.className = "er-table";
    const caption = document.createElement("caption");
    const header = document.createElement("div");
    header.className = "table-header";
    const handle = document.createElement("button");
    handle.type = "button";
    handle.className = "drag-handle";
    handle.setAttribute("aria-label", "Move " + table.name + " table. Drag or use arrow keys.");
    handle.title = "Drag to move; use arrow keys for keyboard movement";
    const name = document.createElement("span");
    name.textContent = table.name;
    const grip = document.createElement("span");
    grip.className = "drag-handle__grip";
    grip.setAttribute("aria-hidden", "true");
    grip.textContent = "::";
    handle.append(name, grip);
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "table-toggle";
    header.append(handle, toggle);
    caption.appendChild(header);
    makeDraggable(handle, slot, table.name);
    const head = document.createElement("thead");
    const columnCheckboxes = new Map();
    const heading = document.createElement("th");
    heading.scope = "col";
    const headingContent = document.createElement("div");
    headingContent.className = "table-heading";
    const headingLabel = document.createElement("span");
    headingLabel.textContent = "Select | Key | Column | Type";
    const actions = document.createElement("div");
    actions.className = "table-actions";
    function addColumnAction(label, checked) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.setAttribute("aria-label", label + " columns in " + table.name);
      button.addEventListener("click", () => {
        let changed = false;
        columnCheckboxes.forEach((checkbox, columnKey) => {
          if (checkbox.checked === checked) return;
          checkbox.checked = checked;
          if (checked) selected.add(columnKey);
          else selected.delete(columnKey);
          changed = true;
        });
        if (changed) onColumnChange([...selected].map(key => JSON.parse(key)));
      });
      actions.appendChild(button);
    }
    addColumnAction("Select all", true);
    addColumnAction("Reset", false);
    headingContent.append(headingLabel, actions);
    heading.appendChild(headingContent);
    const headingRow = document.createElement("tr");
    headingRow.appendChild(heading);
    head.appendChild(headingRow);
    const body = document.createElement("tbody");
    body.id = "fields-" + encodeURIComponent(table.name);
    toggle.setAttribute("aria-controls", body.id);
    function updateCollapse() {
      const isCollapsed = collapsed.has(table.name);
      head.hidden = isCollapsed;
      body.hidden = isCollapsed;
      toggle.setAttribute("aria-expanded", String(!isCollapsed));
      toggle.setAttribute("aria-label", (isCollapsed ? "Expand " : "Collapse ") + table.name + " table");
      toggle.textContent = isCollapsed ? "\u25b8" : "\u25be";
    }
    toggle.addEventListener("click", () => {
      if (sampleField && slot.contains(sampleField)) hideSample();
      if (collapsed.has(table.name)) collapsed.delete(table.name);
      else {
        reservedHeights.set(table.name, slot.offsetHeight);
        collapsed.add(table.name);
      }
      updateCollapse();
      resizeBoard();
    });
    table.columns.forEach(column => {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      const fieldRow = document.createElement("div");
      fieldRow.className = "field-row";
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.className = "column-select";
      checkbox.setAttribute("aria-label", `Select ${table.name}.${column.name} for query`);
      const columnKey = JSON.stringify([table.name, column.name]);
      checkbox.checked = selected.has(columnKey);
      columnCheckboxes.set(columnKey, checkbox);
      checkbox.addEventListener("change", () => {
        if (checkbox.checked) selected.add(columnKey);
        else selected.delete(columnKey);
        onColumnChange([...selected].map(key => JSON.parse(key)));
      });
      const field = document.createElement("button");
      field.type = "button";
      field.className = "field";
      field.dataset.table = table.name;
      field.dataset.column = column.name;
      const keys = document.createElement("span");
      keys.className = "field__keys";
      if (column.pk) {
        const badge = document.createElement("span");
        badge.className = "key";
        badge.textContent = "PK";
        badge.title = "Primary key";
        keys.appendChild(badge);
      }
      const foreign = schema.relationships.filter(relationship =>
        relationship.child === table.name && relationship.columns.some(pair => pair.from === column.name));
      if (foreign.length) {
        const badge = document.createElement("span");
        badge.className = "key key--foreign";
        badge.textContent = "FK";
        badge.title = foreign.map(relationship => "References " + relationship.parent).join("; ");
        keys.appendChild(badge);
      }
      const columnName = document.createElement("span");
      columnName.className = "field__name";
      columnName.textContent = column.name;
      const type = document.createElement("span");
      type.className = "field__type";
      type.textContent = column.type || "untyped";
      field.append(keys, columnName, type);
      field.addEventListener("pointerenter", () => showSample(field, table, column));
      field.addEventListener("focus", () => showSample(field, table, column));
      field.addEventListener("pointerleave", event => {
        if (!tooltip.contains(event.relatedTarget) && !(document.activeElement === field && field.matches(":focus-visible"))) hideSample();
      });
      field.addEventListener("blur", () => {
        if (!field.matches(":hover") && !tooltip.matches(":hover")) hideSample();
      });
      field.addEventListener("click", () => {
        if (column.pk || foreign.length || schema.relationships.some(relationship =>
          relationship.parent === table.name && relationship.columns.some(pair => pair.to === column.name))) {
          showRelated(table.name, column.name);
        }
      });
      fieldRow.append(checkbox, field);
      cell.appendChild(fieldRow);
      row.appendChild(cell);
      body.appendChild(row);
    });
    updateCollapse();
    element.append(caption, head, body);
    slot.appendChild(element);
    return slot;
  }

  function addTable(name, near) {
    if (slots.has(name)) return;
    const table = tables.get(name);
    if (!table) throw new Error("Unknown table: " + name);
    const slot = makeTable(table);
    slot.style.visibility = "hidden";
    board.appendChild(slot);
    slots.set(name, slot);
    place(slot, name, near);
    slot.style.visibility = "";
    clearTables.disabled = false;
    resizeBoard();
  }

  function mark(x, y, direction, cardinality, end) {
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", "cardinality-mark");
    group.dataset.end = end;
    group.dataset.min = String(cardinality.min);
    group.dataset.max = cardinality.max === null ? "many" : String(cardinality.max);
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    if (cardinality.max === 1) {
      const at = x + direction * 7;
      path.setAttribute("d", `M ${at} ${y - 7} L ${at} ${y + 7}`);
    } else {
      const point = x + direction * 17;
      const tip = x + direction * 5;
      path.setAttribute("d", `M ${point} ${y} L ${tip} ${y - 7} M ${point} ${y} L ${tip} ${y} M ${point} ${y} L ${tip} ${y + 7}`);
    }
    group.appendChild(path);
    if (cardinality.min === 0) {
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", x + direction * 25);
      circle.setAttribute("cy", y);
      circle.setAttribute("r", "4");
      group.appendChild(circle);
    } else {
      const bar = document.createElementNS("http://www.w3.org/2000/svg", "path");
      const at = x + direction * 25;
      bar.setAttribute("d", `M ${at} ${y - 7} L ${at} ${y + 7}`);
      group.appendChild(bar);
    }
    return group;
  }

  function drawConnectors() {
    svg.replaceChildren();
    descriptions.replaceChildren();
    const origin = svg.getBoundingClientRect();
    function anchor(name, column) {
      const slot = slots.get(name);
      if (collapsed.has(name)) return slot.querySelector("caption");
      return [...slot.querySelectorAll(".field")].find(field => field.dataset.column === column);
    }
    schema.relationships.filter(relationship => slots.has(relationship.parent) && slots.has(relationship.child))
      .forEach(relationship => {
        const parent = anchor(relationship.parent, relationship.columns[0].to);
        const child = anchor(relationship.child, relationship.columns[0].from);
        if (!parent || !child) return;
        const a = parent.getBoundingClientRect();
        const b = child.getBoundingClientRect();
        const leftToRight = a.left + a.width / 2 <= b.left + b.width / 2;
        const scale = zoom / 100;
        const x1 = ((leftToRight ? a.right : a.left) - origin.left) / scale;
        const y1 = (a.top + a.height / 2 - origin.top) / scale;
        const x2 = ((leftToRight ? b.left : b.right) - origin.left) / scale;
        const y2 = (b.top + b.height / 2 - origin.top) / scale;
        const direction = leftToRight ? 1 : -1;
        const start = x1 + direction * 34;
        const end = x2 - direction * 34;
        const bend = (end - start) / 2;
        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.setAttribute("class", "relationship");
        group.dataset.relationship = relationship.id;
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("class", "connector");
        path.setAttribute("d", `M ${x1} ${y1} L ${start} ${y1} C ${start + bend} ${y1}, ${end - bend} ${y2}, ${end} ${y2} L ${x2} ${y2}`);
        const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
        title.textContent = relationship.columns.map(pair => `${relationship.child}.${pair.from} -> ${relationship.parent}.${pair.to}`).join(", ");
        group.append(title, path, mark(x1, y1, direction, relationship.parentCardinality, "parent"),
          mark(x2, y2, -direction, relationship.childCardinality, "child"));
        svg.appendChild(group);
        const description = document.createElement("p");
        description.textContent = `Each ${relationship.child} row references ${cardinalityText(relationship.parentCardinality)} ${relationship.parent} row(s); each ${relationship.parent} row may have ${cardinalityText(relationship.childCardinality)} ${relationship.child} row(s).`;
        descriptions.appendChild(description);
      });
  }

  schema.tables.forEach(table => {
    const option = document.createElement("option");
    option.value = table.name;
    option.textContent = table.name;
    picker.appendChild(option);
  });
  picker.disabled = false;
  document.getElementById("add-table").disabled = false;
  document.getElementById("show-all").disabled = false;
  document.getElementById("reset-layout").disabled = false;
  document.getElementById("add-table").addEventListener("click", () => addTable(picker.value));
  document.getElementById("show-all").addEventListener("click", () => schema.tables.forEach(table => addTable(table.name)));
  clearTables.addEventListener("click", () => {
    hideSample();
    slots.forEach(slot => slot.remove());
    slots.clear();
    positions.clear();
    collapsed.clear();
    reservedHeights.clear();
    layer = 1;
    svg.replaceChildren();
    descriptions.replaceChildren();
    clearTables.disabled = true;
    status.textContent = "Diagram cleared. Query selections are unchanged.";
    resizeBoard();
    viewport.scrollLeft = 0;
    viewport.scrollTop = 0;
  });
  document.getElementById("reset-layout").addEventListener("click", () => {
    positions.clear();
    slots.forEach((slot, name) => place(slot, name));
    resizeBoard();
  });
  zoomOut.addEventListener("click", () => setZoom(zoom - 25));
  zoomIn.addEventListener("click", () => setZoom(zoom + 25));
  tooltip.addEventListener("pointerleave", event => {
    if (sampleField && !sampleField.contains(event.relatedTarget) &&
      !(document.activeElement === sampleField && sampleField.matches(":focus-visible"))) hideSample();
  });
  document.addEventListener("keydown", event => {
    if (!sampleField || tooltip.hidden) return;
    if (event.key === "Escape") hideSample();
    else if (document.activeElement === sampleField && (event.key === "ArrowDown" || event.key === "ArrowUp") &&
      tooltip.scrollHeight > tooltip.clientHeight) {
      event.preventDefault();
      tooltip.scrollBy(0, event.key === "ArrowDown" ? 40 : -40);
    }
  });
  window.addEventListener("scroll", positionSample, true);
  window.addEventListener("resize", resizeBoard);
  new ResizeObserver(() => {
    if (!viewport.clientWidth || !viewport.clientHeight) hideSample();
    else resizeBoard();
  }).observe(viewport);
  addTable(tables.has("spec_regulations") ? "spec_regulations" : schema.tables[0].name);
  setZoom(100);
}
