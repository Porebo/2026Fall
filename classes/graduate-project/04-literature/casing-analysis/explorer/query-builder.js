const quote = name => '"' + name.replace(/"/g, '""') + '"';

function otherEnd(edge, name) {
  if (edge.child === name && edge.parent !== name) return edge.parent;
  if (edge.parent === name && edge.child !== name) return edge.child;
  return null;
}

function findPaths(relationships, joined, target) {
  const direct = relationships.filter(edge =>
    (edge.child === target && joined.has(edge.parent)) ||
    (edge.parent === target && joined.has(edge.child)));
  if (direct.length) return direct.map(edge => [{ edge, next: target }]);

  const paths = [];
  function walk(current, visited, path) {
    if (paths.length >= 2) return;
    if (current === target) {
      paths.push(path);
      return;
    }
    relationships.forEach(edge => {
      const next = otherEnd(edge, current);
      if (!next || visited.has(next)) return;
      const nextVisited = new Set(visited);
      nextVisited.add(next);
      walk(next, nextVisited, [...path, { edge, next }]);
    });
  }
  joined.forEach(start => walk(start, new Set(joined), []));
  return paths;
}

function chosenPath(relationships, selectedTables, chosenIds) {
  const chosen = relationships.filter(edge => chosenIds.has(edge.id));
  if (chosen.some(edge => edge.child === edge.parent)) {
    throw new Error("Self-joins require aliases. Use Edit SQL for this relationship.");
  }
  const joined = new Set([selectedTables[0]]);
  const edges = [];
  const used = new Set();
  const queue = [selectedTables[0]];
  while (queue.length) {
    const current = queue.shift();
    chosen.forEach(edge => {
      if (used.has(edge.id)) return;
      const next = otherEnd(edge, current);
      if (!next) return;
      if (joined.has(next)) throw new Error("The chosen relationships form a cycle. Remove a relationship or use Edit SQL.");
      used.add(edge.id);
      joined.add(next);
      queue.push(next);
      edges.push({ edge, next });
    });
  }
  if (selectedTables.some(name => !joined.has(name))) {
    throw new Error("The chosen relationships do not connect every selected table. Choose the complete path, including intermediate tables.");
  }
  if (used.size !== chosen.length) throw new Error("Some chosen relationships are disconnected from the first selected table.");
  return edges;
}

export function buildQuery(schema, selected, chosenIds, joinType) {
  if (!selected.length) return { sql: "", message: "Select columns to build a query." };
  const selectedTables = [...new Set(selected.map(([table]) => table))];
  let edges;
  if (chosenIds.size) {
    edges = chosenPath(schema.relationships, selectedTables, chosenIds);
  } else {
    const joined = new Set([selectedTables[0]]);
    edges = [];
    for (const target of selectedTables.slice(1)) {
      if (joined.has(target)) continue;
      const paths = findPaths(schema.relationships, joined, target);
      if (!paths.length) throw new Error(`No declared foreign-key path connects ${target} to the selected tables.`);
      if (paths.length > 1) throw new Error(`Multiple join paths connect ${target}. Choose the relationships below.`);
      paths[0].forEach(part => {
        joined.add(part.next);
        edges.push(part);
      });
    }
  }
  const select = selected.map(([table, column]) =>
    `  ${quote(table)}.${quote(column)}`).join(",\n");
  const joins = edges.map(({ edge, next }) => {
    const conditions = edge.columns.map(pair =>
      `${quote(edge.child)}.${quote(pair.from)} = ${quote(edge.parent)}.${quote(pair.to)}`).join(" AND ");
    return `${joinType} ${quote(next)} ON ${conditions}`;
  });
  const sql = [`SELECT\n${select}`, `FROM ${quote(selectedTables[0])}`, ...joins].join("\n") + ";";
  return { sql, message: `Visual query: ${selected.length} column(s), ${edges.length} ${joinType.toLowerCase()}(s). First table: ${selectedTables[0]}.` };
}

export function createQueryBuilder(schema, onChange) {
  const editor = document.getElementById("sql-editor");
  const status = document.getElementById("query-status");
  const edit = document.getElementById("edit-sql");
  const visual = document.getElementById("visual-sql");
  const run = document.getElementById("run-query");
  const joinType = document.getElementById("join-type");
  const details = document.getElementById("join-details");
  const options = document.getElementById("join-options");
  const chosen = new Set();
  let selected = [];
  let manual = false;
  let busy = false;
  let visualSql = "";
  let visualError = "";

  function refresh() {
    try {
      const result = buildQuery(schema, selected, chosen, joinType.value);
      visualSql = result.sql;
      visualError = "";
      status.textContent = manual ? "Manual SQL mode. " + result.message : result.message;
    } catch (error) {
      visualSql = "";
      visualError = error.message;
      status.textContent = (manual ? "Manual SQL mode. Visual builder: " : "") + error.message;
      if (error.message.includes("Multiple join paths")) details.open = true;
    }
    status.classList.toggle("error", !!visualError);
    if (!manual) editor.value = visualSql;
    editor.readOnly = !manual;
    document.getElementById("sql-mode").textContent = manual ? "(manual mode)" : "(visual mode)";
    edit.disabled = manual;
    visual.disabled = !manual;
    run.disabled = busy || !editor.value.trim() || (!manual && !!visualError);
    onChange();
  }

  schema.relationships.forEach(edge => {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.dataset.relationship = edge.id;
    input.addEventListener("change", () => {
      if (input.checked) chosen.add(edge.id);
      else chosen.delete(edge.id);
      refresh();
    });
    const description = document.createTextNode(" " + edge.columns.map(pair =>
      `${edge.child}.${pair.from} -> ${edge.parent}.${pair.to}`).join(" AND "));
    label.append(input, description);
    options.appendChild(label);
  });
  document.getElementById("clear-joins").addEventListener("click", () => {
    chosen.clear();
    options.querySelectorAll("input").forEach(input => { input.checked = false; });
    refresh();
  });
  joinType.addEventListener("change", refresh);
  edit.addEventListener("click", () => {
    manual = true;
    refresh();
    editor.focus();
  });
  visual.addEventListener("click", () => {
    manual = false;
    refresh();
  });
  editor.addEventListener("input", () => {
    run.disabled = busy || !editor.value.trim();
    onChange();
  });
  refresh();
  return {
    selectColumns(columns) { selected = columns; refresh(); },
    getSql() { return editor.value; },
    setBusy(value) { busy = value; run.disabled = busy || !editor.value.trim() || (!manual && !!visualError); }
  };
}
