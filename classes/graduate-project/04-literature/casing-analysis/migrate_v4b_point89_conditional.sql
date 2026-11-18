-- migrate_v4b_point89_conditional.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v4.txt (Version 4.0)
-- Run after migrate_v4_subdivisions_b_c.sql.
-- Backup taken before running: scratchpad casing_specs.pre-v4b.db
--
-- Student decision (2026-11-18)
--   § 1724.7.1(c) applies only "when multiple boreholes are drilled in a
--   well" and does not require a label. Point 89, (c).borehole_designation
--   (requirement_id 89), is therefore conditional:
--     - more than one borehole shown: scored; MET when each bore is
--       identified and the required information is given for each bore,
--       otherwise MISSING;
--     - single borehole shown: NOT_APPLICABLE, removed from that diagram's
--       denominator (89 -> 88).
--   No other requirement may take NOT_APPLICABLE.
--
-- What this migration does
--   1. Rebuilds diagram_requirement_results so that its CHECK allows
--      status 'NOT_APPLICABLE' for requirement_id 89 only. SQLite cannot
--      alter a CHECK in place. Existing rows are copied unchanged with the
--      same result_id values, so completeness_infractions references stay
--      valid. The three infraction triggers are recreated, and a fourth
--      closes an open infraction if a result is changed to NOT_APPLICABLE.
--   2. Updates the text of requirement 89.
--   3. Replaces casing_final_score: scoring_items = 89 minus the number of
--      NOT_APPLICABLE results for the diagram; percentage = MET / that.
--   4. Adds casing_bc_subtotal: the same calculation for points 79-89
--      (subdivisions (b) and (c)) only.
--
-- W diagrams (out of study): no result row is added or changed; existing
-- rows are copied as they are during the table rebuild.

PRAGMA foreign_keys = OFF;
BEGIN IMMEDIATE;

CREATE TABLE diagram_requirement_results_new (
    result_id INTEGER PRIMARY KEY,
    diagram_number TEXT NOT NULL REFERENCES diagrams(diagram_number),
    requirement_id INTEGER NOT NULL REFERENCES spec_requirements(requirement_id),
    status TEXT NOT NULL CHECK (
        status IN ('MET', 'MISSING')
        OR (status = 'NOT_APPLICABLE' AND requirement_id = 89)
    ),
    evidence TEXT,
    explanation TEXT,
    evaluated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (diagram_number, requirement_id)
);

INSERT INTO diagram_requirement_results_new (
    result_id, diagram_number, requirement_id, status, evidence, explanation, evaluated_at
)
SELECT result_id, diagram_number, requirement_id, status, evidence, explanation, evaluated_at
FROM diagram_requirement_results;

DROP VIEW IF EXISTS casing_final_score;
DROP VIEW IF EXISTS casing_missing_items;
DROP TABLE diagram_requirement_results;
ALTER TABLE diagram_requirement_results_new RENAME TO diagram_requirement_results;

CREATE INDEX IF NOT EXISTS idx_results_diagram_status
    ON diagram_requirement_results(diagram_number, status);

CREATE TRIGGER create_completeness_infraction
AFTER INSERT ON diagram_requirement_results
WHEN NEW.status = 'MISSING'
BEGIN
    INSERT INTO completeness_infractions (result_id)
    VALUES (NEW.result_id);
END;

CREATE TRIGGER update_completeness_infraction
AFTER UPDATE OF status ON diagram_requirement_results
WHEN NEW.status = 'MISSING'
BEGIN
    INSERT OR IGNORE INTO completeness_infractions (result_id)
    VALUES (NEW.result_id);
    UPDATE completeness_infractions
    SET resolution_status = 'OPEN'
    WHERE result_id = NEW.result_id;
END;

CREATE TRIGGER resolve_completeness_infraction
AFTER UPDATE OF status ON diagram_requirement_results
WHEN NEW.status = 'MET'
     AND EXISTS (
         SELECT 1
         FROM completeness_infractions
         WHERE result_id = NEW.result_id
     )
BEGIN
    UPDATE completeness_infractions
    SET resolution_status = 'RESOLVED'
    WHERE result_id = NEW.result_id;
END;

CREATE TRIGGER not_applicable_completeness_infraction
AFTER UPDATE OF status ON diagram_requirement_results
WHEN NEW.status = 'NOT_APPLICABLE'
BEGIN
    UPDATE completeness_infractions
    SET resolution_status = 'NOT_APPLICABLE'
    WHERE result_id = NEW.result_id;
END;

UPDATE spec_requirements
SET requirement_name = 'Borehole designation (original hole, redrill, or sidetrack; conditional: multiple boreholes only)',
    requirement_text = 'Conditional on more than one borehole being shown (14 CCR 1724.7.1(c), "when multiple boreholes are drilled"). Multiple boreholes: MET when each bore is identified and the required information is given for each bore, otherwise MISSING. Single borehole: NOT_APPLICABLE, removed from the denominator (89 -> 88). No label is required for a single bore.'
WHERE requirement_id = 89 AND requirement_code = '(c).borehole_designation';

CREATE VIEW casing_final_score AS
SELECT
    d.diagram_number,
    89 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS not_applicable_items,
    ROUND(
        100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END)
        / (89 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END)),
        1
    ) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code IN ('(a)', '(b)', '(c)')
GROUP BY d.diagram_number;

CREATE VIEW casing_bc_subtotal AS
SELECT
    d.diagram_number,
    11 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS not_applicable_items,
    ROUND(
        100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END)
        / (11 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END)),
        1
    ) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code IN ('(b)', '(c)')
GROUP BY d.diagram_number;

CREATE VIEW casing_missing_items AS
SELECT
    r.diagram_number,
    q.requirement_code,
    q.requirement_name,
    r.status,
    r.evidence,
    r.explanation,
    i.infraction_id
FROM diagram_requirement_results AS r
JOIN spec_requirements AS q USING (requirement_id)
LEFT JOIN completeness_infractions AS i USING (result_id)
WHERE r.status = 'MISSING'
ORDER BY r.diagram_number, q.requirement_code;

COMMIT;
PRAGMA foreign_keys = ON;
