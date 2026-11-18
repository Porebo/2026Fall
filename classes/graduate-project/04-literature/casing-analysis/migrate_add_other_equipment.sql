-- migrate_add_other_equipment.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v3.txt (Version 3.0)
--
-- Purpose
--   14 CCR § 1724.7.1(a)(10) reads "Information regarding equipment in the
--   well such as subsurface safety valves, packers, and gas lift mandrels."
--   "Such as" makes the list illustrative, not exhaustive. Checklist v2
--   decomposed (a)(10) into only the three named examples (requirement_id
--   29-31). This migration adds one presence-only, non-depth requirement for
--   any other in-well equipment, mirroring (a)(9).other_integrity_feature
--   (requirement_id 28). It has no TVD pair.
--
-- Scoring rule (presence-only)
--   MET when the diagram supplies information on in-well equipment other than
--   SSSVs, packers, and gas-lift mandrels (e.g., tubing, pumps, rods),
--   including an explicit "none" or "N/A". A blank label is MISSING.
--
-- Numbering
--   requirement_id is appended as 88. Existing ids are NOT renumbered because
--   diagram_requirement_results.requirement_id (and, through result_id,
--   completeness_infractions) reference them, and DB ids already differ from
--   checklist display numbers (checklist 52-77 = DB ids 62-87). The checklist
--   v3 display number for this point is 32.
--
-- Scoring denominator
--   casing_final_score changes from 77 to 78 subdivision (a) items.
--
-- W01 (out-of-study practice diagram)
--   No W01 result is recorded: W01 is out of study (2026-11-18).

PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

INSERT INTO spec_requirements (
    requirement_id, section_id, requirement_code, requirement_name,
    requirement_text, scope_type, is_conditional
) VALUES (
    88, 1, '(a)(10).other_equipment',
    'Other equipment in the well (e.g., tubing, pumps, rods)',
    'Information regarding equipment in the well other than subsurface safety valves, packers, and gas-lift mandrels; the regulation''s list is illustrative ("such as").',
    'WELLBORE', 1
);

DROP VIEW IF EXISTS casing_final_score;
CREATE VIEW casing_final_score AS
SELECT
    d.diagram_number,
    78 AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    ROUND(100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END) / 78.0, 1) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code = '(a)'
GROUP BY d.diagram_number;

COMMIT;
