-- migrate_v41_cement_job_identification.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v4.1.txt (Version 4.1)
-- Run after migrate_v4c_b_reference_rule.sql.
-- Backup taken before running: scratchpad casing_specs.pre-v4.1.db
--
-- Student decision (2026-11-18)
--   § 1724.7.1(b)(2) requires the slurry information "for each cement job
--   completed in each well." A scored point is added for cement job
--   identification: the date, stage number, or job name that identifies each
--   cement job (e.g., U01 shows "8/1/2013" and "8/11/2013" on its cement
--   entries). MET when every cement job shown is identified (any indication,
--   including "N/A"); blank or not mentioned is MISSING. Non-depth; no TVD.
--
-- Numbering
--   Checklist v4.1 inserts this as point 81 (first (b)(2) point); former
--   points 81-89 become 82-90. Database ids are NOT renumbered (results
--   reference them): the new record is appended as requirement_id 90.
--   Checklist-to-id map (v4.1):
--     points  1-78 -> ids 1-51, 88, 62-87 (unchanged)
--     points 79-80 -> ids 52-53
--     point     81 -> id 90 (new)
--     points 82-89 -> ids 54-61
--     point     90 -> id 89 (conditional borehole designation;
--                     NOT_APPLICABLE still allowed for id 89 only)
--
-- Views
--   casing_final_score: 90 minus NOT_APPLICABLE results (90 or 89).
--   casing_bc_subtotal: 12 minus NOT_APPLICABLE results (12 or 11).
--
-- W diagrams (out of study): no result row is added or changed.

PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

INSERT INTO spec_requirements (
    requirement_id, section_id, requirement_code, requirement_name,
    requirement_text, scope_type, is_conditional
) VALUES (
    90, 2, '(b)(2).cement_job_identification',
    'Cement job identification (date or stage)',
    'Date, stage number, or job name identifying each cement job (e.g., 8/1/2013, Stage 1, Primary, Squeeze). MET when every cement job shown is identified, including N/A; blank or not mentioned is MISSING. Also MET when the diagram states or shows that this information accompanies it separately (e.g., "cement calculations attached", "see directional survey", "slurry details in cement report"). Non-depth; no TVD pair.',
    'CEMENT_JOB', 0
);

DROP VIEW IF EXISTS casing_final_score;
CREATE VIEW casing_final_score AS
SELECT
    d.diagram_number,
    90 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS not_applicable_items,
    ROUND(
        100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END)
        / (90 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END)),
        1
    ) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code IN ('(a)', '(b)', '(c)')
GROUP BY d.diagram_number;

DROP VIEW IF EXISTS casing_bc_subtotal;
CREATE VIEW casing_bc_subtotal AS
SELECT
    d.diagram_number,
    12 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END) AS not_applicable_items,
    ROUND(
        100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END)
        / (12 - COUNT(CASE WHEN r.status = 'NOT_APPLICABLE' THEN 1 END)),
        1
    ) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code IN ('(b)', '(c)')
GROUP BY d.diagram_number;

UPDATE spec_sections
SET section_text = 'Each casing diagram shall be accompanied by the listed documentation. Scored from checklist v4.1 (points 79-89): MET when the published diagram shows the information or states that it accompanies the diagram separately; MISSING when it neither shows nor references it.'
WHERE section_id = 2 AND section_code = '(b)';

UPDATE spec_requirements
SET requirement_text = REPLACE(requirement_text, 'removed from the denominator (89 -> 88)', 'removed from the denominator (90 -> 89)')
WHERE requirement_id = 89;

COMMIT;
