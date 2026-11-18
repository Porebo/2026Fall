PRAGMA foreign_keys = ON;

CREATE TABLE spec_regulations (
    regulation_id INTEGER PRIMARY KEY,
    citation TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    source_url TEXT,
    effective_note TEXT
);

CREATE TABLE spec_sections (
    section_id INTEGER PRIMARY KEY,
    regulation_id INTEGER NOT NULL REFERENCES spec_regulations(regulation_id),
    section_code TEXT NOT NULL,
    title TEXT NOT NULL,
    section_text TEXT NOT NULL,
    UNIQUE (regulation_id, section_code)
);

CREATE TABLE spec_requirements (
    requirement_id INTEGER PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES spec_sections(section_id),
    requirement_code TEXT NOT NULL UNIQUE,
    requirement_name TEXT NOT NULL,
    requirement_text TEXT NOT NULL,
    scope_type TEXT NOT NULL CHECK (scope_type IN ('DIAGRAM', 'WELL', 'WELLBORE', 'INTERVAL', 'CEMENT_JOB')),
    is_conditional INTEGER NOT NULL DEFAULT 0 CHECK (is_conditional IN (0, 1))
);

CREATE TABLE spec_validation_rules (
    rule_id INTEGER PRIMARY KEY,
    regulation_id INTEGER NOT NULL REFERENCES spec_regulations(regulation_id),
    rule_code TEXT NOT NULL UNIQUE,
    rule_name TEXT NOT NULL,
    rule_text TEXT NOT NULL
);

CREATE TABLE diagrams (
    diagram_number TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    document_title TEXT,
    diagram_date TEXT,
    initials TEXT,
    submission_format TEXT NOT NULL DEFAULT 'PDF'
);

CREATE TABLE operators (
    operator_id INTEGER PRIMARY KEY,
    operator_name TEXT NOT NULL UNIQUE
);

CREATE TABLE wells (
    well_id INTEGER PRIMARY KEY,
    diagram_number TEXT NOT NULL UNIQUE REFERENCES diagrams(diagram_number),
    operator_id INTEGER REFERENCES operators(operator_id),
    lease_name TEXT,
    well_number TEXT NOT NULL,
    api_number TEXT NOT NULL,
    spud_date TEXT,
    well_type TEXT,
    ground_elevation_ft REAL,
    reference_elevation_ft REAL,
    reference_elevation_type TEXT,
    base_freshwater_md_ft REAL,
    base_usdw_md_ft REAL
);

CREATE TABLE wellbores (
    wellbore_id INTEGER PRIMARY KEY,
    diagram_number TEXT NOT NULL REFERENCES diagrams(diagram_number),
    well_id INTEGER NOT NULL REFERENCES wells(well_id),
    wellbore_number TEXT NOT NULL,
    is_original INTEGER NOT NULL DEFAULT 1 CHECK (is_original IN (0, 1)),
    orientation TEXT,
    plugged_back_md_ft REAL,
    total_md_ft REAL,
    UNIQUE (well_id, wellbore_number)
);

CREATE TABLE drilled_intervals (
    drilled_interval_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    hole_diameter_in REAL NOT NULL,
    top_md_ft REAL NOT NULL,
    bottom_md_ft REAL NOT NULL
);

CREATE TABLE casing_intervals (
    casing_interval_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    casing_diameter_in REAL NOT NULL,
    weight_ppf REAL,
    grade_or_schedule TEXT,
    connection_type TEXT,
    top_md_ft REAL NOT NULL,
    bottom_md_ft REAL NOT NULL,
    terminal_feature TEXT CHECK (terminal_feature IN ('SHOE', 'STUB', 'LINER_TOP', 'OTHER')),
    notes TEXT
);

CREATE TABLE cement_jobs (
    cement_job_id INTEGER PRIMARY KEY,
    casing_interval_id INTEGER REFERENCES casing_intervals(casing_interval_id),
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    job_type TEXT NOT NULL,
    job_date TEXT,
    top_md_ft REAL,
    bottom_md_ft REAL,
    sacks REAL,
    density_ppg REAL,
    yield_cf_per_sack REAL,
    cement_volume_cf REAL,
    returns_bbl REAL,
    calculation_steps TEXT,
    remarks TEXT
);

