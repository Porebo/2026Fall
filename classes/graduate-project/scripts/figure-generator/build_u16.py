"""Reviewed source observations for U16; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U16", "Aera Energy LLC")
u.page_panel(1, (8, 10, 610, 708))
u.add(1, "Aera Energy LLC", u.find("Aera Energy LLC"))
u.add(3, "WWD10-27", u.find("WWD10-27"))
u.add(4, "0403047484", u.find("0403047484"))
u.add(6, "Ground elevation 509.08 ft", u.find("509.08ft"))
u.add(7, "Kelly bushing 522.08 ft", u.find("522.08ft"))
u.add(10, "20.000; 13.375; 9.625; 9.625 in",
      u.find("20.000", occurrence=1), u.find("13.375", occurrence=3),
      u.find("9.625", occurrence=3), u.find("9.625", occurrence=4))
u.add(13, "20-in 78.76; 13.375-in 54.50; both 9.625-in strings 36.00 ppf",
      u.find("78.76ppf"), u.find("54.50ppf", occurrence=0),
      u.find("36.00ppf", occurrence=0), u.find("36.00ppf", occurrence=1))
u.add(14, "Casing shoes 53, 944, 1,000, and 1,211 ft MD",
      u.find("CSG SHOE @ 53ft"), u.find("CSG SHOE @ 944ft"),
      u.find("CSG SHOE @ 1,000ft"), u.find("CSG SHOE @ 1,211ft"))
u.add(16, "Lower 9.625-in string top 944 ft MD", loc(1, 89.9, 142.4, 100.0, 148.5))
u.add(28, "Slots 990.34–1,130.51 ft", loc(1, 196.6, 578.4, 330.3, 584.1))
u.add(32, "Insert valve at 970 ft", u.find("Insert Valve @ 970ft"))
hole_sections = [
    u.find("24.000in to 53.00ft"), u.find("17.500in to 1000.00ft"),
    u.find("15.000in to 1230.00ft"),
]
u.add(33, "Hole sections 24.000, 17.500, and 15.000 in", *hole_sections)
u.add(34, "Hole sections to 53.00, 1,000.00, and 1,230.00 ft MD", *hole_sections)
u.add(38, "Primary cement stage for 13.375-in casing", u.find("Primary"))
u.add(39, "Primary cement top 13 ft MD", loc(1, 112.7, 199.1, 119.3, 204.8))
u.add(40, "Primary cement bottom 1,000 ft MD", u.find("1,000", occurrence=1))
u.add(43, "Tulare", u.find("Tulare"))
u.add(44, "Tulare top 501.52 ft MD", u.find("501.52"))
u.add(47, "Tulare marker", u.find("Tulare"))
u.add(48, "Tulare marker top 501.52 ft MD", u.find("501.52"))
u.add(81, "Primary cement 9/10/2012", u.find("9/10/2012"))
u.add(82, "473 sacks", u.find("473 sks"))
u.add(83, "14 ppg", u.find("14 ppg"))
u.add(84, "2.03 cf/sk", u.find("2.03 cf/sk"))
u.add(85, "A-5 Blend TYPE C", u.find("TYPE C"))
u.add(86, "35% silica flour and 4% CaCl2", u.find("35% Silica Flour"), u.find("4% CaCl2"))
for point in (87, 88, 89):
    u.add(point, "Orientation: Vertical", u.find("Vertical"))
u.single_borehole("Wellbore 00", loc(1, 80.5, 41.9, 89.1, 49.3))

u.uncertain([2, 3], "WWD10-27 is the entire stated well number; neither the diagram "
            "nor screening supplies a separate lease name.")
u.uncertain([10, 11, 12, 13, 14, 16], "The table has four casing rows, including two "
            "9.625-in sections with separate shoes. The second is treated as a lower liner "
            "with top 944 ft. Sch20 is not an explicit grade, and connection fields are "
            "blank, so repeated-string grade and connection are MISSING. Confirm the "
            "36.00-ppf entries apply to both 9.625-in rows.")
u.uncertain([17, 18, 28], "The labelled SLOTS interval is treated as another "
            "flow/integrity feature, not as explicitly named perforations.")
u.uncertain([32], "Insert Valve is treated as other in-well equipment; it is not "
            "automatically classified as a subsurface safety valve.")
u.uncertain([43, 44, 47, 48], "Tulare appears under MARKER DETAILS; the draft counts "
            "it as both a formation and a marker, and its displayed MD as both depths.")
u.uncertain([81, 82, 83, 84, 85, 86], "One primary cement stage is shown. Its remarks "
            "supply the quantity and slurry properties; 35 bbls of returns is not "
            "treated as slurry volume.")
u.uncertain([87, 88, 89], "The orientation is explicitly Vertical. Checklist v4.2 treats "
            "an explicit vertical-hole statement as answering all three path points, "
            "even without individual survey stations or azimuth values.")

u.add_excess("Well type", [
    ("well type", "Injector", u.find("Injector"), "Well type is not scored."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "1,209.73 ft", u.find("1,209.73ft"), "Plug-back depth is not a cement plug."),
])
u.add_excess("Casing schedule", [
    ("20-in casing", "Sch20", u.find("Sch20"), "Schedule is not an explicit grade."),
])
u.add_excess("Intermediate casing-joint bottoms", [
    (name, value, loc(1, x0, y, x1, y + 5.8),
     "A joint endpoint is not the full-string shoe.")
    for name, value, x0, y, x1 in (
        ("9.625-in upper", "942.33 ft", 278.8, 309.7, 299.1),
        ("13.375-in first", "969.50 ft", 281.0, 330.1, 301.2),
        ("13.375-in second", "999.20 ft", 284.2, 520.3, 304.4),
        ("9.625-in lower", "990.34 ft", 281.8, 535.7, 302.0),
        ("9.625-in bottom", "1,209.76 ft", 286.4, 606.1, 311.3),
    )
])
u.add_excess("Slot specifications", [
    ("slots", "0.050, 2.000 in, 72, 6.000", loc(1, 218.0, 578.4, 280.0, 584.1),
     "Slot dimensions are not separately scored."),
])
u.add_excess("Cement returns", [
    ("returns", "35 bbls", u.find("35 bbls"), "Return volume is not slurry volume."),
])
u.uncertain([28, 38], "Confirm the new excess categories well type, casing schedule, "
            "slot specifications, and cement returns.")
u.add_provenance("Preparer initials", "xyz", u.find("xyz"))

if __name__ == "__main__":
    u.build()
