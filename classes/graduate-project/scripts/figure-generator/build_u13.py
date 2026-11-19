"""Reviewed source observations for U13; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U13", "Not explicitly stated (bry logo)", printed_date="2023-06-22")
u.page_panel(1, (15, 15, 600, 772))
u.add(2, "MCV (in well name MCV WD 2)", loc(1, 320.1, 48.5, 347.0, 60.3))
u.add(3, "2", loc(1, 365.3, 48.5, 373.1, 60.3))
u.add(4, "0403032462", u.find("0403032462", occurrence=0))
u.add(5, "5/29/2007", u.find("5/29/2007"))
u.add(6, "Ground elevation 792.10 ft", u.find("792.10"))
u.add(8, "BFW/USDW 1,003.0 ft MD", u.find("1,003.0", occurrence=1))
u.add(9, "BFW/USDW 1,003.0 ft MD", u.find("1,003.0", occurrence=1))
u.add(10, "Conductor 10 3/4 in; scab liner 5 1/2 in; production 7 in",
      u.find("10 3/4"), u.find("5 1/2"), loc(1, 371.4, 450.0, 375.7, 458.6))
u.add(11, "Conductor H-40; scab liner J-55; production K-55",
      u.find("H-40", occurrence=0), u.find("J-55", occurrence=0),
      u.find("K-55", occurrence=0))
u.add(13, "Conductor 40.50; scab liner 17.00; production 23.00 lb/ft",
      u.find("40.50", occurrence=1), u.find("17.00", occurrence=4),
      u.find("23.00", occurrence=3))
u.add(14, "Conductor 93.0; scab liner 1,431.0; production 1,856.0 ft MD",
      u.find("93.0", occurrence=6), u.find("1,431.0", occurrence=2),
      u.find("1,856.0", occurrence=2))
u.add(16, "Scab liner top 13.5 ft MD", loc(1, 514.7, 370.1, 529.7, 378.7))
u.add(17, "Perforation top 1,440.0 ft MD", u.find("1,440.0", occurrence=2))
u.add(18, "Perforated 1,440.0–1,605.0 ft MD",
      u.find("1,440.0", occurrence=2), u.find("1,605.0", occurrence=2))
u.add(32, "Tubing hanger, fatigue nipple, tubing, Arrow 1XS, and wireline guide",
      u.find("Tubing", occurrence=1), u.find("Fatigue Nipple"),
      u.find("Tubing", occurrence=0), u.find("Arrow 1XS"), u.find("Wireline Guide"))
u.add(33, "Openhole sections 20 and 9 7/8 in",
      loc(1, 491.8, 159.1, 500.5, 167.7), u.find("9 7/8"))
u.add(34, "Openhole sections 13.5–93.0 and 93.0–1,857.0 ft MD",
      loc(1, 532.2, 159.1, 594.0, 167.7), loc(1, 532.2, 169.9, 593.9, 178.5))
u.add(35, "Production Casing Cement (plug)", loc(1, 239.4, 575.3, 313.2, 589.4))
u.add(36, "Production cement plug top 1,816.0 ft MD",
      u.find("1,816.0-1,857.0"))
u.add(37, "Production cement plug bottom 1,857.0 ft MD",
      u.find("1,816.0-1,857.0"))
u.add(38, "Conductor, production casing, and scab liner cement",
      u.find("Conductor Cement", occurrence=1),
      u.find("Production Casing Cement", occurrence=3),
      u.find("Scab Liner Cement", occurrence=1))
u.add(39, "Cement fill tops 13.5 ft MD for conductor, production, and scab liner",
      *(loc(1, 491.6, y, 506.7, y + 8.6) for y in (529.2, 557.3, 585.4)))
u.add(40, "Cement fill bottoms: conductor 93.0; production 1,857.0; "
      "scab liner 1,431.0 ft MD",
      loc(1, 520.4, 529.2, 535.5, 537.8),
      loc(1, 520.4, 557.1, 546.3, 565.9),
      loc(1, 520.4, 585.1, 546.3, 593.9))
zone_names = [
    u.find("BFW/USDW"), u.find("Basal Etchegoin"), u.find("Chanac", occurrence=0),
    u.find("Chanac Silt"), u.find("Santa Margarita"), u.find("Round Moun. Silt"),
]
zone_depths = [
    u.find("1,003.0", occurrence=1), u.find("1,062.0", occurrence=1),
    u.find("1,189.0", occurrence=1), u.find("1,292.0", occurrence=1),
    u.find("1,425.0"), u.find("1,714.0"),
]
u.add(45, "Zones: BFW/USDW, Basal Etchegoin, Chanac, Chanac Silt, "
      "Santa Margarita, Round Moun. Silt", *zone_names)
u.add(46, "Zone tops 1,003.0; 1,062.0; 1,189.0; 1,292.0; 1,425.0; "
      "1,714.0 ft MD", *zone_depths)
u.add(81, "Conductor 5/28/2007; production 5/31/2007; scab liner 10/24/2017",
      u.find("5/28/2007", occurrence=0), u.find("5/31/2007", occurrence=1),
      u.find("10/24/2017", occurrence=0))
for point in (87, 88, 89):
    u.add(point, "Vertical", u.find("Vertical", occurrence=0))
u.single_borehole("Original Hole", u.find("Original Hole", occurrence=0))

u.uncertain([1], "The page displays a bry logo but no explicitly labelled operator name; "
            "the draft does not infer the operator from branding.")
u.uncertain([2, 3], "MCV is treated as the lease abbreviation and 2 as the well number "
            "within MCV WD 2. Screening lists McVan / WDW 2; confirm the source identity "
            "without substituting the screening values.")
u.uncertain([6, 7], "Ground elevation is explicit, but the page gives only KB–ground height, "
            "not a separately stated absolute reference elevation.")
u.uncertain([8, 9], "The BFW/USDW zone at 1,003 ft is used for both freshwater and "
            "lowermost-USDW base; confirm that combined label answers both points.")
u.uncertain([14, 16], "Casing set depths are treated as shoe depths. The table explicitly "
            "calls the 5 1/2-in string a scab liner even though its top is 13.5 ft, "
            "so that depth is counted as a liner top; confirm.")
u.uncertain([19, 33, 34], "The two entries are labelled Openhole in wellbore sections; "
            "they answer hole diameter and depths, but do not by themselves establish "
            "an open-hole completion.")
u.uncertain([30, 32], "The named Arrow 1XS is listed as other equipment; the diagram does "
            "not explicitly identify it as a packer, so the packer point is MISSING.")
u.uncertain([35, 36, 37, 38, 39, 40, 81], "The production cement is shown as both a fill "
            "and a plug, with one job date and shared slurry narrative. Its fill bottom "
            "is 1,857 ft, while the production casing set depth is 1,856 ft; the draft "
            "records the displayed values without reconciling them.")
u.uncertain([43, 44, 45, 46, 47, 48], "The names and depths appear in the Zones table. "
            "The draft scores them as zones, including BFW/USDW, but does not infer "
            "separate formation or marker classifications from the names.")
u.uncertain([82, 83, 84, 85, 86], "Slurry details are shown for production and scab-liner "
            "cement, but no corresponding conductor slurry amounts or properties are "
            "shown; all repeated-job points are MISSING. The cement-table volume values "
            "appear to describe returns rather than slurry quantities.")
u.uncertain([87, 88, 89], "The header explicitly says Vertical. Checklist v4.2 treats "
            "an explicit vertical-hole statement as answering all three path points, "
            "even without individual survey stations or azimuth values.")

u.add_excess("Well location", [
    ("field", "Poso Creek", u.find("Poso Creek"), "Field location is not scored."),
    ("section", "14", loc(1, 318.1, 130.3, 326.6, 138.9), "PLSS location is not scored."),
    ("township", "27S", loc(1, 344.0, 130.3, 357.8, 138.9), "PLSS location is not scored."),
    ("range", "27E", loc(1, 376.4, 130.3, 390.2, 138.9), "PLSS location is not scored."),
    ("meridian", "MD", loc(1, 402.4, 130.3, 414.3, 138.9), "PLSS location is not scored."),
    ("latitude", "35.5805640000", u.find("35.5805640000"), "Location is not scored."),
    ("longitude", "-119.0440880000", u.find("-119.0440880000"), "Location is not scored."),
    ("datum", "NAD 83", loc(1, 565.8, 130.3, 592.7, 138.9), "Location datum is not scored."),
])
u.add_excess("KB–ground height", [
    ("KB–ground height", "13.50 ft", u.find("13.50"), "Height is not an absolute elevation."),
])
u.add_excess("Rig-release date", [
    ("rig release", "6/1/2007", u.find("6/1/2007"), "Rig-release date is not scored."),
])
u.add_excess("Casing inside diameters", [
    (name, value, loc(1, 403.1, y, x1, y + 8.6), "Inside diameter is not scored.")
    for name, value, y, x1 in (("conductor", "10.05 in", 322.6, 422.5),
                               ("scab liner", "4.89 in", 370.1, 418.1),
                               ("production", "6.37 in", 450.0, 418.1))
])
u.add_excess("Casing run dates", [
    ("conductor", "5/28/2007", u.find("5/28/2007", occurrence=1),
     "Casing run date is not scored."),
    ("scab liner", "10/24/2017", u.find("10/24/2017", occurrence=1),
     "Casing run date is not scored."),
    ("production", "5/31/2007", u.find("5/31/2007", occurrence=2),
     "Casing run date is not scored."),
])
u.add_excess("Intermediate casing-joint bottoms", [
    (name, value, loc(1, 568.0, y, 593.9, y + 8.6),
     "A joint bottom inside a string is not a string shoe.")
    for name, value, y in (("scab casing joints", "1,322.5 ft", 388.8),
                           ("scab pup joint 1", "1,332.5 ft", 399.6),
                           ("scab pup joint 2", "1,352.5 ft", 410.4),
                           ("production casing joints", "1,816.0 ft", 468.7),
                           ("production insert", "1,817.0 ft", 479.5))
])
u.add_excess("Casing-component lengths", [
    (name, value, loc(1, 443.0, y, 473.1, y + 8.6),
     "Component length is not a scored point.")
    for name, value, y in (("scab casing joints", "1,309 ft", 388.8),
                           ("scab pup joint 1", "10 ft", 399.6),
                           ("scab pup joint 2", "20 ft", 410.4),
                           ("scab bottom joints", "78.5 ft", 421.2),
                           ("production joints", "1,802.5 ft", 468.7),
                           ("insert", "1 ft", 479.5),
                           ("shoe track", "39 ft", 490.3))
])
u.add_excess("Perforation date and shot details", [
    ("date", "6/18/2007", u.find("6/18/2007"), "Perforation date is not scored."),
    ("calculated shots", "661", u.find("661"), "Shot count is not scored."),
    ("shot density", '4 - 1/2" JHPF', loc(1, 560.0, 612.7, 584.7, 630.2),
     "Shot details are not scored."),
])
u.add_excess("Cement-return details", [
    (name, value, loc(1, 549.2, y, 593.2, y + 8.6),
     "Return information is not a cement slurry amount.")
    for name, value, y in (("conductor", "No, 0.0", 529.2),
                           ("production", "Yes, 20.0", 557.3),
                           ("scab liner", "No, 0.0", 585.4))
])
u.uncertain([2, 38], "The location header labels the latitude/longitude NAD 27 while the "
            "datum field says NAD 83. Confirm the new excess categories casing-component "
            "lengths, run dates, and cement-return details.")
u.add_provenance("Drawing timestamp", "6/22/2023 10:48:03 AM",
                 u.find("6/22/2023 10:48:03 AM"))
u.add_provenance("Report software", "www.peloton.com", u.find("www.peloton.com"))
u.add_provenance("Page number", "Page 1/1", u.find("Page 1/1"))
u.add_provenance("Print date", "6/22/2023", u.find("6/22/2023", occurrence=0))

if __name__ == "__main__":
    u.build()
