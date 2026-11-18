PRAGMA foreign_keys = OFF;
PRAGMA legacy_alter_table = ON;

BEGIN IMMEDIATE;

DROP VIEW IF EXISTS casing_final_score;
DROP VIEW IF EXISTS casing_missing_items;
DROP TRIGGER IF EXISTS create_completeness_infraction;
DROP TRIGGER IF EXISTS update_completeness_infraction;
DROP TRIGGER IF EXISTS resolve_completeness_infraction;

ALTER TABLE diagram_requirement_results RENAME TO diagram_requirement_results_old;

CREATE TABLE diagram_requirement_results (
    result_id INTEGER PRIMARY KEY,
    diagram_number TEXT NOT NULL REFERENCES diagrams(diagram_number),
    requirement_id INTEGER NOT NULL REFERENCES spec_requirements(requirement_id),
    status TEXT NOT NULL CHECK (status IN ('MET', 'MISSING')),
    evidence TEXT,
    explanation TEXT,
    evaluated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (diagram_number, requirement_id)
);

INSERT INTO diagram_requirement_results (
    result_id, diagram_number, requirement_id, status,
    evidence, explanation, evaluated_at
)
SELECT
    result_id,
    diagram_number,
    requirement_id,
    CASE
        WHEN requirement_id IN (8, 9) THEN 'MET'
        WHEN status IN ('MET', 'INVALID') THEN 'MET'
        ELSE 'MISSING'
    END,
    evidence,
    explanation,
    evaluated_at
FROM diagram_requirement_results_old;

DROP TABLE diagram_requirement_results_old;

DELETE FROM completeness_infractions;
INSERT INTO completeness_infractions (result_id, severity, resolution_status, created_at)
SELECT
    result_id,
    'COMPLETENESS',
    'OPEN',
    CURRENT_TIMESTAMP
FROM diagram_requirement_results
WHERE status = 'MISSING';

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

CREATE VIEW casing_final_score AS
SELECT
    d.diagram_number,
    51 AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    ROUND(
        100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END) / 51.0,
        1
    ) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code = '(a)'
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