CREATE TABLE cement_components (
    cement_component_id INTEGER PRIMARY KEY,
    cement_job_id INTEGER NOT NULL REFERENCES cement_jobs(cement_job_id),
    component_name TEXT NOT NULL,
    quantity REAL,
    unit TEXT
);

CREATE TABLE cement_placements (
    cement_placement_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    placement_type TEXT NOT NULL CHECK (placement_type IN ('BEHIND_CASING', 'INSIDE_CASING')),
    casing_interval_id INTEGER REFERENCES casing_intervals(casing_interval_id),
    cement_job_id INTEGER REFERENCES cement_jobs(cement_job_id),
    top_md_ft REAL,
    bottom_md_ft REAL,
    determination_method TEXT
);

CREATE TABLE perforation_intervals (
    perforation_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    top_md_ft REAL NOT NULL,
    bottom_md_ft REAL NOT NULL,
    shots_per_ft REAL
);

CREATE TABLE geological_features (
    geological_feature_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    feature_class TEXT NOT NULL CHECK (feature_class IN ('FORMATION', 'ZONE', 'MARKER', 'INJECTION_ZONE', 'CONFINING_LAYER')),
    feature_name TEXT NOT NULL,
    top_md_ft REAL,
    bottom_md_ft REAL
);

CREATE TABLE downhole_assemblies (
    assembly_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    assembly_name TEXT NOT NULL
);

CREATE TABLE downhole_components (
    component_id INTEGER PRIMARY KEY,
    assembly_id INTEGER NOT NULL REFERENCES downhole_assemblies(assembly_id),
    component_type TEXT NOT NULL,
    top_md_ft REAL,
    bottom_md_ft REAL,
    notes TEXT
);

CREATE TABLE well_features (
    well_feature_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    feature_type TEXT NOT NULL CHECK (
        feature_type IN (
            'OPEN_HOLE_COMPLETION', 'WATER_SHUTOFF_HOLE', 'CEMENT_PORT',
            'CAVITY_SHOT', 'CUT', 'CASING_DAMAGE', 'JUNK_OR_FISH',
            'OTHER_FLOW_OR_INTEGRITY_FEATURE', 'SUBSURFACE_SAFETY_VALVE',
            'PACKER', 'GAS_LIFT_MANDREL', 'OBSTRUCTION'
        )
    ),
    top_md_ft REAL,
    bottom_md_ft REAL,
    description TEXT
);

CREATE TABLE borehole_surveys (
    survey_id INTEGER PRIMARY KEY,
    wellbore_id INTEGER NOT NULL REFERENCES wellbores(wellbore_id),
    md_ft REAL NOT NULL,
    tvd_ft REAL,
    inclination_deg REAL,
    azimuth_deg REAL
);

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

