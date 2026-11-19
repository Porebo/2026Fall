"""Reviewed source observations for U21; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U21", "Not explicitly stated (bry logo)", printed_date="6/18/2025")
u.page_panel(1, (15, 15, 600, 772), layout=(230, 102, 330, 680), label="Source page 1")
u.page_panel(2, (315, 78, 598, 410), layout=(565, 102, 203, 680),
             label="Source page 2: continued tables")
u.add(2, "FA (in well name FA 52-69)", loc(1, 318, 95, 328, 105))
u.add(3, "52-69", loc(1, 330, 95, 350, 105))
u.add(4, "0403065482", u.find("0403065482", occurrence=0))
u.add(5, "5/30/2019", u.find("5/30/2019"))
u.add(6, "Ground elevation 1,348.65 ft", u.find("1,348.65"))
casing_y = (324, 371.5, 451.5, 573.9)
u.add(10, "Conductor 14; sidetrack surface 9 5/8; sidetrack and original "
      "production 5 1/2 in", *(loc(1, 371, y, 390, y + 9) for y in casing_y))
u.add(11, "Conductor H-40; sidetrack surface J-55; both production strings K-55",
      *(loc(1, 434, y, 452, y + 9) for y in casing_y))
u.add(13, "Conductor 32.70; sidetrack surface 36.00; both production strings "
      "17.00 lb/ft", *(loc(1, 476, y, 497, y + 9) for y in casing_y))
u.add(14, "Conductor 93; sidetrack surface 1,134; sidetrack production 1,732; "
      "original production 1,754 ft MD",
      *(loc(1, 551, y, 579, y + 9) for y in casing_y))
perf_y = (302.4, 329.1, 355.7, 382.3)
u.add(17, "Perforation tops 1,407, 1,520, 1,610, and 1,628 ft MD",
      *(loc(2, 398, y, 425, y + 9) for y in perf_y))
u.add(18, "Perforation intervals 1,407–1,427; 1,520–1,540; 1,610–1,626; "
      "1,628–1,632 ft MD", *(loc(2, 398, y, 465, y + 9) for y in perf_y))
u.add(32, "Casing insert and float collars", u.find("Insert"),
      u.find("Float Collar", occurrence=0), u.find("Float Collar", occurrence=1))
prod_plug = loc(1, 233, 598, 300, 620)
plug_names = [
    prod_plug, loc(1, 318, 730, 385, 740), loc(1, 318, 758, 385, 768),
    *(loc(2, 318, y, 385, y + 9) for y in (106.5, 134.5, 162.5, 190.5, 218.5)),
]
plug_tops = [
    loc(1, 244, 612, 264, 620), loc(1, 491, 730, 518, 740),
    loc(1, 491, 758, 518, 768),
    *(loc(2, 491, y, 518, y + 9) for y in (106.2, 134.3, 162.4, 190.5, 218.7)),
]
plug_bottoms = [
    loc(1, 265, 612, 286, 620), loc(1, 520, 730, 547, 740),
    loc(1, 520, 758, 547, 768),
    *(loc(2, 520, y, 547, y + 9) for y in (106.2, 134.3, 162.4, 190.5, 218.7)),
]
u.add(35, "Production cement plug; six abandonment-plug entries; cement KO plug",
      *plug_names)
u.add(36, "Plug tops 1,714; 1,420; 1,395; 1,395; 1,395; 1,010; 150; 30 ft MD",
      *plug_tops)
u.add(37, "Plug bottoms 1,754; 1,428; 1,420; 1,395; 1,395; 1,395; 1,010; "
      "150 ft MD", *plug_bottoms)
fill_names = [
    loc(1, 318, 674, 384, 684), loc(1, 318, 702, 411, 712),
    loc(2, 318, 246, 413, 256), loc(2, 318, 274, 423, 284),
]
fill_rows = [(1, 674.6), (1, 702.5), (2, 246.8), (2, 274.8)]
u.add(38, "Conductor, original production, sidetrack surface, and sidetrack "
      "production cement fills", *fill_names)
u.add(39, "All four fill tops 13 ft MD",
      *(loc(page, 491, y, 508, y + 9) for page, y in fill_rows))
u.add(40, "Fill bottoms 93, 1,754, 1,134, and 1,732 ft MD",
      *(loc(page, 520, y, 547, y + 9) for page, y in fill_rows))
u.add(45, "Original-hole zones Tulare, San Joaquin, Etchegoin, Reef Ridge Diatomite",
      u.find("Tulare"), u.find("San Joaquin"), u.find("Etchegoin"),
      loc(1, 388, 276, 432, 294))
u.add(46, "Original-hole zone tops 690, 941, 1,032, and 1,130 ft MD",
      *(loc(1, 459, y, 486, y + 9) for y in (224.7, 241.9, 259.2, 276.5)))
u.add(81, "Four named casing fills, production cement plug, six Abandonment Plug "
      "entries, and Cement KO Plug", *fill_names, *plug_names)
u.add(90, "Original Hole; Sidetrack",
      u.find("Original Hole", occurrence=0), u.find("Sidetrack", occurrence=2))
u.applicable_boreholes()

u.uncertain([1, 2, 3], "A bry logo is visible but no operator name is explicitly labelled. "
            "FA is provisionally treated as the lease abbreviation and 52-69 as the well "
            "number within FA 52-69; confirm both calls.")
u.uncertain([7], "KB–ground height is stated, but an absolute reference elevation is not.")
u.uncertain([10, 11, 13, 14], "All four casing rows are retained, including the two "
            "separate 5 1/2-in production strings. Their set depths are treated as shoes.")
u.uncertain([17, 18], "All four perforation-table rows are included. The table does not "
            "explicitly associate each row with a borehole; do not infer that from dates.")
u.uncertain([32], "The explicitly listed casing insert and float collars are treated as "
            "other in-well equipment; confirm that classification.")
u.uncertain([33, 34], "Two original-hole sections give diameters and MD depths, but no "
            "separate sidetrack hole diameter or final hole depth is shown. Under the "
            "repeated-borehole rule the draft leaves these points MISSING.")
u.uncertain([35, 36, 37, 38, 39, 40, 81], "The production-cement plug is displayed in "
            "the schematic and may share its job with the original production fill. The "
            "tables also list six abandonment-plug entries, including two distinct rows "
            "both displayed as 1,395–1,395 ft, plus one KO plug and four casing fills. "
            "All displayed instances and endpoints are retained without deduplication.")
u.uncertain([45, 46, 43, 44, 47, 48], "The four names and depths are in a Zones table "
            "for the original hole; the draft does not infer separate formation or marker "
            "classifications or a sidetrack zone list.")
u.uncertain([81, 82, 83, 84, 85, 86], "Descriptions identify the displayed fills and "
            "plugs. Slurry details for several entries are present, but not for every "
            "conductor, sidetrack, and zero-length plug entry, so repeated-job slurry "
            "points are MISSING. Confirm whether any entries share a job.")
u.uncertain([87, 88, 89, 90], "Both Original Hole and Sidetrack are explicitly designated, "
            "so point 90 is applicable and MET. Deviated (15° to 30°) is explicitly tied "
            "to Original Hole only; the sidetrack has no separate MD path, inclination, "
            "or azimuth, so the three repeated-borehole path points are MISSING.")

u.add_excess("Well location", [
    ("field", "Midway Sunset MN RPT", loc(1, 383, 95, 425, 123), "Location is not scored."),
    ("section", "11", loc(1, 318, 157, 327, 166), "PLSS location is not scored."),
    ("township", "31S", loc(1, 344, 157, 358, 166), "PLSS location is not scored."),
    ("range", "22E", loc(1, 376, 157, 391, 166), "PLSS location is not scored."),
    ("meridian", "MD", loc(1, 402, 157, 415, 166), "PLSS location is not scored."),
    ("latitude", "35.2513150000", u.find("35.2513150000"), "Location is not scored."),
    ("longitude", "-119.5800220000", u.find("-119.5800220000"), "Location is not scored."),
    ("datum", "NAD 83", loc(1, 565, 157, 594, 166), "Location datum is not scored."),
])
u.add_excess("KB–ground height", [
    ("KB–ground", "13.00 ft", loc(1, 368, 139, 389, 149),
     "Height is not an absolute reference elevation."),
])
u.add_excess("Rig-release date", [
    ("rig release", "6/1/2019", loc(1, 469, 139, 500, 149), "Date is not scored."),
])
u.add_excess("Plug-back depths", [
    ("original", "1,714.0 ft", loc(1, 488, 104, 517, 114), "PBTD is not a cement-plug depth."),
    ("sidetrack", "1,688.0 ft", loc(1, 488, 122, 516, 131), "PBTD is not a cement-plug depth."),
])
u.add_excess("Casing inside diameters", [
    (name, value, loc(1, 402, y, 423, y + 9), "Inside diameter is not scored.")
    for name, value, y in zip(("conductor", "ST surface", "ST production", "production"),
                              ("13.50", "8.92", "4.89", "4.89"), casing_y)
])
u.add_excess("Casing run dates", [
    ("conductor", "4/30/2019", loc(1, 318, 324, 353, 333), "Run date is not scored."),
    ("ST surface", "2/25/2025", loc(1, 318, 371, 353, 381), "Run date is not scored."),
    ("production", "6/1/2019", loc(1, 318, 573, 349, 583), "Run date is not scored."),
])
u.add_excess("Intermediate casing-component bottoms", [
    (f"component {index}", value, loc(1, 568, y, 595, y + 9),
     "Intermediate component bottom is not a string shoe.")
    for index, (value, y) in enumerate((
        ("1,092.9", 390.3), ("1,093.0", 401.1), ("1,133.0", 411.9),
        ("1,322.5", 470.2), ("1,366.0", 481.0), ("1,668.1", 492.5),
        ("1,688.0", 503.3), ("1,689.2", 523.5), ("1,731.0", 534.3),
        ("1,072.0", 592.6), ("1,092.0", 603.4), ("1,714.0", 614.2),
        ("1,715.0", 625.0)), 1)
])
u.add_excess("Flag joint", [
    ("flag joint", "1,072–1,092 ft", u.find("Flag Joint"), "Flag joint is not a scored point."),
])
u.add_excess("Perforation details", [
    (f"date {index}", value, loc(2, 318, y, 353, y + (18 if index == 1 else 9)),
     "Perforation date is not scored.")
    for index, (value, y) in enumerate(
        (("12/11/2019", 302.4), ("3/17/2025", 329.1),
         ("3/17/2025", 355.7), ("3/17/2025", 382.3)), 1)
] + [
    (f"shots and comment {index}", value, loc(2, 479, y, 595, y + 18),
     "Shot counts, density and hole size are not scored.")
    for index, (value, y) in enumerate(
        (("80, 80; 4 JHPF, 3/8 in", 302.4), ("80, 80; 4 JHPF, 3/8 in", 329.1),
         ("64, 64; 4 JHPF, 3/8 in", 355.7), ("16, 16; 4 JHPF, 3/8 in", 382.3)), 1)
])
u.add_excess("Cement returns", [
    ("conductor", "0.0", loc(1, 577, 674, 594, 684), "Returns are not slurry volume."),
    ("original production", "18.0", loc(1, 577, 702, 595, 712), "Returns are not slurry volume."),
    ("sidetrack surface", "45.0", loc(2, 577, 246, 595, 256), "Returns are not slurry volume."),
    ("sidetrack production", "0.0", loc(2, 577, 274, 595, 284), "Returns are not slurry volume."),
])
u.uncertain([32, 38, 90], "Confirm the new excess categories flag joint and grouped "
            "perforation details; cement-return fields are distinguished from slurry amounts.")
u.add_provenance("Drawing timestamp", "6/18/2025 4:53:15 PM", loc(1, 186, 80, 255, 87))
u.add_provenance("Report printed", "6/18/2025", loc(1, 498, 761, 596, 771))
u.add_provenance("Report website", "www.peloton.com", u.find("www.peloton.com"))

if __name__ == "__main__":
    u.build()
