-- migrate_v4_subdivisions_b_c.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v4.txt (Version 4.0)
-- Backup taken before running: scratchpad casing_specs.pre-v4.db
--
-- Purpose
--   14 CCR § 1724.7.1(b) requires each casing diagram to be "accompanied by
--   documentation" of (1) all steps of cement yield and cement calculations,
--   (2) all information used to calculate the cement slurry (volume, density,
--   yield), including cement type and additives, for each cement job, and
--   (3) the wellbore path, with measured depth, inclination, and azimuth.
--   § 1724.7.1(c) requires all information for the original hole and any
--   redrilled or sidetracked wellbore. Through checklist v3 this content was
--   stored (10 (b) records, requirement_id 52-61) but not scored. From v4 it
--   is scored.
--
-- What this migration does
--   1. Reuses the 10 existing (b) records (ids 52-61) as checklist points
--      79-88. Codes are unchanged; names and texts are aligned with the v4
--      checklist labels and presence rules.
--   2. Adds one (c) record, id 89, (c).borehole_designation = checklist
--      point 89. It is conditional (the regulation applies when multiple
--      boreholes are drilled) but, like other conditional points, is scored
--      under the presence rule: MET when each borehole is designated or the
--      diagram states that no redrill or sidetrack exists.
--      SUPERSEDED for point 89 by migrate_v4b_point89_conditional.sql:
--      a single-borehole diagram is NOT_APPLICABLE, not MISSING.
--   3. Changes casing_final_score from 78 subdivision-(a) items to 89 items
--      in subdivisions (a), (b), and (c).
--
-- Checklist-to-id map (v4)
--   points  1-78 -> ids as in migrate_add_other_equipment.sql (1-51, 88, 62-87)
--   points 79-88 -> ids 52-61 (unchanged ids)
--   point     89 -> id 89 (new)
--
-- Presence rule and limitation for (b)
--   Only the published diagram file is observed. A (b) point is MET if the
--   information appears on the scored diagram file (including "none", "N/A",
--   or another explicit entry) and MISSING otherwise. A MISSING (b) point
--   means "not on the published diagram", not that the operator failed to
--   file the documentation.
--
-- No TVD records are added: § 1724.7.1(d) requires TVD only for depths
-- required under subdivision (a). Point 86 ((b)(3).wellbore_path_md) is the
-- only MD point without a TVD pair.
--
-- W diagrams (out of study)
--   No result rows are added or changed. The existing W01 rows are left as
--   they are; the view change only alters W01's derived score.

PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

UPDATE spec_requirements SET requirement_name = 'Cement-yield calculation steps',
    requirement_text = 'Steps of the cement-yield calculation for each cement job (inputs and computation). A yield value alone is (b)(2).slurry_yield.'
    WHERE requirement_id = 52 AND requirement_code = '(b)(1).yield_calculation_steps';
UPDATE spec_requirements SET requirement_name = 'Cement calculation steps',
    requirement_text = 'Steps of any other cement calculation performed for each cement job (e.g., annular volume, excess, sacks required). A result alone is not the steps.'
    WHERE requirement_id = 53 AND requirement_code = '(b)(1).cement_calculation_steps';
UPDATE spec_requirements SET requirement_name = 'Slurry volume (or sacks) for each cement job',
    requirement_text = 'Slurry volume, or the quantity used to calculate it (e.g., sacks, cubic feet, barrels), for each cement job.'
    WHERE requirement_id = 54 AND requirement_code = '(b)(2).slurry_volume';
UPDATE spec_requirements SET requirement_name = 'Slurry density for each cement job',
    requirement_text = 'Slurry density or weight (e.g., ppg) for each cement job.'
    WHERE requirement_id = 55 AND requirement_code = '(b)(2).slurry_density';
UPDATE spec_requirements SET requirement_name = 'Slurry yield for each cement job',
    requirement_text = 'Slurry yield (e.g., cu ft/sk) for each cement job.'
    WHERE requirement_id = 56 AND requirement_code = '(b)(2).slurry_yield';
UPDATE spec_requirements SET requirement_name = 'Cement type for each cement job',
    requirement_text = 'Cement type or class (e.g., Class G) for each cement job.'
    WHERE requirement_id = 57 AND requirement_code = '(b)(2).cement_type';
UPDATE spec_requirements SET requirement_name = 'Cement additives for each cement job',
    requirement_text = 'Additives for each cement job, or an explicit statement of none (e.g., neat).'
    WHERE requirement_id = 58 AND requirement_code = '(b)(2).cement_additives';
UPDATE spec_requirements SET requirement_name = 'Wellbore path: measured depth (MD)',
    requirement_text = 'Measured depths of the wellbore-path (survey) stations for each borehole. An explicit vertical/straight-hole statement or N/A is an answer. No TVD pair: subdivision (d) covers only subdivision-(a) depths.'
    WHERE requirement_id = 59 AND requirement_code = '(b)(3).wellbore_path_md';
UPDATE spec_requirements SET requirement_name = 'Wellbore path: inclination',
    requirement_text = 'Inclination along the wellbore path for each borehole. An explicit vertical/straight-hole statement or N/A is an answer; a deviation statement or range (e.g., "Deviated (15 to 30 deg)") also answers this point.'
    WHERE requirement_id = 60 AND requirement_code = '(b)(3).inclination';
UPDATE spec_requirements SET requirement_name = 'Wellbore path: azimuth',
    requirement_text = 'Azimuth along the wellbore path for each borehole. An explicit vertical/straight-hole statement or N/A is an answer; a deviation range without azimuth is not.'
    WHERE requirement_id = 61 AND requirement_code = '(b)(3).azimuth';

INSERT INTO spec_requirements (
    requirement_id, section_id, requirement_code, requirement_name,
    requirement_text, scope_type, is_conditional
) VALUES (
    89, 3, '(c).borehole_designation',
    'Borehole designation (original hole, redrill, or sidetrack)',
    'Each borehole shown is designated as the original hole or a redrill or sidetrack (e.g., Original hole, OH, RD1, ST01, wellbore number 00/01), or the diagram states that no redrill or sidetrack exists. An undesignated single bore is MISSING.',
    'WELLBORE', 1
);

UPDATE spec_sections
SET section_text = 'Each casing diagram shall be accompanied by the listed documentation. Scored from checklist v4 (points 79-88) only as it appears on the published diagram file.'
WHERE section_id = 2 AND section_code = '(b)';

DROP VIEW IF EXISTS casing_final_score;
CREATE VIEW casing_final_score AS
SELECT
    d.diagram_number,
    89 AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    ROUND(100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END) / 89.0, 1) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code IN ('(a)', '(b)', '(c)')
GROUP BY d.diagram_number;

COMMIT;
