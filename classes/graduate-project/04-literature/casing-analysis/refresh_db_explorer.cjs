const { DatabaseSync } = require("node:sqlite");
const { join } = require("node:path");
const { writeFileSync } = require("node:fs");

const directory = __dirname;
const database = new DatabaseSync(join(directory, "casing_specs.db"), { readOnly: true });

try {
  const rootName = "spec_regulations";
  const quote = name => '"' + name.replace(/"/g, '""') + '"';
  const columns = name => database.prepare("PRAGMA table_info(" + quote(name) + ")").all();
  const foreignKeys = name => database.prepare("PRAGMA foreign_key_list(" + quote(name) + ")").all();
  const rootColumns = columns(rootName);
  const primaryKey = rootColumns.filter(column => column.pk).sort((a, b) => a.pk - b.pk);
  if (!rootColumns.length || !primaryKey.length) {
    throw new Error("The root table or its primary key was not found.");
  }

  function describe(name, tableColumns, keys) {
    const table = quote(name);
    return {
      name,
      columns: tableColumns,
      foreignKeys: keys,
      rowCount: database.prepare("SELECT COUNT(*) AS count FROM " + table).get().count,
      sample: database.prepare("SELECT * FROM " + table + " LIMIT 5").all()
    };
  }

  const tables = database.prepare(
    "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
  ).all();
  function describeRelated(name, parentName, parentColumns) {
    const keys = foreignKeys(name);
    const parentKeys = keys.filter(key => key.table === parentName);
    if (!parentKeys.length) return null;

    const tableColumns = columns(name);
    const parentPrimaryKey = parentColumns.filter(column => column.pk).sort((a, b) => a.pk - b.pk);
    const indexes = database.prepare("PRAGMA index_list(" + quote(name) + ")").all();
    const tablePrimaryKey = tableColumns.filter(column => column.pk);
    const uniqueKeys = [];
    if (tablePrimaryKey.length) uniqueKeys.push(tablePrimaryKey.map(column => column.name));
    indexes.filter(index => index.unique && !index.partial).forEach(function (index) {
      const parts = database.prepare("PRAGMA index_xinfo(" + quote(index.name) + ")").all()
        .filter(part => part.key);
      if (parts.length && parts.every(part => part.cid >= 0)) {
        uniqueKeys.push(parts.map(part => part.name));
      }
    });

    const relationships = parentKeys.map(function (key) {
      const target = key.to === null ? parentPrimaryKey[key.seq] && parentPrimaryKey[key.seq].name : key.to;
      if (!target) throw new Error("Cannot resolve foreign key from " + name + "." + key.from);
      const group = parentKeys.filter(other => other.id === key.id);
      const groupColumns = group.map(other => other.from);
      const required = groupColumns.every(function (columnName) {
        const column = tableColumns.find(item => item.name === columnName);
        if (!column) throw new Error("Cannot find foreign key column " + name + "." + columnName);
        const rowidKey = column.pk && tablePrimaryKey.length === 1 &&
          column.type.toUpperCase() === "INTEGER" && !indexes.some(index => index.origin === "pk");
        return column.notnull || rowidKey;
      });
      const unique = uniqueKeys.some(uniqueKey => uniqueKey.every(column => groupColumns.includes(column)));
      return {
        from: key.from,
        to: target,
        parent: { min: required ? 1 : 0, max: 1 },
        child: { min: 0, max: unique ? 1 : null }
      };
    }).filter(key => parentPrimaryKey.some(column => column.name === key.to));
    return relationships.length ? { ...describe(name, tableColumns, keys), relationships } : null;
  }

  const relatedTables = tables.map(({ name }) => describeRelated(name, rootName, rootColumns)).filter(Boolean);
  const sections = relatedTables.find(table => table.name === "spec_sections");
  if (!sections) throw new Error("spec_sections is not related to the root table.");
  const requirementsTable = describeRelated("spec_requirements", sections.name, sections.columns);
  if (!requirementsTable) throw new Error("spec_requirements is not related to spec_sections.");

  const data = {
    version: 4,
    generatedAt: new Date().toISOString(),
    root: describe(rootName, rootColumns, foreignKeys(rootName)),
    relatedTables,
    requirementsTable
  };
  writeFileSync(join(directory, "db_explorer_data.json"), JSON.stringify(data, null, 2) + "\n");
  console.log("Refreshed the database explorer snapshot.");
} finally {
  database.close();
}
