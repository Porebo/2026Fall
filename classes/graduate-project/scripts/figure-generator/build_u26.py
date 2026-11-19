"""Reviewed source observations for U26; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U26", "Chevron U.S.A. Inc.")
u.page_panel(1, (25, 27, 570, 820))
u.add(1, "Chevron U.S.A. Inc.", u.find("Chevron U.S.A. Inc."))
u.add(2, "1Y (in well name 1Y 2008V)", loc(1, 364, 31, 373, 39))
u.add(3, "2008V", u.find("2008V", occurrence=1))
u.add(4, "0403064453", u.find("0403064453", occurrence=0))
u.add(5, "11/27/2018", u.find("11/27/2018"))
u.add(6, "Ground elevation 885.10 ft MSL", u.find("885.10"))
u.add(7, "Kelly Bushing elevation 898.60 ft MSL", u.find("898.60"))
casings = [loc(1, 68, 208, 235, 222), loc(1, 68, 225, 235, 237),
           loc(1, 68, 386, 235, 396), loc(1, 68, 677, 235, 689),
           loc(1, 100, 713, 235, 725)]
u.add(10, "Casing sizes 18.000, 13.375, 9.625, and 5.500 in", *casings)
u.add(11, "18-in H-40; 13.375-in and 9.625-in K-55; 5.5-in K-55 "
      "and K-40 segments", *casings)
u.add(13, "Casing weights 78.00, 54.50, 40.00, and 17.00 lb/ft", *casings)
u.add(14, "18-in bottom 93; 13.375-in shoe 360; 9.625-in shoe 1,047; "
      "5.5-in shoe 1,558 ft MD", casings[0], loc(1, 360, 294, 520, 303),
      loc(1, 360, 453, 520, 462), loc(1, 360, 752, 520, 762))
perf = loc(1, 125, 610, 235, 619)
u.add(17, "Open perforation depths 1,300 and 1,330 ft MD", perf)
u.add(18, "Open perforation interval 1,300–1,330 ft MD", perf)
u.add(32, "Tubing hanger, landing sub, tubing, three float collars, "
      "wireline re-entry guide, and cast-iron bridge plug",
      loc(1, 360, 133, 460, 142), loc(1, 360, 152, 535, 169),
      loc(1, 360, 180, 525, 189), loc(1, 60, 544, 235, 552),
      loc(1, 360, 247, 515, 260), loc(1, 360, 403, 520, 420),
      loc(1, 360, 565, 535, 577), loc(1, 360, 655, 510, 664),
      loc(1, 360, 699, 515, 712))
holes = [loc(1, 360, 203, 500, 213), loc(1, 360, 316, 500, 326),
         loc(1, 360, 476, 505, 486), loc(1, 360, 766, 515, 776)]
u.add(33, "Hole diameters 20.0000, 16.0000, 12.2500, and 8.5000 in", *holes)
u.add(34, "Hole sections 14–93, 93–379, 379–1,052, and 1,052–1,570 ft MD", *holes)
plug = loc(1, 360, 742, 495, 752)
u.add(35, "Plug - Cement", plug)
u.add(36, "Cement plug top 1,514 ft MD", plug)
u.add(37, "Cement plug bottom 1,558 ft MD", plug)
fills = [loc(1, 65, 193, 235, 207), loc(1, 65, 290, 235, 307),
         loc(1, 65, 447, 235, 470), loc(1, 60, 728, 235, 767)]
u.add(38, "Cement behind the four casing strings", *fills)
u.add(39, "Casing cement-fill tops 14 ft MD", *fills)
u.add(40, "Casing cement-fill bottoms 93, 360, 1,047, and 1,558 ft MD", *fills)
tops = [loc(1, 360, 360, 520, 370), loc(1, 360, 521, 505, 531)]
u.add(43, "San Joaquin–Etchegoin and Antelope Shale", *tops)
u.add(44, "Estimated formation tops 724 and 1,136 ft MD", *tops)
u.add(47, "San Joaquin–Etchegoin and Antelope Shale top markers", *tops)
u.add(48, "Estimated top markers 724 and 1,136 ft MD", *tops)
u.add(81, "Cement behind four casing strings, two named Top Jobs, and Plug - Cement",
      *fills, loc(1, 70, 453, 235, 467), loc(1, 70, 748, 235, 764), plug)
u.add(88, "Well Profile: Directional", u.find("Directional"))
u.single_borehole("One borehole shown", loc(1, 240, 114, 356, 775))

u.uncertain([2, 3], "1Y is provisionally treated as the lease identifier in well "
            "name 1Y 2008V; Fee is shown under Fee/Lease but appears to describe "
            "tenure rather than the lease name. Confirm the split.")
u.uncertain([10, 11, 13, 14], "Four casing strings are distinguished from tubing. "
            "The 18-in component bottom is treated as its shoe; the other three "
            "shoes are explicitly labelled. The 5.5-in string has K-55 and K-40 "
            "segments. Confirm the manually transcribed raster labels.")
u.uncertain([17, 18], "The one explicitly open perforation interval is "
            "1,300–1,330 ft MD.")
u.uncertain([32, 35, 36, 37], "The cast-iron bridge plug is treated as other "
            "equipment, not a cement plug. The separately labelled Plug - Cement "
            "is credited with its printed MD endpoints.")
u.uncertain([35, 38, 39, 40, 81], "Four physical cement-behind-casing intervals, "
            "two Top Jobs within the 9.625-in and 5.5-in narratives, and one cement "
            "plug are retained. The plug may share a job with the 5.5-in fill; the "
            "Top Jobs have no separate fill interval and are not assumed to be "
            "additional physical fills. Confirm grouping and job identification.")
u.uncertain([43, 44, 47, 48], "The two estimated named tops are treated as both "
            "formation tops and markers; no accuracy judgment is made.")
u.uncertain([82, 83, 84, 85, 86], "The 18-in fill explicitly says Unknown Mix/Volume; "
            "unknown volume counts as an answer. Its density, yield, cement class "
            "and additives are not separately stated, and no separate slurry details "
            "are linked to the cement plug. Repeated-job slurry points remain MISSING.")
u.uncertain([87, 88, 89], "Directional is treated as an explicit deviation "
            "statement answering inclination only; no path MD stations or azimuth "
            "are shown.")
u.uncertain([90], "Only one borehole is drawn; no separate original-hole label is visible.")
u.uncertain([10, 17, 32, 33, 38], "The schematic labels are rasterized and were "
            "transcribed and positioned manually; confirm the readings.")

u.add_excess("Well location", [
    ("field", "Cymric", u.find("Cymric"), "Location is not scored."),
    ("county", "Kern (2)", u.find("Kern (2)"), "Location is not scored."),
    ("state", "California", u.find("California"), "Location is not scored."),
    ("section", "1", loc(1, 100, 72, 106, 80), "PLSS location is not scored."),
    ("township", "30S", u.find("30S"), "PLSS location is not scored."),
    ("range", "21E", u.find("21E"), "PLSS location is not scored."),
    ("meridian", "MD", u.find("MD"), "PLSS location is not scored."),
])
u.add_excess("Lease tenure", [
    ("Fee/Lease", "Fee", u.find("Fee", occurrence=1), "Tenure is not a scored point."),
])
u.add_excess("API12", [
    ("API12", "040306445300", u.find("040306445300"), "API12 is not the API10 point."),
])
u.add_excess("Datum correction factor", [
    ("correction factor", "13.50 ft", u.find("13.50"), "Datum height is not scored."),
])
u.add_excess("Completion date", [
    ("completion date", "12/14/2018", u.find("12/14/2018"), "Completion date is not scored."),
])
u.add_excess("Casing IDs and drift", [
    ("18-in", "17.194-in ID; 17.007-in drift", loc(1, 135, 208, 220, 219),
     "Casing ID and drift are not separately scored."),
    ("13.375-in", "12.615-in ID; 12.459-in drift", loc(1, 135, 225, 220, 234),
     "Casing ID and drift are not separately scored."),
    ("9.625-in", "8.835-in ID; 8.679-in drift", loc(1, 135, 386, 220, 395),
     "Casing ID and drift are not separately scored."),
    ("5.5-in", "4.892-in ID; 4.767-in drift", loc(1, 135, 677, 220, 686),
     "Casing ID and drift are not separately scored."),
])
u.add_excess("Cement returns", [
    ("18-in", "Unknown returns", loc(1, 68, 200, 96, 207),
     "Returns are not slurry volume."),
    ("13.375-in", "32 bbl returned", loc(1, 117, 294, 165, 302),
     "Returns are not a separate scored point."),
    ("9.625-in", "No Returns", loc(1, 147, 450, 180, 457),
     "Returns are not a separate scored point."),
    ("5.5-in", "No Returns", loc(1, 130, 747, 165, 755),
     "Returns are not a separate scored point."),
])
u.uncertain([2, 38], "Confirm the new excess category lease tenure and grouped "
            "cement-return readings.")

if __name__ == "__main__":
    u.build()
