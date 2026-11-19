"""Reviewed source observations for U28; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U28", "Linn Energy")
u.page_panel(1, (15, 10, 525, 700))
u.badge_size = (9, 6)
u.row_aligned_badges = True
u.add(1, "Linn Energy (logo)", loc(1, 330, 16, 358, 37))
u.add(2, "GPM", u.find("GPM", occurrence=1))
u.add(3, "32", u.find("32"))
u.add(4, "037-13943", u.find("037-13943"))
u.add(5, "5/12/1951", u.find("5/12/1951"))
u.add(6, "Ground elevation 1,554 ft", u.find("1554"))
u.add(7, "Kelly Bushing elevation 1,562 ft", u.find("1562"))
u.add(8, "Base of fresh water 500 ft", loc(1, 284, 166, 398, 178))
u.add(9, "Base of USDW 1,034 ft", loc(1, 284, 178, 380, 190))
conductor = loc(1, 240, 264, 369, 278)
production = loc(1, 240, 279, 485, 292)
tubing = loc(1, 240, 321, 485, 337)
u.add(10, "12-in conductor and 6-5/8-in casing", conductor, production)
u.add(14, "12-in conductor bottom 12; 6-5/8-in casing bottom 1,951 ft",
      conductor, production)
slots = loc(1, 240, 381, 462, 395)
holes = loc(1, 240, 396, 476, 409)
u.add(17, "Slots 1,580–1,950 ft; four testing/water-shutoff holes at 1,565 ft",
      slots, holes)
u.add(20, "Four water-shutoff holes at 1,565 ft",
      holes, loc(1, 264, 511, 338, 523))
u.add(21, "Cement ports at 1,575 ft", loc(1, 37, 511, 119, 524))
fallen = [loc(1, 363, 511, 480, 523), loc(1, 337, 522, 480, 534)]
u.add(26, "Two cement retainers came loose and fell down the hole", *fallen)
u.add(32, "3-1/2-in tubing and two historical cement retainers",
      tubing, loc(1, 297, 500, 399, 512), loc(1, 264, 522, 339, 534))
u.add(33, "10-5/8-in hole", u.find("10-5/8” hole"))
u.add(34, "Total hole depth 1,951 ft", loc(1, 22, 101, 100, 121))
u.add(38, "Cemented 12-in conductor, 6-5/8-in casing, and 3-1/2-in tubing",
      conductor, production, tubing)
tops = [loc(1, 284, 190, 397, 202), loc(1, 284, 202, 416, 214),
        loc(1, 284, 215, 416, 227)]
u.add(43, "Shepard, Upper Kraft, and Lower Kraft", *tops)
u.add(44, "Formation tops 1,034, 1,118, and 1,579 ft", *tops)
u.add(47, "Shepard, Upper Kraft, and Lower Kraft top markers", *tops)
u.add(48, "Top markers 1,034, 1,118, and 1,579 ft", *tops)
u.add(81, "Conductor cement; production casing cement through ports; 25-sack top "
      "job; 8/22/1960 retainer, dump, and squeeze operations; 5/10/1986 tubing cement",
      conductor, production, u.find("top job"), u.find("8/22/60"), u.find("5/10/86"))
u.single_borehole("One borehole shown", loc(1, 148, 129, 220, 631))

u.uncertain([1, 4], "Linn Energy appears as a logo, not an operator-labelled field. "
            "The diagram prints API 037-13943; the state prefix in the screening "
            "record is not substituted into the diagram evidence.")
u.uncertain([8, 9, 53, 54], "Freshwater and USDW base depths are printed without "
            "an explicit TVD indication; only their MD points are credited.")
u.uncertain([10, 11, 12, 13, 14], "The 12-in conductor and 6-5/8-in casing are "
            "both displayed. Their bottoms are used for shoe depth; the conductor "
            "has no stated grade, connection, or weight, and the 6-5/8-in casing "
            "has no stated connection. The 3-1/2-in component is tubing.")
u.uncertain([17, 18, 20], "The PERFORATIONS DETAIL identifies slots at 1,580–1,950 "
            "and four testing holes at 1,565 ft. The workover history identifies "
            "the latter as WSO holes. Both instances have depths, but the four "
            "holes do not have a printed interval, so point 18 is MISSING.")
u.uncertain([26, 27, 32], "Two cement retainers are described as falling down the "
            "hole; the draft counts these historical fallen tools as junk and as "
            "equipment, without assuming how far they fell. The later history says "
            "a cement retainer was drilled out. Confirm this classification.")
u.uncertain([33, 34], "One 10-5/8-in hole is labelled on the schematic and the "
            "diagram states total depth 1,951 ft. Confirm the association.")
u.uncertain([35, 36, 37], "The history says PB with 10 sacks from 1,951 to 1,895 ft "
            "but does not explicitly identify the material as cement; the later "
            "TOC at 1,938 inside tubing is not explicitly called a cement plug. "
            "The cement-plug points remain MISSING pending review.")
u.uncertain([38, 39, 40], "The conductor, casing and tubing are described as "
            "cemented. An estimated TTOC of about 811 ft is supplied for the "
            "6-5/8-in casing, but fill tops and bottoms are not explicitly given "
            "for every cemented component. Returns to surface and casing depth "
            "are not assumed to be complete fill endpoints.")
u.uncertain([43, 44, 47, 48], "The explicitly named Shepard, Upper Kraft and Lower "
            "Kraft tops are treated as both formation tops and markers.")
u.uncertain([81, 82, 83, 84, 85, 86], "The cemented conductor and production casing "
            "are treated as job-identifying descriptions; the top job is named and "
            "the workover cement operations are dated. The conductor has no stated "
            "slurry quantity. Other entries include 225 sacks through ports, a "
            "25-sack top job, repeated 1- and 3-sack retainer operations, a 30-sack "
            "Class A squeeze, and 384 cu ft of Class G with 40% silica for tubing. "
            "These partial details do not answer the slurry points for every job.")
u.uncertain([87, 88, 89], "The vertical drawing is not an explicit vertical/straight "
            "statement; no wellbore path is stated.")
u.uncertain([90], "Only one borehole is drawn; no separate original-hole label is visible.")

u.add_excess("Well location", [
    ("section", "SEC 31", u.find("SEC 31", occurrence=0), "PLSS location is not scored."),
    ("township", "T4N", u.find("T4N"), "PLSS location is not scored."),
    ("range", "R15W", u.find("R15W"), "PLSS location is not scored."),
    ("meridian", "S.B. B&M", u.find("S.B. B&M"), "PLSS location is not scored."),
    ("north offset", "2548 ft N", u.find("2548"), "Location is not scored."),
    ("east offset", "1669 ft E", u.find("1669"), "Location is not scored."),
    ("coordinate datum", "NAD 83", u.find("NAD 83"), "Location is not scored."),
    ("latitude", "34.386351", u.find("34.386351"), "Location is not scored."),
    ("longitude", "-118.495965", u.find("-118.495965"), "Location is not scored."),
])
u.add_excess("Datum height", [
    ("KB height", "8 ft", u.find("8’ KB"), "Datum height is not a scored point."),
])
u.add_excess("Well status and type", [
    ("status", "ACTIVE", u.find("ACTIVE"), "Well status is not a checklist point."),
    ("type", "Temperature observation", loc(1, 437, 66, 515, 96),
     "Well type is not a checklist point."),
])
u.add_excess("Well UID", [
    ("well UID", "14003", u.find("14003"), "The internal UID is not the API number."),
])
u.add_excess("Plug-back depth", [
    ("PBTD", "1,938 ft", u.find("1938", occurrence=0), "PBTD is not a separate point."),
    ("historical PB", "1,895–1,951 ft", loc(1, 332, 473, 435, 485),
     "PB is not explicitly identified as cement."),
])
u.add_excess("Perforation specifications", [
    ("slots", "140M/16R/2½”S/6”C", loc(1, 296, 381, 399, 395),
     "Slot details are not separate scored points."),
    ("testing holes", "Four ½-in holes", loc(1, 240, 396, 290, 409),
     "Hole count and size are not separate scored points."),
])
u.add_excess("Cement returns", [
    ("tubing cement", "Returns to surface", u.find("returns to surface", occurrence=0),
     "Returns are not a separate scored point."),
])
u.add_excess("Workover dates", [
    ("plugback", "5/26/51", u.find("5/26/51"), "Workover date is not a scored point."),
    ("injection conversion", "8/22/60", u.find("8/22/60"), "Workover date is not a scored point."),
    ("production conversion", "2/9/84", u.find("2/9/84"), "Workover date is not a scored point."),
    ("temperature observation conversion", "5/10/86", u.find("5/10/86"),
     "Workover date is not a scored point."),
])
u.add_excess("Workover materials and measurements", [
    ("sand", "Filled hole with sand to 1,865 ft", u.find("sand"),
     "Historical fill material is not a fluid between plugs."),
    ("LCM", "20 sacks LCM, tagged at 1,180 ft", loc(1, 264, 587, 382, 599),
     "LCM and its tag are not cement-plug identification."),
    ("mud", "Filled hole with mud", u.find("mud"), "No between-plugs fluid is identified."),
    ("displacement", "Lease water", u.find("lease water"), "Displacement water is not a scored point."),
    ("pressure", "1,500 psi on tubing", u.find("1500 psi"), "Test pressure is not a scored point."),
])
u.add_provenance("revision date", "10/31/2014", u.find("10/31/2014"))
u.add_provenance("initials", "DC", u.find("DC"))
u.uncertain([26, 35, 38], "Confirm the new excess categories well UID and workover "
            "materials/measurements, including the classification of the historical PB.")

if __name__ == "__main__":
    u.build()
