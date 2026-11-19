"""Reviewed source observations for U05; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U05", "Sentinel Peak Resources California LLC")
u.page_panel(1, (20, 15, 596, 775))
u.page_panel(2, (318, 75, 596, 152), inset=True)

u.add(1, "SENTINEL PEAK RESOURCES CALIFORNIA LLC",
      u.find("SENTINEL PEAK RESOURCES CALIFORNIA LLC"))
u.add(2, "MCKITTRICK UNIT 1", u.find("MCKITTRICK UNIT 1", occurrence=1))
u.add(3, "I-36", u.find("I-36"))
u.add(4, "0403069246", u.find("0403069246"))
u.add(5, "10/9/2021", u.find("10/9/2021"))
u.add(7, "KB: 742.00 ft", u.find("742.00ft"))
u.add(8, "BFW: N/A ft", u.find("BFW: N/A"))
u.add(10, "Conductor 14 in; production 7 in",
      loc(1, 403.5, 103.7, 410.7, 110.9), loc(1, 405.4, 113.8, 409.0, 121.0))
u.add(13, "Conductor 13.5 lb/ft; production 23.0 lb/ft",
      u.find("13.5", occurrence=0), u.find("23.0"))
u.add(14, "Conductor 54 ftKB; production 1,599 ftKB",
      u.find("54", occurrence=0), u.find("1,599", occurrence=0))
u.add(17, "975, 1,173, and 1,330 ftKB at the perforation tops",
      *(u.find(value, occurrence=0) for value in ("975", "1173", "1330")))
u.add(18, "975–985, 1,173–1,183, and 1,330–1,340 ftKB",
      *(loc(1, 400.3, y, 435.6, y + 7.3) for y in (385.9, 403.9, 421.9)))
u.add(32, "Injection tubing, tubing and perforated pups, up/down cups, hanger, and WSV shoe",
      u.find("Tubing - Injection"), loc(1, 386.3, 499.0, 455.0, 743.0),
      u.find("WSV shoe", page=2))
u.add(34, "TD: 1,599.00 ftKB", loc(1, 273.7, 62.1, 324.1, 72.8))
u.add(38, "Conductor Cement; Production Cement",
      u.find("Conductor Cement"), u.find("Production Cement"))
u.add(39, "Conductor cement top 14.0 ftKB; production cement top 14.0 ftKB",
      u.find("14.0", occurrence=0), u.find("14.0", occurrence=1))
u.add(40, "Conductor cement bottom 54.0 ftKB; production cement bottom 1,599.0 ftKB",
      loc(1, 407.9, 159.1, 420.5, 166.4), u.find("1,599.0", occurrence=0))
u.add(81, "Conductor: 5/1/2021; production: 10/11/2021",
      u.find("5/1/2021"), u.find("10/11/2021"))
u.add(82, "Conductor: Unknown Mix/Volume; production: 141 bbl, 276 sacks, 792 cu ft",
      loc(1, 474.1, 159.1, 579.7, 173.8),
      loc(1, 525.8, 240.0, 571.4, 247.2), u.find("792 CUFT"))
u.add(88, "Directional", u.find("Directional"))
u.single_borehole("Original Hole", u.find("Original Hole", occurrence=0))

u.uncertain([6, 7], "KB elevation is explicit, but the 14 ft datum/height is not an explicit "
            "ground elevation; the draft does not calculate one.")
u.uncertain([8], "The source explicitly states BFW N/A, which is an answer under the "
            "presence-only rule, not NOT_APPLICABLE.")
u.uncertain([11], "Production casing grade K-55 is given but the conductor grade cell is "
            "blank, so the repeated-casing point is MISSING.")
u.uncertain([14], "The casing table labels these values as set depths, used here as shoe depths.")
u.uncertain([17], "The depth point uses the top of each perforation interval; the distinct "
            "interval point records both endpoints.")
u.uncertain([30, 32], "The source lists up/down cups and tubing but does not explicitly call "
            "them packers. They are counted as other equipment, not inferred as packers.")
u.uncertain([34], "TD 1,599 ftKB is treated as hole depth, as in the U03 draft, although "
            "the header does not separately label it 'hole depth'.")
u.uncertain([35, 36, 37], "The cement-job narrative mentions top and bottom wiper plugs, "
            "and the plug-back record says Insert; neither is explicitly a cement plug.")
u.uncertain([39], "The conductor cement table gives top 14 ftKB while its comment says "
            "'TOC Not Reported'; the displayed value is counted without judging consistency.")
u.uncertain([82], "The conductor cement explicitly says 'Unknown Mix/Volume'. Under the "
            "rule accepting any explicit entry, the draft counts this as an answer; "
            "Lester should confirm whether 'unknown' qualifies.")
u.uncertain([88], "'Directional' is treated as an explicit deviation statement, answering "
            "inclination only; no survey stations or azimuth are shown.")
u.uncertain([10], "The schematic separately shows 13.50 in and 6.37 in, but does not label "
            "their role. They are not assumed to be casing inside diameters.")

u.add_excess("Well location (field and PLSS)", [
    ("field", "Cymric", u.find("Cymric"), "Location is not among the scored points."),
    ("PLSS", "Sec. 6, T. 30S, R. 22E", u.find("Sec. 6, T. 30S, R. 22E"),
     "Location is not among the scored points."),
])
u.add_excess("Well type", [
    ("type", "Injector", loc(1, 297.8, 29.0, 328.0, 39.7),
     "Well type is not among the 90 scored points."),
])
u.add_excess("KB-ground / datum height", [
    ("datum height", "14 ft", u.find("Datum: 14ft"),
     "Height from ground or datum to KB is not an absolute ground elevation."),
])
u.add_excess("Completion date", [
    ("completion date", "10/25/2021", u.find("10/25/2021"),
     "Completion date is not a scored point."),
])
u.add_excess("Perforation dates", [
    (f"interval {interval}", "10/21/2021", u.find("10/21/2021", occurrence=index + 1),
     "Perforation date is not a scored point.")
    for index, interval in enumerate(("975–985", "1173–1183", "1330–1340"))
])
u.add_excess("Perforation shot density", [
    (f"interval {interval}", "4.0 shots/ft", loc(1, 444.7, y, 453.7, y + 7.3),
     "Shot density is not a scored point.")
    for interval, y in zip(("975–985", "1173–1183", "1330–1340"), (385.9, 403.9, 421.9))
])
u.add_excess("Perforation gun size / comment", [
    entry
    for index, (interval, y) in enumerate(zip(
        ("975–985", "1173–1183", "1330–1340"), (385.9, 403.9, 421.9)))
    for entry in [
        (f"interval {interval} gun size", "4 in", loc(1, 470.9, y, 474.5, y + 7.3),
         "Gun size is not a scored point."),
        (f"interval {interval} comment", "4 JHPF", u.find("4 JHPF", occurrence=index),
         "Gun comment is not a scored point."),
    ]
])
u.add_excess("Perforation status", [
    (f"interval {interval}", f"Open ({interval} ftKB)",
     loc(1, 534.6, y, right, y + 14.5), "Perforation status is not a scored point.")
    for interval, y, right in zip(("975–985", "1173–1183", "1330–1340"),
                                   (385.9, 403.9, 421.9), (590, 590, 590))
])
u.add_excess("Plug-back depth / tag details", [
    ("plug-back date", "10/21/2021", u.find("10/21/2021", occurrence=0),
     "Plug-back date is not a scored point."),
    ("plug-back depth", "1,558 ft MD", u.find("1,558", occurrence=0),
     "Plug-back depth is not a cement-plug endpoint."),
    ("tag method", "Tagged", u.find("Tagged"), "Tagging method is not a scored point."),
    ("plug-back type", "Insert", u.find("Insert"), "The type is not identified as a cement plug."),
])
u.add_excess("Tubing run date", [
    ("tubing run", "10/22/2021", u.find("10/22/2021"),
     "Equipment run date is not a scored point."),
])
u.add_excess("Cement-top measurement methods", [
    ("conductor method", "Unknown Volumes", loc(1, 437.3, 159.1, 464.1, 173.8),
     "Top-measurement method is not a scored point."),
    ("production method", "Visual", u.find("Visual"), "Top-measurement method is not a scored point."),
])
u.add_excess("Cementing operational details", [
    (item, value, u.find(phrase), "The operation's fluid, pressure, or returns is not a scored point.")
    for item, value, phrase in [
        ("fresh-water preflush", "2 BBLS", "2 BBLS"),
        ("SAP water", "28 BBLS", "28 BBLS"),
        ("displacement water", "58 BBLS", "58 BBLS"),
        ("test pressure", "2500 PSI", "2500 PSI"),
        ("displacement pressure", "482 PSI", "482 PSI"),
        ("bump pressure", "940 PSI", "940 PSI"),
        ("cement returns", "40 bbls", "40 bbls"),
    ]
])
u.uncertain([32, 38], "Confirm the new excess categories well type, tag details, tubing run "
            "date, cement-top methods, and cementing operational details.")
u.add_provenance("Drawing timestamp", "12/28/2021 10:39:54 AM",
                 u.find("12/28/2021 10:39:54 AM"))

if __name__ == "__main__":
    u.build()
