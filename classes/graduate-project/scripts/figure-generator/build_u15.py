"""Reviewed source observations for U15; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U15", "Chevron U.S.A. Inc.")
u.page_panel(1, (28, 25, 568, 815))
u.add(1, "Chevron U.S.A. Inc.", u.find("Chevron U.S.A. Inc."))
u.add(2, "Fee", u.find("Fee", occurrence=1))
u.add(3, "3783", u.find("3783", occurrence=1))
u.add(4, "0402970840", u.find("0402970840", occurrence=0))
u.add(5, "5/27/1984", u.find("5/27/1984"))
u.add(6, "Ground elevation 611.80 ft MSL", u.find("611.80 ft"))
u.add(7, "Derrick floor elevation 619.80 ft MSL", u.find("619.80 ft"))
conductor = loc(1, 92, 155, 237, 171)
production = [loc(1, 81, 714, 238, 729), loc(1, 81, 731, 238, 746)]
u.add(10, "Conductor 10.750 in; production 7.000 in", conductor, *production)
u.add(11, "Conductor Unknown Grade; production K-55", conductor, *production)
u.add(13, "Conductor Unknown Weight; production 23.00 lb/ft", conductor, *production)
u.add(14, "Conductor 80 ft; production float shoe 962 ft MD",
      conductor, loc(1, 364, 744, 537, 760))
perf_y = (249, 299, 317, 327, 356, 384, 489, 498, 516, 526, 578, 638)
perf_names = ("180–210", "210–283", "286–310", "310–323", "322–367", "380–408",
              "530–565", "567–570", "590–604", "606–608", "618–726", "730–753")
perf_locations = [loc(1, 118, y, 235, y + 9) for y in perf_y]
u.add(17, "Perforation tops " + "; ".join(name.split("–")[0] for name in perf_names) +
      " ft MD", *perf_locations)
u.add(18, "Perforation intervals " + "; ".join(perf_names) + " ft MD", *perf_locations)
u.add(32, "Tubing hanger, landing sub, tubing, rod subs, rods, tubing drain, "
      "shear tool, pump barrel, pump plunger, float collar and float shoe",
      loc(1, 363, 113, 535, 140), loc(1, 363, 160, 535, 186),
      loc(1, 75, 559, 238, 577), loc(1, 75, 588, 238, 636),
      loc(1, 363, 548, 535, 663), loc(1, 363, 710, 537, 725),
      loc(1, 363, 745, 537, 760))
u.add(33, "Conductor hole size not reported; production wellbore hole 9.875 in",
      loc(1, 363, 196, 537, 211), loc(1, 363, 760, 526, 770))
u.add(34, "Conductor hole 8–80 ft; production hole 80–966 ft MD",
      loc(1, 363, 196, 537, 211), loc(1, 363, 760, 526, 770))
u.add(35, "Plug - Cement", loc(1, 363, 735, 467, 744))
u.add(36, "Cement plug top 923 ft MD", loc(1, 363, 735, 467, 744))
u.add(37, "Cement plug bottom 962 ft MD", loc(1, 363, 735, 467, 744))
u.add(38, "Cement behind production casing; no record behind conductor",
      loc(1, 73, 747, 238, 769), loc(1, 363, 187, 537, 196))
u.add(39, "Cement behind production casing top 8 ft MD", loc(1, 73, 760, 238, 769))
u.add(40, "Cement behind production casing bottom 962 ft MD", loc(1, 73, 760, 238, 769))
u.add(81, "Cement behind casing; Plug - Cement",
      loc(1, 73, 747, 238, 769), loc(1, 363, 735, 467, 744))
u.single_borehole("One borehole shown", loc(1, 240, 114, 356, 770))

u.uncertain([2], "The source Fee/Lease field explicitly says Fee; screening lists the "
            "lease as Unspecified. The draft uses the source entry for scoring.")
u.uncertain([11, 12, 13, 14], "The conductor explicitly says Unknown Grade/Thread/Weight, "
            "counted as entries for grade and weight; the production casing's connection "
            "is not stated, so connection remains MISSING. The conductor bottom and "
            "production float-shoe bottom are treated as shoe depths.")
u.uncertain([17, 18], "All 12 labelled perforation intervals are included, even where "
            "intervals overlap or are adjacent; every line is a separate displayed instance.")
u.uncertain([32], "The equipment call groups the shown tubing, rods, pump, tools, "
            "float collar, and shoe; the raster source requires manual localization.")
u.uncertain([33, 34], "The conductor hole size is explicitly 'not reported', counted as "
            "an entry under the presence-only rule; the second hole has size 9.875 in. "
            "Confirm that interpretation.")
u.uncertain([35, 36, 37, 38, 39, 40, 81, 82, 83, 84, 85, 86], "The source separately "
            "labels a cement plug at 923–962 ft and cement behind casing at 8–962 ft, "
            "but does not explicitly say whether they are the same cement job. Both are "
            "identified; the draft leaves repeated-job slurry properties MISSING because "
            "no slurry details are explicitly linked to the plug. The conductor says no "
            "record of cement; that explicit statement is not treated as an additional job.")
u.uncertain([43, 44, 45, 46, 47, 48, 49, 50], "Estimated top and base of oil are shown "
            "but are not explicitly labelled formations, zones, markers, or an injection "
            "zone; the draft does not infer those classifications.")
u.uncertain([87, 88, 89], "Well Profile: N/A is a general profile entry, not an explicit "
            "MD survey, inclination, or azimuth; none of those points is inferred.")
u.uncertain([90], "Only one borehole is drawn; there is no explicit original-hole label.")

u.add_excess("Well location", [
    ("field", "Kern River", u.find("Kern River"), "Field location is not scored."),
    ("county", "Kern (1)", u.find("Kern (1)"), "County is not scored."),
    ("state", "California", u.find("California"), "State is not scored."),
    ("section", "3", loc(1, 100.2, 72.0, 103.2, 79.4), "PLSS location is not scored."),
    ("township", "29S", u.find("29S"), "PLSS location is not scored."),
    ("range", "28E", u.find("28E"), "PLSS location is not scored."),
    ("meridian", "MD", loc(1, 496.8, 72.0, 507.0, 79.4), "PLSS location is not scored."),
])
u.add_excess("API12", [
    ("API12", "040297084000", u.find("040297084000"), "The 12-digit API is not the API10 point."),
])
u.add_excess("Datum correction factor", [
    ("correction factor", "8.00 ft", u.find("8.00 ft"), "Datum height is not a scored point."),
])
u.add_excess("Completion date", [
    ("completion date", "7/5/1984", u.find("7/5/1984"), "Completion date is not scored."),
])
u.add_excess("Perforation status", [
    (f"{name} ft", "Open", loc(1, 164, y, 183, y + 9), "Status is not a scored point.")
    for name, y in zip(perf_names, perf_y)
])
u.add_excess("Estimated oil limits", [
    ("top oil", "28 ft, estimated", loc(1, 363, 148, 465, 159), "Not explicitly an injection zone."),
    ("base oil", "893 ft, estimated", loc(1, 363, 698, 469, 708),
     "Not explicitly an injection zone."),
])
u.add_excess("Noncement plug information", [
    ("fill plug", "904–923 ft MD", loc(1, 363, 725, 465, 734),
     "The fill plug is not identified as a cement plug."),
])
u.add_excess("Cement bond-log operation", [
    ("CBL", "6/02/1984 on 7-in casing at 8–888 ft", loc(1, 363, 689, 533, 698),
     "A bond-log operation is not a scored point."),
])
u.add_excess("Cement returns", [
    ("production cement returns", "120 CF", loc(1, 73, 753, 238, 763),
     "Returns are not slurry volume."),
])
u.uncertain([28, 38], "Confirm the new excess categories API12, estimated oil limits, "
            "noncement plug information, and cement-bond-log operation.")

if __name__ == "__main__":
    u.build()
