-- migrate_v42_reference_records.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v4.2.txt (Version 4.2)
-- Run after migrate_v42_ai_cannot_determine.sql.
-- Backup taken before running: scratchpad casing_specs.pre-uload.db
--
-- Purpose
--   Store the human-reference scoring of the study diagrams (U01-U30) loaded
--   from 06-study/sample-uic/reference/Uxx.json by
--   scripts/load_reference_json.py.
--
-- What this migration adds (no rows are inserted or changed)
--   diagrams                     metadata columns: sample, api_number,
--                                well_name, operator_name, field_name, county,
--                                uic_project, well_type, wellstar_doc_id.
--                                (diagram_date already exists.)
--   diagram_requirement_results  checklist_point (v4.2 display number; DB
--                                ids differ, see migrate_v41), location_page,
--                                location_bbox (JSON text [x0,y0,x1,y1]).
--                                evidence/explanation already exist.
--   reference_reviews            one row per diagram: checklist version,
--                                reviewer, review date, counts and the
--                                completeness percentage stated by the review.
--   non_scored_items             items recorded but not scored: EXCESS data,
--                                PROVENANCE, SUPPORTING (supports another
--                                requirement; optional requirement_id).
--   reference_score_check        view: reference_reviews vs casing_final_score.
--
-- W diagrams (out of study): no W row is added or changed. New diagrams
-- columns stay NULL for W01.

PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

ALTER TABLE diagrams ADD COLUMN sample TEXT CHECK (sample IN ('W', 'UIC'));
ALTER TABLE diagrams ADD COLUMN api_number TEXT;
ALTER TABLE diagrams ADD COLUMN well_name TEXT;
ALTER TABLE diagrams ADD COLUMN operator_name TEXT;
ALTER TABLE diagrams ADD COLUMN field_name TEXT;
ALTER TABLE diagrams ADD COLUMN county TEXT;
ALTER TABLE diagrams ADD COLUMN uic_project TEXT;
ALTER TABLE diagrams ADD COLUMN well_type TEXT;
ALTER TABLE diagrams ADD COLUMN wellstar_doc_id TEXT;

ALTER TABLE diagram_requirement_results ADD COLUMN checklist_point INTEGER
    CHECK (checklist_point BETWEEN 1 AND 90);
ALTER TABLE diagram_requirement_results ADD COLUMN location_page INTEGER;
ALTER TABLE diagram_requirement_results ADD COLUMN location_bbox TEXT;

CREATE TABLE reference_reviews (
    diagram_number TEXT PRIMARY KEY REFERENCES diagrams(diagram_number),
    checklist_version TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date TEXT NOT NULL,
    met_items INTEGER NOT NULL,
    missing_items INTEGER NOT NULL,
    not_applicable_items INTEGER NOT NULL,
    applicable_items INTEGER NOT NULL,
    completeness_percentage REAL NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (met_items + missing_items = applicable_items),
    CHECK (applicable_items + not_applicable_items = 90)
);

CREATE TABLE non_scored_items (
    non_scored_item_id INTEGER PRIMARY KEY,
    diagram_number TEXT NOT NULL REFERENCES diagrams(diagram_number),
    category TEXT NOT NULL CHECK (category IN ('EXCESS', 'PROVENANCE', 'SUPPORTING')),
    type_code TEXT,
    label TEXT,
    instance_text TEXT,
    requirement_id INTEGER REFERENCES spec_requirements(requirement_id),
    location_page INTEGER,
    location_bbox TEXT,
    citation TEXT,
    notes TEXT
);

CREATE INDEX idx_non_scored_items_diagram ON non_scored_items(diagram_number, category);

CREATE VIEW reference_score_check AS
SELECT
    rr.diagram_number,
    rr.met_items AS review_met,
    f.complete_items AS db_met,
    rr.applicable_items AS review_applicable,
    f.scoring_items AS db_applicable,
    rr.completeness_percentage AS review_percentage,
    f.completeness_percentage AS db_percentage,
    CASE
        WHEN rr.met_items = f.complete_items
         AND rr.applicable_items = f.scoring_items
         AND ROUND(rr.completeness_percentage, 1) = f.completeness_percentage
        THEN 'MATCH' ELSE 'MISMATCH'
    END AS check_result
FROM reference_reviews AS rr
LEFT JOIN casing_final_score AS f USING (diagram_number);

COMMIT;
