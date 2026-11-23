importScripts("vendor/sql-wasm.js");

const quote = name => '"' + name.replace(/"/g, '""') + '"';
const displayValue = value => value instanceof Uint8Array ? `[BLOB: ${value.length} bytes]` : value;

function rows(db, sql) {
  const result = db.exec(sql)[0];
  if (!result) return [];
  return result.values.map(values => Object.fromEntries(result.columns.map((name, i) => [name, values[i]])));
}

function inspect(db) {
  const names = rows(db, "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name");
  const tables = names.map(({ name }) => {
    const columns = rows(db, "PRAGMA table_info(" + quote(name) + ")");
    const indexes = rows(db, "PRAGMA index_list(" + quote(name) + ")");
    const primary = columns.filter(column => column.pk).sort((a, b) => a.pk - b.pk);
    const uniqueKeys = primary.length ? [primary.map(column => column.name)] : [];
    indexes.filter(index => index.unique && !index.partial).forEach(index => {
      const parts = rows(db, "PRAGMA index_xinfo(" + quote(index.name) + ")").filter(part => part.key);
      if (parts.length && parts.every(part => part.cid >= 0)) uniqueKeys.push(parts.map(part => part.name));
    });
    const sample = rows(db, "SELECT * FROM " + quote(name) + " LIMIT 5")
      .map(row => Object.fromEntries(Object.entries(row).map(([key, value]) => [key, displayValue(value)])));
    return {
      name, columns, indexes, uniqueKeys, primary,
      foreignKeys: rows(db, "PRAGMA foreign_key_list(" + quote(name) + ")"),
      rowCount: rows(db, "SELECT COUNT(*) AS count FROM " + quote(name))[0].count,
      sample
    };
  });
  const byName = new Map(tables.map(table => [table.name, table]));
  const relationships = [];
  tables.forEach(table => {
    const ids = [...new Set(table.foreignKeys.map(key => key.id))];
    ids.forEach(id => {
      const group = table.foreignKeys.filter(key => key.id === id).sort((a, b) => a.seq - b.seq);
      const parent = byName.get(group[0].table);
      if (!parent) throw new Error("Foreign key in " + table.name + " references missing table " + group[0].table);
      const columns = group.map(key => {
        const target = key.to === null ? parent.primary[key.seq]?.name : key.to;
        if (!target || !table.columns.some(column => column.name === key.from)) {
          throw new Error("Cannot resolve foreign key in " + table.name);
        }
        return { from: key.from, to: target };
      });
      const groupColumns = columns.map(column => column.from);
      const required = groupColumns.every(name => {
        const column = table.columns.find(item => item.name === name);
        const rowidKey = column.pk && table.primary.length === 1 &&
          column.type.toUpperCase() === "INTEGER" && !table.indexes.some(index => index.origin === "pk");
        return column.notnull || rowidKey;
      });
      const unique = table.uniqueKeys.some(key => key.every(name => groupColumns.includes(name)));
      relationships.push({
        id: table.name + ":" + id,
        child: table.name,
        parent: parent.name,
        columns,
        parentCardinality: { min: required ? 1 : 0, max: 1 },
        childCardinality: { min: 0, max: unique ? 1 : null }
      });
    });
  });
  return { tables, relationships };
}

function query(db, sql) {
  const leading = sql.replace(/^(?:\s|--[^\n]*(?:\n|$)|\/\*[\s\S]*?\*\/)*/, "");
  if (!/^(select|with)\b/i.test(leading)) {
    throw new Error("Only a single SELECT or WITH query is allowed.");
  }
  const iterator = db.iterateStatements(sql);
  const first = iterator.next();
  if (first.done) throw new Error("Enter a SELECT query.");
  const statement = first.value;
  const columns = statement.getColumnNames();
  if (!columns.length) throw new Error("The statement must return rows.");
  const values = [];
  while (values.length < 500 && statement.step()) values.push(statement.get().map(displayValue));
  const truncated = values.length === 500 && statement.step();
  if (!iterator.next().done) throw new Error("Only one SQL statement is allowed.");
  return { columns, values, truncated };
}

self.onmessage = async event => {
  let db;
  try {
    const SQL = await initSqlJs({
      locateFile: file => new URL("vendor/" + file, self.location.href).href
    });
    db = new SQL.Database(new Uint8Array(event.data.database));
    db.run("PRAGMA query_only = ON");
    const result = event.data.type === "inspect" ? inspect(db) : query(db, event.data.sql);
    self.postMessage({ result });
  } catch (error) {
    self.postMessage({ error: error instanceof Error ? error.message : String(error) });
  } finally {
    if (db) db.close();
  }
};
