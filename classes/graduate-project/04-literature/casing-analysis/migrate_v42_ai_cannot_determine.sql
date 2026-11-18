-- migrate_v42_ai_cannot_determine.sql
-- Date: 2026-11-18
-- Checklist version: casing-diagram-atomic-checklist-v4.2.txt (Version 4.2)
-- Run after migrate_v41_cement_job_identification.sql.
-- Backup taken before running: scratchpad casing_specs.pre-v4.2.db
--
-- Student decision (2026-11-18), after review of the prompts by a
-- wellbore-diagram subject-matter expert (C. Castro, personal communication,
-- November 18, 2026): the AI may return a third verdict, CANNOT_DETERMINE,
-- so that it does not guess.
--
-- Schema finding
--   Before v4.2 the database held only the human-reference results
--   (diagram_requirement_results). No table stored AI responses. The human
--   reference is NOT changed: it stays MET / MISSING (plus NOT_APPLICABLE for
--   requirement_id 89 = checklist point 90). The reviewer never uses
--   CANNOT_DETERMINE.
--
-- What this migration adds (no rows are inserted)
--   ai_runs              one row per run (diagram, service, prompt type,
--                        prompt version, order, date, model version, file).
--   ai_point_judgments   one row per point the AI returned. Status allows
--                        MET, MISSING, CANNOT_DETERMINE (any point), and
--                        NOT_APPLICABLE (requirement_id 89 only). A point the
--                        AI did not return has no row ("not addressed").
--   ai_point_scoring     view: every applicable reference point for every
--                        run, categorized CORRECT, WRONG, CANNOT_DETERMINE,
--                        or NOT_ADDRESSED. Points whose reference is
--                        NOT_APPLICABLE are excluded (denominator 90 or 89).
--   ai_run_accuracy      view: per run, the counts per category and accuracy
--                        = CORRECT / applicable points. CANNOT_DETERMINE is in
--                        the denominator but not the numerator.
--   ai_cannot_determine_rate  view: CANNOT_DETERMINE rate per service and
--                        prompt type (secondary outcome).

PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

CREATE TABLE ai_runs (
    run_id TEXT PRIMARY KEY,
    diagram_number TEXT NOT NULL REFERENCES diagrams(diagram_number),
    ai_service TEXT NOT NULL CHECK (ai_service IN ('ChatGPT', 'Claude', 'Gemini')),
    prompt_type TEXT NOT NULL CHECK (prompt_type IN ('NAIVE', 'INFORMED', 'CHAIN_OF_THOUGHT')),
    prompt_version TEXT NOT NULL,
    prompt_order INTEGER CHECK (prompt_order IN (1, 2, 3)),
    run_date TEXT NOT NULL,
    displayed_model_version TEXT,
    response_file TEXT NOT NULL,
    rows_returned INTEGER,
    response_word_count INTEGER,
    UNIQUE (diagram_number, ai_service, prompt_type)
);

CREATE TABLE ai_point_judgments (
    judgment_id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES ai_runs(run_id),
    requirement_id INTEGER NOT NULL REFERENCES spec_requirements(requirement_id),
    ai_status TEXT NOT NULL CHECK (
        ai_status IN ('MET', 'MISSING', 'CANNOT_DETERMINE')
        OR (ai_status = 'NOT_APPLICABLE' AND requirement_id = 89)
    ),
    displayed_answer TEXT,
    UNIQUE (run_id, requirement_id)
);

CREATE INDEX idx_ai_judgments_run ON ai_point_judgments(run_id);

CREATE VIEW ai_point_scoring AS
SELECT
    run.run_id,
    run.diagram_number,
    run.ai_service,
    run.prompt_type,
    ref.requirement_id,
    ref.status AS reference_status,
    j.ai_status,
    CASE
        WHEN j.ai_status IS NULL THEN 'NOT_ADDRESSED'
        WHEN j.ai_status = 'CANNOT_DETERMINE' THEN 'CANNOT_DETERMINE'
        WHEN j.ai_status = ref.status THEN 'CORRECT'
        ELSE 'WRONG'
    END AS judgment_category
FROM ai_runs AS run
JOIN diagram_requirement_results AS ref
    ON ref.diagram_number = run.diagram_number
JOIN spec_requirements AS q ON q.requirement_id = ref.requirement_id
JOIN spec_sections AS s ON s.section_id = q.section_id
LEFT JOIN ai_point_judgments AS j
    ON j.run_id = run.run_id AND j.requirement_id = ref.requirement_id
WHERE s.section_code IN ('(a)', '(b)', '(c)')
  AND ref.status <> 'NOT_APPLICABLE';

CREATE VIEW ai_run_accuracy AS
SELECT
    run_id,
    diagram_number,
    ai_service,
    prompt_type,
    COUNT(*) AS applicable_points,
    SUM(judgment_category = 'CORRECT') AS correct,
    SUM(judgment_category = 'WRONG') AS wrong,
    SUM(judgment_category = 'CANNOT_DETERMINE') AS cannot_determine,
    SUM(judgment_category = 'NOT_ADDRESSED') AS not_addressed,
    ROUND(1.0 * SUM(judgment_category = 'CORRECT') / COUNT(*), 4) AS accuracy
FROM ai_point_scoring
GROUP BY run_id, diagram_number, ai_service, prompt_type;

CREATE VIEW ai_cannot_determine_rate AS
SELECT
    ai_service,
    prompt_type,
    COUNT(DISTINCT run_id) AS runs,
    COUNT(*) AS applicable_points,
    SUM(judgment_category = 'CANNOT_DETERMINE') AS cannot_determine,
    ROUND(1.0 * SUM(judgment_category = 'CANNOT_DETERMINE') / COUNT(*), 4) AS cannot_determine_rate
FROM ai_point_scoring
GROUP BY ai_service, prompt_type;

COMMIT;
