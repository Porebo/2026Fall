"""Reviewed source observations for U10; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U10", "Seneca Resources")
u.page_panel(1, (20, 20, 780, 1020))
u.add(1, "SENECA RESOURCES (logo)", loc(1, 33, 32, 158, 85))
u.add(3, "232X (in well name SUNSET 232X)", loc(1, 75.8, 109.4, 98.9, 120.2))
u.add(4, "03064787", u.find("03064787", occurrence=1))
u.add(5, "1/24/2019", u.find("1/24/2019", occurrence=1))
u.add(6, "Ground elevation 914 ft", u.find("914"))
u.add(10, "Conductor 14 in; surface 7 in; liner 5 1/2 in",
      loc(1, 570.4, 266.9, 581.3, 277.7), loc(1, 573.2, 326.3, 578.6, 337.1),
      loc(1, 564.9, 385.8, 586.9, 396.5))
u.add(11, "Conductor, surface, and liner: K-55",
      *(u.find("K-55", occurrence=i) for i in range(3)))
u.add(13, "Conductor 36.75; surface 23.00; liner 17.00 lb/ft",
      u.find("36.75"), u.find("23.00"), u.find("17.00"))
u.add(14, "Conductor 94 ft; surface 430 ft; liner 581 ft MD",
      loc(1, 643.4, 289.5, 654.3, 300.3), loc(1, 637.9, 349.0, 654.3, 359.8),
      loc(1, 637.9, 408.4, 654.3, 419.2))
u.add(16, "Liner top 393 ft MD", u.find("393", occurrence=0))
perf_ranges = [loc(1, 651.1, y, 738.1, y + 10.8) for y in (454.6, 468.7)]
u.add(17, "Semi-perf and slotted-liner tops: 405.2 and 427.2 ft MD", *perf_ranges)
u.add(18, "Semi-perf 405.2–427.2 ft; slotted liner 427.2–578.7 ft MD", *perf_ranges)
u.add(28, "Semi-perf and slotted-liner sections",
      u.find("Slotted Liner Semi Perf"), u.find("Slotted Liner;"))
u.add(32, "Fatigue nipple, tubing, steel seal adapter, guide shoe, pump barrel, "
      "and circulating shoe",
      *(u.find(s) for s in ("Fatigue Nipple;", "Tubing;", "Steel Seal Adapter;",
                            "Guide Shoe;", "Pump Barrel;", "Circulating Shoe;")))
u.add(33, "Conductor section 14 in; surface 9 7/8 in; underreamed section 13 in",
      loc(1, 598.2, 171.7, 609.1, 182.4), u.find("9 7/8"),
      loc(1, 598.2, 216.9, 609.1, 227.7))
u.add(34, "Conductor bottom 94 ft; surface and underreamed bottoms 581 ft MD",
      loc(1, 758.4, 171.7, 769.3, 182.4), loc(1, 752.9, 194.3, 769.3, 205.1),
      loc(1, 752.9, 216.9, 769.3, 227.7))
u.add(38, "Conductor String Cement; Surface String Cement",
      u.find("Conductor String Cement"), u.find("Surface String Cement"))
u.add(39, "Conductor and surface cement tops 14 ft MD",
      loc(1, 672.6, 505.5, 683.5, 516.3), loc(1, 591.6, 564.0, 602.5, 574.8))
u.add(40, "Conductor cement bottom 94 ft; surface cement bottom 430 ft MD",
      loc(1, 758.4, 505.5, 769.3, 516.3), loc(1, 645.4, 564.0, 661.9, 574.8))
u.add(55, "Conductor 94.1 ft; surface 425.7 ft; liner 571.3 ft TVD",
      u.find("94.1"), u.find("425.7"), u.find("571.3"))
u.add(57, "Liner top 389.5 ft TVD", u.find("389.5"))
u.add(58, "Semi-perf and slotted-liner tops 401.6 and 422.8 ft TVD",
      u.find("401.6"), u.find("422.8"))
u.add(59, "Semi-perf 401.6–422.8 ft; slotted liner 422.8–569.0 ft TVD",
      u.find("401.6"), u.find("422.8"), u.find("569.0"))
u.add(67, "Conductor section bottom 94.1 ft; surface and underreamed "
      "bottoms 571.3 ft TVD", u.find("94.1"), u.find("571.3"))
u.add(70, "Conductor and surface cement tops 14.1 ft TVD", u.find("14.1", occurrence=1))
u.add(71, "Conductor cement bottom 94.1 ft; surface bottom 425.7 ft TVD",
      u.find("94.1"), u.find("425.7"))
u.add(81, "Conductor String Cement; Surface String Cement",
      u.find("Conductor String Cement"), u.find("Surface String Cement"))
u.add(88, "Deviated", u.find("Deviated"))
u.single_borehole("Original Hole", u.find("Original Hole"))

u.uncertain([1, 2, 3, 4], "The operator appears in a Seneca Resources logo; the source "
            "says well name SUNSET 232X but has no separately labelled lease. It prints "
            "API 03064787 while the screening log uses 0403064787. Confirm the logo and "
            "identity interpretation without replacing the displayed source values.")
u.uncertain([6, 7], "Ground elevation is 914 ft and KB-ground distance is 14 ft, but the "
            "source does not separately state absolute KB elevation. It is not calculated.")
u.uncertain([17, 18, 28, 58, 59], "One slotted section is labelled Semi Perf; both slots "
            "rows have a Perf Rows column. The draft treats both intervals as perforation "
            "intervals and records the slotted liner as another flow/integrity feature. "
            "Confirm this classification.")
u.uncertain([19, 33, 34, 67], "Underreamed is a named wellbore section, not an explicit "
            "open-hole completion. Both surface and underreamed sections end at 581 ft MD.")
u.uncertain([55, 57, 58, 59, 67, 70, 71], "TVD values are read from the paired MD/TVD "
            "axis at the corresponding depicted features. The casing and cement tables "
            "round MD values to whole feet: 94 aligns with 94.2 on the axis, 430 with "
            "430.1, 393 with 392.7, and 14 with 14.1. Confirm these associations; no "
            "TVD is assumed merely from MD.")
u.uncertain([81, 82, 83, 84, 85, 86], "Both cement fills have distinguishing names. "
            "The surface job lists volumes, sack counts, yields, and Class C, but the "
            "conductor job has no corresponding entries, so the repeated-job points "
            "remain MISSING. A yield value alone is not calculation steps.")
u.uncertain([87, 88, 89], "Deviated is treated as an explicit deviation statement "
            "answering inclination only. Vertical schematic describes the drawing, "
            "not a separate assertion that the deviated borehole is vertical.")

u.add_excess("Well location", [
    ("field", "Midway Sunset South", u.find("Midway Sunset South", occurrence=1),
     "Field location is not a scored point."),
    ("surface legal location", "SEC20/T11N/R23W", u.find("SEC20/T11N/R23W"),
     "Location is not a scored point."),
])
u.add_excess("Well status", [
    ("status", "Producing - Rod Pump", u.find("Producing - Rod Pump"),
     "Well status is not a scored point."),
])
u.add_excess("KB-ground height", [
    ("KB-ground distance", "14 ft", loc(1, 404.1, 132.0, 415.0, 142.8),
     "Height is not an absolute reference elevation."),
])
u.add_excess("Casing inside diameter", [
    ("conductor", "13.50 in", u.find("13.50", occurrence=0), "Casing ID is not nominal OD."),
    ("surface", "6.37 in", u.find("6.37", occurrence=0), "Casing ID is not nominal OD."),
    ("liner", "4.89 in", u.find("4.89", occurrence=0), "Casing ID is not nominal OD."),
])
u.add_excess("Casing string lengths", [
    (name, value, location, "String length is not a scored point.")
    for name, value, location in [
        ("conductor", "80.00 ft", loc(1, 744.6, 289.5, 769.3, 300.3)),
        ("surface", "416.00 ft", loc(1, 739.1, 349.0, 769.3, 359.8)),
        ("liner", "188.26 ft", loc(1, 739.1, 408.4, 769.3, 419.2)),
    ]
])
u.add_excess("Intermediate casing-joint bottoms", [
    ("7 in joint", "404 ft", u.find("14-404"),
     "An intermediate joint bottom is not a complete-string shoe."),
    ("7 in joint", "429 ft", u.find("404-429"),
     "An intermediate joint bottom is not a complete-string shoe."),
])
u.add_excess("Slot specifications", [
    (f"slot row {i + 1}", "0.030 in; 2.00 in; 6.00 ft; "
     f"{rows} perforation rows", loc(1, 428.6, y, 626.2, y + 10.8),
     "Slot dimensions and row count are not separate scored points.")
    for i, (y, rows) in enumerate(((454.6, 32), (468.7, 64)))
])
u.add_excess("Cement-top method", [
    ("surface cement", "Returns to Surface", u.find("Returns to Surface"),
     "Top-measurement method is not a scored point."),
])
u.uncertain([10, 28, 38], "Confirm the new excess categories well status, casing inside "
            "diameters and string lengths, slot specifications, and cement-top method.")
u.add_provenance("Drawing timestamp", "7/17/2019 2:57:03 PM",
                 loc(1, 232.3, 146.3, 307.0, 155.3))
u.add_provenance("Report printed", "7/17/2019", u.find("7/17/2019", occurrence=0))
u.add_provenance("Software website", "www.natfuel.com/seneca", u.find("www.natfuel.com/seneca"))
u.add_provenance("Page number", "1/1", u.find("Page 1/1"))

if __name__ == "__main__":
    u.build()
