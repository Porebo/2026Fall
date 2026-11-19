"""Reviewed source observations for U30; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U30", "Naftex Operating Company")
u.page_panel(1, (50, 50, 560, 690))
u.badge_size = (9, 6)
u.row_aligned_badges = True
u.add(1, "Naftex Operating Company", u.find("NAFTEX OPERATING COMPANY"))
u.add(2, "Racetrack", u.find("RACETRACK"))
u.add(3, "336", u.find("336"))
u.add(4, "0403064261", u.find("0403064261"))
u.add(5, "8/14/2018", u.find("8/14/18"))
u.add(7, "Kelly Bushing elevation 734 ft", u.find("734"))
conductor = loc(1, 372, 216, 453, 225)
production = loc(1, 325, 293, 477, 302)
u.add(10, "12.75-in conductor and 7-in production casing", conductor, production)
u.add(14, "12.75-in conductor bottom 53; 7-in casing shoe 1,141 ft MD",
      conductor, loc(1, 330, 659, 390, 679))
perf = loc(1, 332, 504, 361, 513)
u.add(17, "Perforation depths 741 and 751 ft MD", perf)
u.add(18, "Perforation interval 741–751 ft MD", perf)
u.add(26, "Fish: none", u.find("none"))
u.add(30, "Thermal Packer at 680 ft", loc(1, 60, 469, 165, 479))
u.add(32, "Float shoe", u.find("float shoe"))
holes = [loc(1, 372, 194, 416, 203), loc(1, 372, 260, 475, 269)]
u.add(33, "Hole diameters 24 and 9-7/8 in", *holes)
u.add(34, "24-in hole to 53; 9-7/8-in hole 53–1,143 ft MD", *holes)
cement = loc(1, 325, 315, 474, 346)
u.add(38, "Production-casing cement", production, cement)
u.add(39, "Production-casing TTOC: surface", u.find("surface", occurrence=3))
tops = [u.find("1st Chanac"), u.find("2nd Chanac"), u.find("3rd Chanac"),
        u.find("Santa Margarita")]
u.add(43, "1st Chanac, 2nd Chanac, 3rd Chanac, and Santa Margarita", *tops)
u.add(47, "1st Chanac, 2nd Chanac, 3rd Chanac, and Santa Margarita tops", *tops)
u.add(81, "Production-casing cement job", production, cement)
u.add(82, "Production-casing cement volume 488 cu ft", u.find("488"))
u.single_borehole("One borehole shown", loc(1, 195, 170, 315, 684))

u.uncertain([6, 7], "Kelly Bushing elevation is 734 ft and KB height is 13 ft; "
            "ground elevation is not explicitly printed and is not calculated.")
u.uncertain([10, 11, 12, 13, 14], "Both the 12.75-in conductor and 7-in production "
            "casing are shown, but the conductor has no grade, connection or weight. "
            "The 53-ft conductor bottom and the labelled 1,141-ft production shoe "
            "are used as shoe depths.")
u.uncertain([17, 18], "The one displayed perforation interval is 741–751 ft MD.")
u.uncertain([26, 30, 32, 35, 36, 37], "Fish explicitly says none. Thermal Packer "
            "and float shoe are equipment; the Bridge Plugs and Cmt Plugs headings "
            "have no entries and are not treated as explicit none or cement plugs.")
u.uncertain([33, 34], "Both hole sizes and depths are printed. The 24-in hole "
            "is stated to 53 ft and the 9-7/8-in hole from 53 to 1,143 ft.")
u.uncertain([38, 39, 40, 81, 82], "The production-casing cement is treated as an "
            "identified cement job with 488 cu ft and TTOC at surface. The fill "
            "bottom is not explicitly stated and is not inferred from casing depth. "
            "No separate conductor cement job is identified.")
u.uncertain([43, 44, 47, 48], "The four labels under Tops are treated as formation "
            "names and top markers. Only 1st Chanac at 641 ft and Santa Margarita "
            "at 1,049 ft have printed depths; 2nd and 3rd Chanac have blank depth "
            "entries, so both repeated-depth points remain MISSING.")
u.uncertain([87, 88, 89], "The drawing is not explicitly called vertical/straight. "
            "The bottom-hole location offset does not state an inclination, path "
            "station or azimuth.")
u.uncertain([90], "Only one borehole is drawn; no original-hole label is visible.")

u.add_excess("Well location", [
    ("field", "Edison", u.find("EDISON"), "Location is not scored."),
    ("section", "Sec 27", u.find("Sec 27"), "PLSS location is not scored."),
    ("township", "T29S", u.find("T29S"), "PLSS location is not scored."),
    ("range", "R29E", u.find("R29E"), "PLSS location is not scored."),
    ("meridian", "MD B&M", u.find("MD B&M"), "PLSS location is not scored."),
    ("south offset", "532S", u.find("532S"), "Location is not scored."),
    ("east offset", "941E", u.find("941E"), "Location is not scored."),
    ("surface X", "1744538", u.find("1744538"), "Location is not scored."),
    ("surface Y", "683450", u.find("683450"), "Location is not scored."),
    ("bottom-hole north offset", "201 ft N", u.find("201", occurrence=0),
     "Location is not a path inclination."),
    ("bottom-hole east offset", "16 ft E", u.find("16"),
     "Location is not a path azimuth."),
])
u.add_excess("Well status and type", [
    ("status", "SF", u.find("SF"), "Status is not a checklist point."),
    ("type", "New Injector", u.find("New Injector"), "Well type is not a checklist point."),
])
u.add_excess("Datum height", [
    ("KB", "13 ft", u.find("13", occurrence=0), "Datum height is not a scored point."),
])
u.add_excess("Completion date", [
    ("completion date", "9/24/18", u.find("9/24/18", occurrence=1),
     "Completion date is not a scored point."),
])
u.add_excess("Casing lengths", [
    ("conductor", "40 ft", loc(1, 172, 183, 186, 192),
     "Component length is not a separate scored point."),
    ("production casing", "1,128 ft", loc(1, 169, 194, 186, 203),
     "Component length is not a separate scored point."),
])
u.add_excess("Perforation specification", [
    ("HPF detail", "1-1/2-in JHP2F", loc(1, 378, 504, 425, 513),
     "Shot specification is not a separate scored point."),
])
u.add_excess("Perforation status", [
    ("status", "Open", u.find("Open"), "Status is not a separate scored point."),
])
u.add_excess("Perforation date", [
    ("date", "9/24/2018", u.find("9/24/2018"), "Perforation date is not scored."),
])
u.add_excess("Cement returns", [
    ("returns", "24 bbl to surface", loc(1, 455, 326, 465, 335),
     "Returns are not slurry volume."),
])
u.add_provenance("drawing date", "9/24/18", u.find("9/24/18", occurrence=0))
u.uncertain([10, 17, 38], "Confirm the new excess categories casing lengths, "
            "perforation specifications, and cement returns.")

if __name__ == "__main__":
    u.build()
