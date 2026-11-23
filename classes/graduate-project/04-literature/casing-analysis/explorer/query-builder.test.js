import test from "node:test";
import assert from "node:assert/strict";
import { buildQuery } from "./query-builder.js";

const edge = (id, child, parent, columns = [{ from: "parent_id", to: "id" }]) =>
  ({ id, child, parent, columns });
const selection = [["a", "id"], ["c", "name"]];

test("selects qualified columns without aliases, even when names repeat", () => {
  const schema = { relationships: [edge("c-a", "c", "a")] };
  const result = buildQuery(schema, [["a", "id"], ["c", "id"]], new Set(), "INNER JOIN");
  assert.equal(result.sql, 'SELECT\n  "a"."id",\n  "c"."id"\nFROM "a"\nINNER JOIN "c" ON "c"."parent_id" = "a"."id";');
});

test("builds a composite-key join through an intermediate table", () => {
  const schema = { relationships: [
    edge("b-a", "b", "a", [{ from: "a1", to: "id1" }, { from: "a2", to: "id2" }]),
    edge("c-b", "c", "b")
  ] };
  const result = buildQuery(schema, selection, new Set(), "LEFT JOIN");
  assert.match(result.sql, /LEFT JOIN "b" ON "b"\."a1" = "a"\."id1" AND "b"\."a2" = "a"\."id2"/);
  assert.match(result.sql, /LEFT JOIN "c" ON "c"\."parent_id" = "b"\."id"/);
});

test("prefers a direct key relationship over an indirect path", () => {
  const schema = { relationships: [edge("b-a", "b", "a"), edge("c-b", "c", "b"), edge("c-a", "c", "a")] };
  const automatic = buildQuery(schema, selection, new Set(), "INNER JOIN");
  assert.match(automatic.sql, /INNER JOIN "c" ON "c"\."parent_id" = "a"\."id"/);
  assert.doesNotMatch(automatic.sql, /JOIN "b"/);
  const chosen = buildQuery(schema, selection, new Set(["b-a", "c-b"]), "INNER JOIN");
  assert.match(chosen.sql, /INNER JOIN "b"/);
  assert.match(chosen.sql, /INNER JOIN "c" ON "c"\."parent_id" = "b"\."id"/);
});

test("requires explicit choices when direct relationships are ambiguous", () => {
  const schema = { relationships: [
    edge("c-a", "c", "a"), edge("c-a-other", "c", "a", [{ from: "other_id", to: "id" }]),
    edge("b-a", "b", "a"), edge("c-b", "c", "b")
  ] };
  assert.throws(() => buildQuery(schema, selection, new Set(), "INNER JOIN"), /Multiple join paths/);
  const result = buildQuery(schema, selection, new Set(["c-a"]), "INNER JOIN");
  assert.match(result.sql, /INNER JOIN "c"/);
  assert.doesNotMatch(result.sql, /JOIN "b"/);
  assert.throws(() => buildQuery(schema, selection, new Set(["b-a"]), "INNER JOIN"), /do not connect/);
  assert.throws(() => buildQuery(schema, selection, new Set(["c-a", "b-a", "c-b"]), "INNER JOIN"), /cycle/);
});

test("requires explicit choices when multiple indirect paths exist", () => {
  const schema = { relationships: [
    edge("b-a", "b", "a"), edge("c-b", "c", "b"),
    edge("d-a", "d", "a"), edge("c-d", "c", "d")
  ] };
  assert.throws(() => buildQuery(schema, selection, new Set(), "INNER JOIN"), /Multiple join paths/);
});

test("does not choose between direct relationships from different joined tables", () => {
  const schema = { relationships: [edge("b-a", "b", "a"), edge("c-a", "c", "a"), edge("c-b", "c", "b")] };
  assert.throws(() => buildQuery(schema, [["a", "id"], ["b", "id"], ["c", "id"]], new Set(), "INNER JOIN"), /Multiple join paths/);
});

test("reports disconnected selections rather than inventing a cross join", () => {
  assert.throws(() => buildQuery({ relationships: [edge("b-a", "b", "a")] }, selection, new Set(), "INNER JOIN"), /No declared foreign-key path/);
});
