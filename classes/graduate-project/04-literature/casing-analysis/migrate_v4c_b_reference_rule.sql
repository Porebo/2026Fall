-- migrate_v4c_b_reference_rule.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v4.txt (Version 4.0)
-- Run after migrate_v4b_point89_conditional.sql.
-- Backup taken before running: scratchpad casing_specs.pre-v4c.db
--
-- Student decision (2026-11-18) for points 79-88 (subdivision (b),
-- requirement_id 52-61): if the diagram states or shows that the
-- information accompanies it separately (e.g., "cement calculations
-- attached", "see directional survey", "slurry details in cement report"),
-- the point is MET; if nothing is said or shown, it is MISSING.
-- Only requirement texts change. No result rows are added or changed.

PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

UPDATE spec_requirements
SET requirement_text = requirement_text
    || ' Also MET when the diagram states or shows that this information accompanies it separately (e.g., "cement calculations attached", "see directional survey", "slurry details in cement report"); MISSING when the diagram neither shows nor references it.'
WHERE requirement_id BETWEEN 52 AND 61
  AND requirement_code LIKE '(b)%'
  AND requirement_text NOT LIKE '%accompanies it separately%';

UPDATE spec_sections
SET section_text = 'Each casing diagram shall be accompanied by the listed documentation. Scored from checklist v4 (points 79-88): MET when the published diagram shows the information or states that it accompanies the diagram separately; MISSING when it neither shows nor references it.'
WHERE section_id = 2 AND section_code = '(b)';

COMMIT;
