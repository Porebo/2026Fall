"""Reviewed source observations for U25; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U25", "Aera Energy LLC")
u.page_panel(1, (10, 10, 590, 765))
u.badge_size = (9, 6)
u.row_aligned_badges = True
u.add(1, "Aera Energy LLC", u.find("Aera Energy LLC"))
u.add(3, "8298C-2", u.find("8298C-2"))
u.add(4, "0403064628", u.find("0403064628"))
u.add(5, "11/24/2018", u.find("11/24/2018"))
u.add(6, "Ground elevation 582.51 ft", u.find("582.51"))
u.add(7, "Kelly Bushing datum 596.51 ft", u.find("596.51"))
u.add(8, "Base of fresh water MD: N/A", u.find("N/A", occurrence=1))
u.add(9, "Base of USDW MD: N/A", u.find("N/A", occurrence=0))
u.add(10, "Casing 14.0000, 9.6250, and 5.5000 in",
      u.find("14.0000", occurrence=1), u.find("9.6250", occurrence=2),
      u.find("5.5000", occurrence=4))
u.add(12, "14-in casing plain end; 9.625-in and 5.5-in casing LTC",
      u.find("PLAIN END"), u.find("LTC", occurrence=0), u.find("LTC", occurrence=1))
u.add(13, "Casing weights 36.75, 36.00, and 15.50 lb/ft",
      u.find("36.75ppf"), u.find("36.00ppf"), u.find("15.50ppf", occurrence=0))
u.add(14, "Casing shoes 54.0, 203.0, and 2,055.4 ft MD",
      u.find("54.0", occurrence=2), u.find("203.0", occurrence=1), u.find("2,055.4"))
perf_rows = (240.9, 256.0, 270.1, 284.2, 298.2, 312.3,
             494.8, 517.3, 537.1, 556.7, 576.4, 593.2)
tops = ("1,075", "1,115", "1,145", "1,175", "1,205", "1,235",
        "1,775", "1,815", "1,845", "1,875", "1,905", "1,925")
intervals = ("1,075.000–1,075.100", "1,115.000–1,115.100",
             "1,145.000–1,146.000", "1,175.000–1,176.000",
             "1,205.000–1,206.000", "1,235.000–1,236.000",
             "1,775.000–1,775.100", "1,815.000–1,815.100",
             "1,845.000–1,846.000", "1,875.000–1,876.000",
             "1,905.000–1,906.000", "1,925.000–1,926.000")
u.add(17, "Perforation tops " + ", ".join(tops) + " ft MD",
      *(loc(1, 225, y, 255, y + 6) for y in perf_rows))
u.add(18, "Perforation intervals " + ", ".join(intervals) + " ft MD",
      *(loc(1, 225, y, 287, y + 6) for y in perf_rows))
u.add(30, "Permanent Packer, 1,265–1,268 ft MD", u.find("Permanent Packer"))
u.add(32, "Tubing hanger, pup joint, tubing, no-go nipple, and seal assembly",
      u.find("Tubing Hanger"), u.find("Pup Joint"), u.find("Tubing", occurrence=2),
      u.find("No Go Nipple"), u.find("Seal Assembly"))
hole_rows = [loc(1, 514, 131, 574, 138), loc(1, 514, 145, 574, 152),
             loc(1, 514, 666, 574, 673)]
u.add(33, "Hole details 24.00, 12.25, and 8.75 in; cement-stage table "
      "also lists 8.7500 in for both stages", *hole_rows,
      loc(1, 67, 191, 85, 198), loc(1, 67, 226, 85, 232))
u.add(34, "Hole depths 54.00, 208.00, and 2,065.00 ft MD", *hole_rows)
stage_names = [u.find("Primary", occurrence=0), u.find("Primary", occurrence=1)]
u.add(38, "Primary cement fills for 9.625-in and 5.5-in casing", *stage_names)
u.add(39, "Cement fill tops 15 and 14 ft MD",
      loc(1, 116, 191, 125, 198), loc(1, 116, 226, 125, 232))
u.add(40, "Cement fill bottoms 203 and 2,055 ft MD",
      loc(1, 149, 191, 165, 198), loc(1, 149, 226, 165, 232))
u.add(47, "Markers Tulare, San Joaquin/Etchegoin, and Reef Ridge Diatomite",
      u.find("Tulare"), u.find("San Joaquin/Etchegoin"), u.find("Reef Ridge Diatomite"))
u.add(48, "Marker tops 186.16, 876.15, and 888.68 ft MD",
      u.find("186.16"), u.find("876.15"), u.find("888.68"))
u.add(81, "Primary jobs dated 11/25/2018 and 11/27/2018",
      *stage_names, u.find("11/25/2018"), u.find("11/27/2018"))
u.add(88, "Orientation: Directional", u.find("Directional"))
u.single_borehole("Wellbore 00", loc(1, 80, 42, 89, 49))

u.uncertain([2, 3], "Well 8298C-2 is stated, but no lease name is shown; the "
            "screening-log lease Belridge I is not substituted for diagram evidence.")
u.uncertain([8, 9, 53, 54], "Freshwater and USDW boxes explicitly say N/A for "
            "Base MD, so MD points are MET. No TVD answer is stated.")
u.uncertain([10, 11, 12, 13, 14], "All three casing strings provide sizes, "
            "connection types and weights. SCH 10 is treated as pipe schedule, "
            "not a stated conductor steel grade, so grade is MISSING. Casing-table "
            "base 2,055.4 ft is used as the production shoe, although the final "
            "schematic component ends at 2,054.92 ft.")
u.uncertain([30, 32, 35, 36, 37], "PLUG DETAILS contains a tubing assembly and "
            "permanent packer, not cement plugs. The listed component MD ranges "
            "support the equipment calls rather than separate plug-depth points.")
u.uncertain([33, 34], "Hole details give 24.00, 12.25 and 8.75 in. Both cement "
            "stages separately print hole size 8.7500 in, including the 9.625-in "
            "casing stage. The draft retains the source values without judging them.")
u.uncertain([38, 39, 40, 81, 82, 83, 84, 85, 86], "Both Primary cement stages "
            "are dated and have MD endpoints, but neither shows slurry volume, "
            "density, yield, type, or additives.")
u.uncertain([43, 44, 45, 46, 47, 48], "The three names are explicitly listed "
            "under MARKER DETAILS; formation and zone classifications are not inferred.")
u.uncertain([87, 88, 89], "Directional is treated as an explicit deviation "
            "statement answering inclination only. No path MD stations or azimuth "
            "are stated; confirm that categorical interpretation.")

u.add_excess("Well type", [
    ("type", "Injector", u.find("Injector"), "Well type is not a checklist point."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "2,030.16 ft", u.find("2,030.16ft", occurrence=1),
     "Plug-back MD is not an identified cement plug."),
])
u.add_excess("Total depth", [
    ("TD MD", "2,065 ft", u.find("2,065ft"), "Header total depth is not a separate point."),
])
u.add_excess("Flag joint", [
    ("flag joint", "1,059 ft", u.find("FLAG JOINT"), "Flag joint is not a scored point."),
])
u.add_excess("Intermediate casing-component endpoints", [
    ("upper production", "1,059.33 ft", u.find("1,059.33ft"),
     "Intermediate component endpoint is not a string shoe."),
    ("middle production", "2,030.16 ft", u.find("2,030.16ft", occurrence=0),
     "Intermediate component endpoint is not a string shoe."),
])
u.add_excess("Perforation shot density", [
    (f"interval {index}", f"{density:.3f} shot/ft", loc(1, 288, y, 329, y + 6),
     "Shot density is not scored.")
    for index, (y, density) in enumerate(zip(
        perf_rows, (1, 1, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4)), 1)
])
u.uncertain([30, 32], "Confirm the new excess category well type and whether the "
            "equipment depth ranges should be separately counted as excess data.")
u.add_provenance("Preparer initials", "xyz", u.find("xyz"))
u.add_provenance("Drawing date", "7/24/2023", u.find("7/24/2023"))

if __name__ == "__main__":
    u.build()
