import { createDiagram } from "./diagram.js";
import { createQueryBuilder } from "./query-builder.js";
import { setupPanels } from "./panels.js";

setupPanels();

const status = document.getElementById("status");
const resultStatus = document.getElementById("result-status");
const results = document.getElementById("results");
const runButton = document.getElementById("run-query");
const cancelButton = document.getElementById("cancel-query");
let revision = 0;
let hasResult = false;
let activeQuery = null;
let builder;
let database;

function workerRequest(message, timeout, complete) {
  const worker = new Worker(new URL("sqlite-worker.js", import.meta.url));
  let finished = false;
  const timer = setTimeout(() => finish("The query took too long and was stopped."), timeout);
  function finish(error, result) {
    if (finished) return;
    finished = true;
    clearTimeout(timer);
    worker.terminate();
    complete(error, result);
  }
  worker.onmessage = event => finish(event.data.error, event.data.result);
  worker.onerror = event => {
    event.preventDefault();
    finish("SQLite worker failed: " + event.message);
  };
  worker.onmessageerror = () => finish("SQLite worker returned an unreadable response.");
  worker.postMessage(message);
  return () => finish("Query cancelled.");
}

function markChanged() {
  revision++;
  if (hasResult && !activeQuery) resultStatus.textContent = "The query has changed since these results were run.";
}

function showResults(result) {
  const head = document.createElement("thead");
  const header = document.createElement("tr");
  result.columns.forEach(column => {
    const th = document.createElement("th");
    th.scope = "col";
    th.textContent = column;
    header.appendChild(th);
  });
  head.appendChild(header);
  const body = document.createElement("tbody");
  result.values.forEach(row => {
    const tr = document.createElement("tr");
    row.forEach(value => {
      const td = document.createElement("td");
      td.textContent = value === null ? "NULL" : String(value);
      tr.appendChild(td);
    });
    body.appendChild(tr);
  });
  results.replaceChildren(head, body);
}

runButton.addEventListener("click", () => {
  const queryRevision = revision;
  const sql = builder.getSql();
  builder.setBusy(true);
  cancelButton.disabled = false;
  resultStatus.classList.remove("error");
  resultStatus.textContent = "Running query...";
  activeQuery = workerRequest({ type: "query", database, sql }, 15000, (error, result) => {
    activeQuery = null;
    builder.setBusy(false);
    cancelButton.disabled = true;
    if (error) {
      results.replaceChildren();
      hasResult = false;
      resultStatus.classList.add("error");
      resultStatus.textContent = error;
      return;
    }
    showResults(result);
    hasResult = true;
    resultStatus.textContent = `Showing ${result.values.length} row(s)` +
      (result.truncated ? " (limited to the first 500)" : "") +
      (queryRevision !== revision ? ". The query changed while it was running." : ".");
  });
});
cancelButton.addEventListener("click", () => { if (activeQuery) activeQuery(); });

async function initialize() {
  try {
    const response = await fetch(new URL("../casing_specs.db", import.meta.url), { cache: "no-cache" });
    if (!response.ok) throw new Error("Database request returned HTTP " + response.status);
    database = await response.arrayBuffer();
    workerRequest({ type: "inspect", database }, 30000, (error, schema) => {
      if (error) {
        status.classList.add("status--error");
        status.textContent = "Could not inspect the database: " + error;
        return;
      }
      if (!schema.tables.length) {
        status.classList.add("status--error");
        status.textContent = "The database contains no user tables.";
        return;
      }
      builder = createQueryBuilder(schema, markChanged);
      createDiagram(schema, columns => builder.selectColumns(columns));
      status.textContent = `Loaded ${schema.tables.length} tables and ${schema.relationships.length} declared relationships.`;
    });
  } catch (error) {
    status.classList.add("status--error");
    status.textContent = "Could not load the database: " + error.message + ". Serve this page over HTTP.";
    console.error("Database explorer:", error);
  }
}

initialize();