CREATE TABLE completeness_infractions (
    infraction_id INTEGER PRIMARY KEY,
    result_id INTEGER NOT NULL UNIQUE REFERENCES diagram_requirement_results(result_id),
    severity TEXT NOT NULL DEFAULT 'COMPLETENESS',
    resolution_status TEXT NOT NULL DEFAULT 'OPEN',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

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
        100.0 * COUNT(CASE WHEN r.status = 'MET' THEN 1 END)
        / 51.0,
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

INSERT INTO spec_regulations (
    regulation_id, citation, title, source_url, effective_note
) VALUES (
    1,
    'Cal. Code Regs. tit. 14, § 1724.7.1',
    'Casing Diagrams',
    'https://www.law.cornell.edu/regulations/california/14-CCR-1724.7.1',
    'Current regulation supplied for this database'
);

INSERT INTO spec_sections (section_id, regulation_id, section_code, title, section_text) VALUES
    (1, 1, '(a)', 'Casing diagram data', 'Casing diagrams submitted under this article shall include all listed data.'),
    (2, 1, '(b)', 'Supporting documentation', 'Each casing diagram shall be accompanied by the listed documentation.'),
    (3, 1, '(c)', 'Multiple boreholes', 'All information is required for original, redrilled, and sidetracked wellbores.'),
    (4, 1, '(d)', 'Depth conventions', 'Measured depth and true vertical depth are required for all depths under subdivision (a).'),
    (5, 1, '(e)', 'Submission format', 'A graphical diagram or flat-file data set may be submitted if complete.');

INSERT INTO spec_requirements (
    requirement_id, section_id, requirement_code, requirement_name,
    requirement_text, scope_type, is_conditional
) VALUES
    (1, 1, '(a)(1).operator_name', 'Operator name', 'Name of the well operator.', 'WELL', 0),
    (2, 1, '(a)(1).lease_name', 'Lease name', 'Name of the lease associated with the well.', 'WELL', 0),
    (3, 1, '(a)(1).well_number', 'Well number', 'Assigned number of the well.', 'WELL', 0),
    (4, 1, '(a)(1).api_number', 'API number', 'API number of the well.', 'WELL', 0),
    (5, 1, '(a)(2).spud_date', 'Spud date', 'Date the well was spudded.', 'WELL', 0),
    (6, 1, '(a)(3).ground_elevation', 'Ground elevation', 'Ground elevation from sea level.', 'WELL', 0),
    (7, 1, '(a)(4).reference_elevation', 'Reference elevation', 'Rig-floor or Kelly-bushing reference elevation.', 'WELL', 0),
    (8, 1, '(a)(5).freshwater_base', 'Base of freshwater', 'Depth of the base of freshwater.', 'WELL', 0),
    (9, 1, '(a)(6).usdw_base', 'Base of lowermost USDW', 'Depth of the base of the lowermost USDW penetrated.', 'WELL', 0),
    (10, 1, '(a)(7).casing_size', 'Casing size', 'Size of each casing.', 'INTERVAL', 0),
    (11, 1, '(a)(7).casing_grade', 'Casing grade', 'Grade of each casing.', 'INTERVAL', 0),
    (12, 1, '(a)(7).connection_type', 'Casing connection type', 'Connection type of each casing.', 'INTERVAL', 0),
    (13, 1, '(a)(7).casing_weight', 'Casing weight', 'Weight of each casing.', 'INTERVAL', 0),
    (14, 1, '(a)(8).shoe_depth', 'Shoe depth', 'Depth of each casing shoe.', 'INTERVAL', 0),
    (15, 1, '(a)(8).stub_depth', 'Stub depth', 'Depth of each casing stub.', 'INTERVAL', 1),
    (16, 1, '(a)(8).liner_top_depth', 'Liner-top depth', 'Depth of each liner top.', 'INTERVAL', 1),
    (17, 1, '(a)(9).perforation_depths', 'Perforation depths', 'Depths of perforations.', 'INTERVAL', 1),
    (18, 1, '(a)(9).perforation_intervals', 'Perforation intervals', 'Top and bottom of perforation intervals.', 'INTERVAL', 1),
    (19, 1, '(a)(9).open_hole_completions', 'Open-hole completions', 'Open-hole completion details and depths.', 'INTERVAL', 1),
    (20, 1, '(a)(9).water_shutoff_holes', 'Water-shutoff holes', 'Depths of water-shutoff holes.', 'INTERVAL', 1),
    (21, 1, '(a)(9).cement_ports', 'Cement ports', 'Depths of cement ports.', 'INTERVAL', 1),
    (22, 1, '(a)(9).cavity_shots', 'Cavity shots', 'Depths of cavity shots.', 'INTERVAL', 1),
    (23, 1, '(a)(9).cuts', 'Cuts', 'Depths and extent of casing cuts.', 'INTERVAL', 1),
    (24, 1, '(a)(9).casing_damage_type', 'Casing-damage type', 'Type of casing damage.', 'INTERVAL', 1),
    (25, 1, '(a)(9).casing_damage_extent', 'Casing-damage extent', 'Extent of casing damage.', 'INTERVAL', 1),
    (26, 1, '(a)(9).junk_or_fish_type', 'Junk/fish type', 'Type of junk or fish.', 'INTERVAL', 1),
    (27, 1, '(a)(9).junk_or_fish_extent', 'Junk/fish extent', 'Extent of junk or fish.', 'INTERVAL', 1),
    (28, 1, '(a)(9).other_integrity_feature', 'Other flow/integrity feature', 'Any other feature affecting flow or mechanical integrity.', 'INTERVAL', 1),
    (29, 1, '(a)(10).subsurface_safety_valves', 'Subsurface safety valves', 'Information about subsurface safety valves.', 'WELLBORE', 1),
    (30, 1, '(a)(10).packers', 'Packers', 'Information about packers.', 'WELLBORE', 1),
    (31, 1, '(a)(10).gas_lift_mandrels', 'Gas-lift mandrels', 'Information about gas-lift mandrels.', 'WELLBORE', 1),
    (32, 1, '(a)(11).hole_diameter', 'Hole diameter', 'Diameter for every drilled interval.', 'INTERVAL', 0),
    (33, 1, '(a)(11).hole_depth', 'Hole depth', 'Depth for every drilled interval.', 'INTERVAL', 0),
    (34, 1, '(a)(12).cement_plug_identification', 'Cement-plug identification', 'Identification of cement plugs inside casing.', 'INTERVAL', 1),
    (35, 1, '(a)(12).cement_plug_top', 'Cement-plug top', 'Location of the top of each cement plug.', 'INTERVAL', 1),
    (36, 1, '(a)(12).cement_plug_bottom', 'Cement-plug bottom', 'Location of the bottom of each cement plug.', 'INTERVAL', 1),
    (37, 1, '(a)(13).cement_fill_identification', 'Cement-fill identification', 'Identification of cement fill behind casing.', 'INTERVAL', 0),
    (38, 1, '(a)(13).cement_fill_top', 'Cement-fill top', 'Location of the top of cement fill behind casing.', 'INTERVAL', 0),
    (39, 1, '(a)(13).cement_fill_bottom', 'Cement-fill bottom', 'Location of the bottom of cement fill behind casing.', 'INTERVAL', 0),
    (40, 1, '(a)(14).fluid_type', 'Fluid type between plugs', 'Type of fluid between cement plugs.', 'INTERVAL', 1),
    (41, 1, '(a)(14).fluid_density', 'Fluid density between plugs', 'Density of fluid between cement plugs.', 'INTERVAL', 1),
    (42, 1, '(a)(15).formation_names', 'Formation names', 'Names of formations penetrated by the well.', 'INTERVAL', 0),
    (43, 1, '(a)(15).formation_depths', 'Formation depths', 'Depths of formations penetrated by the well.', 'INTERVAL', 0),
    (44, 1, '(a)(15).zone_names', 'Zone names', 'Names of zones penetrated by the well.', 'INTERVAL', 1),
    (45, 1, '(a)(15).zone_depths', 'Zone depths', 'Depths of zones penetrated by the well.', 'INTERVAL', 1),
    (46, 1, '(a)(15).marker_names', 'Marker names', 'Names of markers penetrated by the well.', 'INTERVAL', 0),
    (47, 1, '(a)(15).marker_depths', 'Marker depths', 'Depths of markers penetrated by the well.', 'INTERVAL', 0),
    (48, 1, '(a)(15).injection_zone_top', 'Injection-zone top', 'Top of the underground-injection zone.', 'INTERVAL', 1),
    (49, 1, '(a)(15).injection_zone_bottom', 'Injection-zone bottom', 'Bottom of the underground-injection zone.', 'INTERVAL', 1),
    (50, 1, '(a)(15).confining_layer_top', 'Confining-layer top', 'Top of each confining layer.', 'INTERVAL', 1),
    (51, 1, '(a)(15).confining_layer_bottom', 'Confining-layer bottom', 'Bottom of each confining layer.', 'INTERVAL', 1),
    (52, 2, '(b)(1).yield_calculation_steps', 'Cement yield calculation steps', 'All steps used in cement-yield calculations.', 'CEMENT_JOB', 0),
    (53, 2, '(b)(1).cement_calculation_steps', 'Cement calculation steps', 'All steps of every cement calculation performed.', 'CEMENT_JOB', 0),
    (54, 2, '(b)(2).slurry_volume', 'Slurry volume inputs', 'All information used to calculate slurry volume.', 'CEMENT_JOB', 0),
    (55, 2, '(b)(2).slurry_density', 'Slurry density', 'All information used to calculate slurry density.', 'CEMENT_JOB', 0),
    (56, 2, '(b)(2).slurry_yield', 'Slurry yield', 'All information used to calculate slurry yield.', 'CEMENT_JOB', 0),
    (57, 2, '(b)(2).cement_type', 'Cement type', 'Cement type for every completed cement job.', 'CEMENT_JOB', 0),
    (58, 2, '(b)(2).cement_additives', 'Cement additives', 'Additives for every completed cement job.', 'CEMENT_JOB', 0),
    (59, 2, '(b)(3).wellbore_path_md', 'Wellbore-path measured depth', 'Measured depths along the wellbore path.', 'WELLBORE', 0),
    (60, 2, '(b)(3).inclination', 'Wellbore inclination', 'Inclination measurements for the wellbore path.', 'WELLBORE', 0),
    (61, 2, '(b)(3).azimuth', 'Wellbore azimuth', 'Azimuth measurements for the wellbore path.', 'WELLBORE', 0);

INSERT INTO spec_validation_rules (rule_id, regulation_id, rule_code, rule_name, rule_text) VALUES
    (1, 1, '(c).all_boreholes', 'All-borehole coverage', 'Apply all requirements separately to original, redrilled, and sidetracked boreholes.'),
    (2, 1, '(d).md_required', 'Measured depth required', 'Provide measured depth for every depth required under subdivision (a).'),
    (3, 1, '(d).tvd_required', 'True vertical depth required', 'Provide true vertical depth for every depth required under subdivision (a).'),
    (4, 1, '(e).complete_format', 'Complete submission format', 'A graphical diagram or flat-file dataset must contain all information described in this section.');

INSERT INTO diagrams (
    diagram_number, source_file, document_title, diagram_date, initials, submission_format
) VALUES (
    'W01',
    'classes\graduate-project\06-study\sample\diagrams\W01.pdf',
    'Wellbore Schematic',
    '2023-11-30',
    'xyz',
    'PDF'
);

INSERT INTO operators (operator_id, operator_name) VALUES (1, 'Aera Energy LLC');

INSERT INTO wells (
    well_id, diagram_number, operator_id, lease_name, well_number, api_number,
    spud_date, well_type, ground_elevation_ft, reference_elevation_ft,
    reference_elevation_type, base_freshwater_md_ft, base_usdw_md_ft
) VALUES (
    1, 'W01', 1, NULL, '948C-28', '0403033530',
    '2007-07-03', 'Producer', 591.26, 603.26,
    'KELLY BUSHING', NULL, NULL
);

INSERT INTO wellbores (
    wellbore_id, diagram_number, well_id, wellbore_number, is_original,
    orientation, plugged_back_md_ft, total_md_ft
) VALUES (
    1, 'W01', 1, '00', 1, 'Directional', 2143.17, 2174.00
);

INSERT INTO drilled_intervals (
    drilled_interval_id, wellbore_id, hole_diameter_in, top_md_ft, bottom_md_ft
) VALUES
    (1, 1, 24.00, 0.00, 52.00),
    (2, 1, 12.25, 52.00, 205.00),
    (3, 1, 8.75, 205.00, 2174.00);

INSERT INTO casing_intervals (
    casing_interval_id, wellbore_id, casing_diameter_in, weight_ppf,
    grade_or_schedule, connection_type, top_md_ft, bottom_md_ft,
    terminal_feature, notes
) VALUES
    (1, 1, 14.0000, 36.71, 'SCH 20', 'PLAIN END', 12.00, 52.00, 'SHOE', NULL),
    (2, 1, 9.6250, 36.00, 'K-55', 'LT&C', 13.00, 202.00, 'SHOE', NULL),
    (3, 1, 7.0000, 23.00, 'K-55', 'LT&C', 12.50, 735.17, 'OTHER', 'Upper portion of depicted production casing'),
    (4, 1, 7.0000, 23.00, 'K-55', 'LT&C', 737.54, 2143.17, 'OTHER', 'Production casing below flag joint'),
    (5, 1, 7.0000, 23.00, 'K-55', 'LT&C', 2143.18, 2163.03, 'OTHER', 'Casing below PBMD');

INSERT INTO cement_jobs (
    cement_job_id, casing_interval_id, wellbore_id, job_type, job_date,
    top_md_ft, bottom_md_ft, sacks, density_ppg, yield_cf_per_sack,
    cement_volume_cf, returns_bbl, calculation_steps, remarks
) VALUES
    (1, 2, 1, 'Primary', '2007-07-03', 13.00, 202.00, 86, 13.5, 1.74,
     149.64, 5, NULL, 'A-4 Versamix Surface Class C cement; returns to surface.'),
    (2, 3, 1, 'Primary', '2007-07-23', 12.00, 2164.00, 168, 12.0, 2.71,
     455.28, 4, NULL, 'B-3 Slim Hole Design Class C cement; returns to surface.');

INSERT INTO cement_components (
    cement_component_id, cement_job_id, component_name, quantity, unit
) VALUES
    (1, 1, 'BWOC FDP-C572', 0.25, '%'),
    (2, 1, 'BWOC VERSASET', 0.60, '%'),
    (3, 1, 'BWOC SILICA FLOUR', 35.00, '%'),
    (4, 1, 'POZMIX A', 37.00, 'lb/sack'),
    (5, 1, 'BWOW SALT', 5.00, '%'),
    (6, 2, 'BWOC SILICA FLOUR', 30.00, '%');

INSERT INTO cement_placements (
    cement_placement_id, wellbore_id, placement_type, casing_interval_id,
    cement_job_id, top_md_ft, bottom_md_ft, determination_method
) VALUES
    (1, 1, 'BEHIND_CASING', 2, 1, 13.00, 202.00, NULL),
    (2, 1, 'BEHIND_CASING', 3, 2, 12.00, 2164.00, NULL);

WITH perforation_depths(n, top_depth) AS (
    VALUES
        (1, 880.00), (2, 932.00), (3, 984.00), (4, 1036.00),
        (5, 1088.00), (6, 1140.00), (7, 1180.00), (8, 1232.00),
        (9, 1284.00), (10, 1336.00), (11, 1388.00), (12, 1440.00),
        (13, 1480.00), (14, 1532.00), (15, 1584.00), (16, 1636.00),
        (17, 1688.00), (18, 1740.00), (19, 1780.00), (20, 1832.00),
        (21, 1884.00), (22, 1936.00), (23, 1988.00), (24, 2040.00)
)
INSERT INTO perforation_intervals (
    perforation_id, wellbore_id, top_md_ft, bottom_md_ft, shots_per_ft
)
SELECT n, 1, top_depth, top_depth + 1.00, 4.00
FROM perforation_depths;

INSERT INTO geological_features (
    geological_feature_id, wellbore_id, feature_class, feature_name, top_md_ft, bottom_md_ft
) VALUES
    (1, 1, 'MARKER', 'Tulare', 70.25, NULL),
    (2, 1, 'MARKER', 'San Joaquin/Etchegoin', 670.03, NULL),
    (3, 1, 'MARKER', 'Reef Ridge Diatomite', 710.00, NULL);

INSERT INTO downhole_assemblies (assembly_id, wellbore_id, assembly_name) VALUES
    (1, 1, 'TUBING'),
    (2, 1, 'ROD STRING');

INSERT INTO downhole_components (
    component_id, assembly_id, component_type, top_md_ft, bottom_md_ft, notes
) VALUES
    (1, 1, 'Tubing Hanger', 12.00, 13.00, NULL),
    (2, 1, 'Tubing Fatigue Nipple', 13.00, 14.00, NULL),
    (3, 1, 'X-Over', 14.00, 15.00, NULL),
    (4, 1, 'Pup Joint', 15.00, 29.00, NULL),
    (5, 1, 'Tubing', 29.00, 532.00, NULL),
    (6, 1, 'Tubing Drain', 532.00, 532.00, NULL),
    (7, 1, 'Tubing', 532.00, 597.00, NULL),
    (8, 1, 'Rod Pump Shoe', 597.00, 597.00, NULL),
    (9, 1, 'Chamfered Collar', 597.00, 598.00, NULL),
    (10, 2, 'Polished Rod', 12.00, 42.00, NULL),
    (11, 2, 'Pony Rod(s)', 42.00, 58.00, NULL),
    (12, 2, 'Sucker Rod(s)', 58.00, 538.00, NULL),
    (13, 2, 'Rod Shear Tool', 538.00, 538.00, NULL),
    (14, 2, 'Sucker Rod(s)', 538.00, 598.00, NULL),
    (15, 2, 'Stabilizer Bar 4'' w/3 guides', 598.00, 602.00, NULL),
    (16, 2, 'Rod Pump', 602.00, 618.00, NULL);

INSERT INTO diagram_requirement_results (
    diagram_number, requirement_id, status, evidence, explanation
)
SELECT
    'W01',
    requirement_id,
    'MISSING',
    NULL,
    'Not demonstrated by the W01 diagram.'
FROM spec_requirements;

UPDATE diagram_requirement_results
SET status = 'MET',
    evidence = CASE requirement_id
        WHEN 1 THEN 'Aera Energy LLC'
        WHEN 3 THEN '948C-28'
        WHEN 4 THEN '0403033530'
        WHEN 5 THEN '2007-07-03'
        WHEN 6 THEN '591.26 ft'
        WHEN 7 THEN 'Kelly bushing at 603.26 ft'
        WHEN 8 THEN 'N/A explicitly shown as the base of fresh water'
        WHEN 9 THEN 'N/A explicitly shown as the base of USDW'
        WHEN 10 THEN '14, 9.625, and 7 inch casing sizes shown'
        WHEN 12 THEN 'Plain End and LT&C shown'
        WHEN 13 THEN '36.71, 36.00, and 23.00 ppf shown'
        WHEN 14 THEN 'Casing bottom depths shown'
        WHEN 17 THEN 'Perforation depths shown'
        WHEN 18 THEN '24 one-foot intervals shown'
        WHEN 32 THEN '24, 12.25, and 8.75 inch intervals shown'
        WHEN 33 THEN '52, 205, and 2174 ft drilled depths shown'
        WHEN 42 THEN 'Tulare, San Joaquin/Etchegoin, and Reef Ridge Diatomite'
        WHEN 43 THEN '70.25, 670.03, and 710.00 ft marker tops'
        WHEN 46 THEN 'Three named marker records shown'
        WHEN 47 THEN 'Three marker-top depths shown'
        WHEN 55 THEN '13.5 and 12.0 ppg shown'
        WHEN 56 THEN '1.74 and 2.71 cf/sk shown'
        WHEN 57 THEN 'Class C cement shown for two documented jobs'
        WHEN 58 THEN 'Additives shown for two documented jobs'
        WHEN 59 THEN 'Measured depths are shown throughout W01'
    END,
    explanation = 'Required value is demonstrated in W01.'
WHERE requirement_id IN (
    1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 17, 18, 32, 33,
    42, 43, 46, 47, 55, 56, 57, 58, 59
);

UPDATE diagram_requirement_results
SET status = 'MET',
    evidence = CASE requirement_id
        WHEN 11 THEN '14-inch casing lists schedule SCH 20 rather than a casing grade'
        WHEN 37 THEN 'Cement fill is shown and described for the 9.625-inch and 7-inch casing jobs'
        WHEN 38 THEN 'Cement-fill top depths are shown for the documented jobs'
        WHEN 39 THEN 'Cement-fill bottom depths are shown for the documented jobs'
    END,
    explanation = 'An answer is visibly supplied on W01; factual accuracy and completeness beyond presence are outside the review scope.'
WHERE requirement_id IN (11, 37, 38, 39);

UPDATE diagram_requirement_results
SET status = 'MISSING',
    evidence = NULL,
    explanation = 'No answer is visibly supplied on W01.'
WHERE requirement_id IN (40, 41, 48, 49, 50, 51);

CREATE INDEX idx_wellbores_diagram ON wellbores(diagram_number);
CREATE INDEX idx_results_diagram_status ON diagram_requirement_results(diagram_number, status);
CREATE INDEX idx_requirements_section ON spec_requirements(section_id);
