PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

ALTER TABLE wells ADD COLUMN base_freshwater_tvd_ft REAL;
ALTER TABLE wells ADD COLUMN base_usdw_tvd_ft REAL;
ALTER TABLE drilled_intervals ADD COLUMN top_tvd_ft REAL;
ALTER TABLE drilled_intervals ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE casing_intervals ADD COLUMN top_tvd_ft REAL;
ALTER TABLE casing_intervals ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE cement_jobs ADD COLUMN top_tvd_ft REAL;
ALTER TABLE cement_jobs ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE cement_placements ADD COLUMN top_tvd_ft REAL;
ALTER TABLE cement_placements ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE perforation_intervals ADD COLUMN top_tvd_ft REAL;
ALTER TABLE perforation_intervals ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE geological_features ADD COLUMN top_tvd_ft REAL;
ALTER TABLE geological_features ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE downhole_components ADD COLUMN top_tvd_ft REAL;
ALTER TABLE downhole_components ADD COLUMN bottom_tvd_ft REAL;
ALTER TABLE well_features ADD COLUMN top_tvd_ft REAL;
ALTER TABLE well_features ADD COLUMN bottom_tvd_ft REAL;

UPDATE spec_requirements
SET requirement_code = requirement_code || '.md',
    requirement_name = requirement_name || ' (MD)'
WHERE requirement_id IN (
    8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    25, 27, 33, 35, 36, 38, 39, 43, 45, 47, 48, 49, 50, 51
);

INSERT INTO spec_requirements (
    requirement_id, section_id, requirement_code, requirement_name,
    requirement_text, scope_type, is_conditional
) VALUES
    (62, 1, '(a)(5).freshwater_base.tvd', 'Base of freshwater (TVD)', 'True vertical depth of the base of freshwater.', 'WELL', 0),
    (63, 1, '(a)(6).usdw_base.tvd', 'Base of lowermost USDW (TVD)', 'True vertical depth of the lowermost USDW base.', 'WELL', 0),
    (64, 1, '(a)(8).shoe_depth.tvd', 'Shoe depth (TVD)', 'True vertical depth of each casing shoe.', 'INTERVAL', 0),
    (65, 1, '(a)(8).stub_depth.tvd', 'Stub depth (TVD)', 'True vertical depth of each casing stub.', 'INTERVAL', 1),
    (66, 1, '(a)(8).liner_top_depth.tvd', 'Liner-top depth (TVD)', 'True vertical depth of each liner top.', 'INTERVAL', 1),
    (67, 1, '(a)(9).perforation_depths.tvd', 'Perforation depths (TVD)', 'True vertical depths of perforations.', 'INTERVAL', 1),
    (68, 1, '(a)(9).perforation_intervals.tvd', 'Perforation intervals (TVD)', 'True vertical depths for perforation interval boundaries.', 'INTERVAL', 1),
    (69, 1, '(a)(9).open_hole_completions.tvd', 'Open-hole completions (TVD)', 'True vertical depths of open-hole completions.', 'INTERVAL', 1),
    (70, 1, '(a)(9).water_shutoff_holes.tvd', 'Water-shutoff holes (TVD)', 'True vertical depths of water-shutoff holes.', 'INTERVAL', 1),
    (71, 1, '(a)(9).cement_ports.tvd', 'Cement ports (TVD)', 'True vertical depths of cement ports.', 'INTERVAL', 1),
    (72, 1, '(a)(9).cavity_shots.tvd', 'Cavity shots (TVD)', 'True vertical depths of cavity shots.', 'INTERVAL', 1),
    (73, 1, '(a)(9).cuts.tvd', 'Cuts (TVD)', 'True vertical depths of casing cuts.', 'INTERVAL', 1),
    (74, 1, '(a)(9).casing_damage_extent.tvd', 'Casing-damage extent (TVD)', 'True vertical depth extent of casing damage.', 'INTERVAL', 1),
    (75, 1, '(a)(9).junk_or_fish_extent.tvd', 'Junk/fish extent (TVD)', 'True vertical depth extent of junk or fish.', 'INTERVAL', 1),
    (76, 1, '(a)(11).hole_depth.tvd', 'Hole depth (TVD)', 'True vertical depth for every drilled interval.', 'INTERVAL', 0),
    (77, 1, '(a)(12).cement_plug_top.tvd', 'Cement-plug top (TVD)', 'True vertical depth of each cement-plug top.', 'INTERVAL', 1),
    (78, 1, '(a)(12).cement_plug_bottom.tvd', 'Cement-plug bottom (TVD)', 'True vertical depth of each cement-plug bottom.', 'INTERVAL', 1),
    (79, 1, '(a)(13).cement_fill_top.tvd', 'Cement-fill top (TVD)', 'True vertical depth of cement-fill tops.', 'INTERVAL', 0),
    (80, 1, '(a)(13).cement_fill_bottom.tvd', 'Cement-fill bottom (TVD)', 'True vertical depth of cement-fill bottoms.', 'INTERVAL', 0),
    (81, 1, '(a)(15).formation_depths.tvd', 'Formation depths (TVD)', 'True vertical depths of formations.', 'INTERVAL', 0),
    (82, 1, '(a)(15).zone_depths.tvd', 'Zone depths (TVD)', 'True vertical depths of zones.', 'INTERVAL', 1),
    (83, 1, '(a)(15).marker_depths.tvd', 'Marker depths (TVD)', 'True vertical depths of markers.', 'INTERVAL', 0),
    (84, 1, '(a)(15).injection_zone_top.tvd', 'Injection-zone top (TVD)', 'True vertical depth of the injection-zone top.', 'INTERVAL', 1),
    (85, 1, '(a)(15).injection_zone_bottom.tvd', 'Injection-zone bottom (TVD)', 'True vertical depth of the injection-zone bottom.', 'INTERVAL', 1),
    (86, 1, '(a)(15).confining_layer_top.tvd', 'Confining-layer top (TVD)', 'True vertical depth of each confining-layer top.', 'INTERVAL', 1),
    (87, 1, '(a)(15).confining_layer_bottom.tvd', 'Confining-layer bottom (TVD)', 'True vertical depth of each confining-layer bottom.', 'INTERVAL', 1);

INSERT INTO diagram_requirement_results (
    diagram_number, requirement_id, status, evidence, explanation
)
SELECT
    'W01',
    requirement_id,
    'MISSING',
    NULL,
    'No TVD answer is visibly supplied on W01.'
FROM spec_requirements
WHERE requirement_id BETWEEN 62 AND 87;

DROP VIEW IF EXISTS casing_final_score;
CREATE VIEW casing_final_score AS
SELECT
    d.diagram_number,
    77 AS scoring_items,
    COUNT(CASE WHEN r.status = 'MET' THEN 1 END) AS complete_items,
    COUNT(CASE WHEN r.status = 'MISSING' THEN 1 END) AS missing_items,
    ROUND(100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END) / 77.0, 1) AS completeness_percentage
FROM diagrams AS d
JOIN diagram_requirement_results AS r USING (diagram_number)
JOIN spec_requirements AS q USING (requirement_id)
JOIN spec_sections AS s USING (section_id)
WHERE s.section_code = '(a)'
GROUP BY d.diagram_number;

COMMIT;
