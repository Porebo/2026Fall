"""Reviewed source observations for U27; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U27", "Not stated")
u.page_panel(1, (25, 27, 570, 820))
u.add(2, "McDonald", u.find("McDonald", occurrence=1))
u.add(3, "505", u.find("505", occurrence=1))
u.add(4, "0403013228", u.find("0403013228", occurrence=0))
u.add(5, "6/28/1999", u.find("6/28/1999"))
u.add(6, "Ground elevation 1,414.00 ft MSL", u.find("1414.00"))
u.add(7, "Kelly Bushing elevation 1,424.00 ft MSL", u.find("1424.00"))
casings = [loc(1, 115, 145, 235, 153), loc(1, 65, 723, 235, 733),
           loc(1, 100, 742, 235, 752)]
u.add(10, "Casing sizes 12.750 and 5.500 in", *casings)
u.add(11, "12.750-in A53B; 5.500-in J-55", *casings)
u.add(13, "Casing weights 33.83 and 17.00 lb/ft", *casings)
u.add(14, "12.750-in casing bottom 50; 5.500-in guide shoe bottom 1,800 ft MD",
      casings[0], loc(1, 360, 751, 520, 762))
perf_rows = [(95, 152), (95, 183), (95, 220), (115, 659), (115, 669),
             (115, 686), (115, 703), (115, 714)]
perfs = [loc(1, x, y, 235, y + 9) for x, y in perf_rows]
u.add(17, "Perforation depths 95, 195, 295, 1,502, 1,532, 1,578, 1,620, "
      "and 1,650 ft MD", *perfs)
u.add(18, "Perforation intervals 95–100, 195–200, 295–300, 1,502–1,502, "
      "1,532–1,532, 1,578–1,578, 1,620–1,620, and 1,650–1,650 ft MD", *perfs)
u.add(28, "Plug - Fill at 1,736–1,776 ft MD", loc(1, 360, 718, 495, 727))
u.add(32, "Float collar and guide shoe", loc(1, 360, 729, 520, 741),
      loc(1, 360, 751, 520, 762))
holes = [loc(1, 360, 147, 505, 156), loc(1, 360, 766, 515, 776)]
u.add(33, "Hole diameters 20.0000 and 7.8750 in", *holes)
u.add(34, "Hole sections 10–50 and 50–1,801 ft MD", *holes)
plugs = [loc(1, 360, 248, 535, 268), loc(1, 360, 568, 535, 583),
         loc(1, 360, 687, 535, 701), loc(1, 360, 742, 500, 751)]
u.add(35, "Four Plug - Cement entries", *plugs)
u.add(36, "Cement-plug tops 10, 408, 1,276, and 1,776 ft MD", *plugs)
u.add(37, "Cement-plug bottoms 408, 1,276, 1,736, and 1,800 ft MD", *plugs)
fills = [loc(1, 65, 120, 235, 141), loc(1, 60, 752, 235, 774)]
u.add(38, "Cement behind the 12.750-in and 5.500-in casing", *fills)
u.add(39, "Casing-cement tops 10 ft MD", *fills)
u.add(40, "Casing-cement bottoms 50 and 1,800 ft MD", *fills)
u.add(81, "Two cement-behind-casing entries and four Plug - Cement entries",
      *fills, *plugs)
u.add(88, "Well Profile: Directional", u.find("Directional"))
u.single_borehole("One borehole shown", loc(1, 240, 114, 356, 775))

u.uncertain([1, 2, 3], "No operator is explicitly stated. McDonald and 505 are "
            "explicitly labelled as CalGEM lease and well number.")
u.uncertain([10, 11, 13, 14], "Both casing strings provide size, grade and weight. "
            "The 12.750-in bottom is treated as its shoe and the production guide "
            "shoe is explicitly labelled 1,799–1,800 ft. Confirm the raster readings.")
u.uncertain([17, 18], "All eight perforation rows are included: three Closed-Squeezed "
            "intervals and five Closed zero-length intervals. Status does not remove "
            "a displayed perforation from the presence-only score.")
u.uncertain([23, 28, 32, 35], "The casing is said to be cut off 5 ft below ground, "
            "but an MD cut depth is not stated. Plug - Fill is treated as an other "
            "integrity feature, not automatically a cement plug or fluid. Float "
            "collar and guide shoe are treated as other equipment.")
u.uncertain([35, 36, 37, 38, 39, 40, 81], "Four explicit cement plugs and two "
            "cement-behind-casing intervals are recorded. The lowermost cement plug "
            "may share a job with the 5.5-in fill; the draft identifies each displayed "
            "entry by its description without deduplicating. Confirm the grouping.")
u.uncertain([82, 83, 84, 85, 86], "Several entries give slurry quantities and "
            "properties, but the lowermost cement plug has no separate slurry details; "
            "the first casing fill also says Unknown Mix. The repeated-job slurry "
            "points remain MISSING.")
u.uncertain([87, 88, 89], "Directional is treated as an explicit deviation "
            "statement answering inclination only; no path MD stations or azimuth "
            "are shown.")
u.uncertain([90], "Only one borehole is drawn; no separate original-hole label is visible.")
u.uncertain([10, 17, 28, 33, 35, 38], "The schematic labels are rasterized and "
            "were transcribed and positioned manually; confirm the readings.")

u.add_excess("Well location", [
    ("field", "Midway", u.find("Midway"), "Location is not scored."),
    ("county", "Kern (2)", u.find("Kern (2)"), "Location is not scored."),
    ("state", "California", u.find("California"), "Location is not scored."),
    ("section", "26", u.find("26", occurrence=1), "PLSS location is not scored."),
    ("township", "31S", u.find("31S"), "PLSS location is not scored."),
    ("range", "22E", u.find("22E"), "PLSS location is not scored."),
    ("meridian", "MD", u.find("MD"), "PLSS location is not scored."),
])
u.add_excess("API12", [
    ("API12", "040301322800", u.find("040301322800"), "API12 is not the API10 point."),
])
u.add_excess("Datum correction factor", [
    ("correction factor", "10.00 ft", u.find("10.00"), "Datum height is not scored."),
])
u.add_excess("Completion date", [
    ("completion date", "10/29/1999", u.find("10/29/1999"), "Completion date is not scored."),
])
u.add_excess("Perforation status", [
    (f"interval {index}", "Closed-Squeezed" if index <= 3 else "Closed",
     loc(1, 125 if index <= 3 else 150, y, 185, y + 9),
     "Perforation status is not a separate scored point.")
    for index, (_, y) in enumerate(perf_rows, 1)
])
u.add_excess("Cement returns", [
    ("surface casing", "Unknown Returns", loc(1, 105, 127, 165, 136),
     "Returns are not slurry volume."),
    ("production casing", "25 bbl returns", loc(1, 60, 758, 235, 773),
     "Returns are not a separate scored point."),
])
u.add_excess("Well-operation events", [
    ("site restoration", "4/18/2023", loc(1, 360, 118, 400, 127), "Event date is not scored."),
    ("TOC witness", "4/17/2023", loc(1, 360, 132, 400, 140), "Event date is not scored."),
    ("casing cut-off", "4/12/2023", loc(1, 360, 141, 400, 149), "Event date is not scored."),
    ("TOC tag 408", "1/13/2023", loc(1, 360, 270, 400, 278), "Tag date is not scored."),
    ("TOC tag 1276", "1/12/2023", loc(1, 360, 584, 400, 592), "Tag date is not scored."),
    ("cleanout tag", "1/12/2023", loc(1, 360, 702, 400, 711), "Tag date is not scored."),
    ("cement bond log", "10/05/1999", loc(1, 360, 711, 400, 719), "Log date is not scored."),
])
u.uncertain([17, 18, 23], "Confirm the new excess categories perforation status "
            "and well-operation events; the cut-off distance is not converted to MD.")

if __name__ == "__main__":
    u.build()
