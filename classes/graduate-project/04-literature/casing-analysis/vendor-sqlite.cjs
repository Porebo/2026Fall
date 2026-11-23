const { copyFileSync, mkdirSync } = require("node:fs");
const { join } = require("node:path");

const source = join(__dirname, "node_modules", "sql.js");
const destination = join(__dirname, "explorer", "vendor");
mkdirSync(destination, { recursive: true });
copyFileSync(join(source, "dist", "sql-wasm.js"), join(destination, "sql-wasm.js"));
copyFileSync(join(source, "dist", "sql-wasm.wasm"), join(destination, "sql-wasm.wasm"));
copyFileSync(join(source, "LICENSE"), join(destination, "LICENSE.sql.js"));
console.log("Copied browser SQLite files and license.");
