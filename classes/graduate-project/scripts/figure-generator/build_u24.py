"""Reviewed source observations for U24; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U24", "Aera Energy LLC")
u.page_panel(1, (10, 10, 590, 765))
u.badge_size = (9, 6)
u.row_aligned_badges = True
u.add(1, "Aera Energy LLC", u.find("Aera Energy LLC"))
u.add(3, "2-6ZR3-19", u.find("2-6ZR3-19"))
u.add(4, "0403040671", u.find("0403040671"))
u.add(5, "8/6/2010", u.find("8/6/2010"))
u.add(6, "Ground elevation 588.69 ft", u.find("588.69"))
u.add(7, "Kelly Bushing datum 602.69 ft", u.find("602.69"))
u.add(8, "Base of fresh water MD: N/A", u.find("N/A", occurrence=1))
u.add(9, "Base of USDW MD: N/A", u.find("N/A", occurrence=0))
u.add(10, "Casing 12.5000 and 3.5000 in",
      u.find("12.5000", occurrence=1), u.find("3.5000", occurrence=4))
u.add(13, "12.5-in casing 33.38; 3.5-in casing 9.30 lb/ft",
      u.find("33.38ppf"), u.find("9.30ppf", occurrence=0))
u.add(14, "12.5-in shoe 54.0; 3.5-in shoe 1,196.0 ft MD",
      u.find("54.0", occurrence=2), u.find("1,196.0"))
perf_rows = (411.9, 435.3, 442.7, 451.6, 465.1, 481.3, 517.0,
             539.8, 553.9, 576.7, 584.2, 602.7, 610.1)
tops = ("806.000", "840.000", "840.000", "854.000", "860.000", "874.000",
        "942.000", "974.000", "982.000", "1,014.000", "1,014.000",
        "1,055.000", "1,055.000")
intervals = ("806.000–806.100", "840.000–840.100", "840.000–840.100",
             "854.000–854.100", "860.000–860.100", "874.000–874.100",
             "942.000–942.100", "974.000–974.100", "982.000–982.100",
             "1,014.000–1,014.100", "1,014.000–1,014.100",
             "1,055.000–1,055.100", "1,055.000–1,055.100")
u.add(17, "Perforation tops " + ", ".join(tops) + " ft MD",
      *(loc(1, 225, y, 255, y + 6) for y in perf_rows))
u.add(18, "Perforation intervals " + ", ".join(intervals) + " ft MD",
      *(loc(1, 225, y, 287, y + 6) for y in perf_rows))
u.add(34, "Displayed hole depths 0.00, 330.00, and 1,200.00 ft MD",
      loc(1, 528, 235, 562, 242), loc(1, 516, 354, 574, 361),
      loc(1, 514, 666, 574, 673))
u.add(38, "Primary cement stage for 3.5-in casing", u.find("Primary"))
u.add(39, "Primary cement top 14 ft MD", loc(1, 115, 194, 125, 201))
u.add(40, "Primary cement bottom 1,196 ft MD", loc(1, 147, 194, 164, 201))
u.add(47, "Markers Tulare and San Joaquin/Etchegoin",
      u.find("Tulare"), u.find("San Joaquin/Etchegoin"))
u.add(48, "Marker tops 278.16 and 1,028.14 ft MD",
      u.find("278.16"), u.find("1,028.14"))
u.add(81, "Primary cement job, 8/7/2010", u.find("Primary"), u.find("8/7/2010"))
for point in (87, 88, 89):
    u.add(point, "Orientation: Vertical", u.find("Vertical"))
u.single_borehole("Wellbore 00", loc(1, 80, 42, 89, 49))

u.uncertain([2, 3], "The diagram states well 2-6ZR3-19 but no lease name. "
            "The screening-log lease Ellis is not substituted for missing diagram evidence.")
u.uncertain([8, 9, 53, 54], "Freshwater and USDW boxes explicitly say N/A for "
            "Base MD, so MD points are MET. No TVD answer is stated.")
u.uncertain([10, 11, 12, 13, 14], "The 12.5-in casing has a size, weight and base "
            "but blank grade and connection fields. The 3.5-in assembly has J-55 "
            "and EUE 8rd. The casing-table base 1,196.0 ft is treated as the shoe, "
            "although the lower schematic component ends at 1,195.97 ft.")
u.uncertain([17, 18], "All 13 displayed perforation rows are included, including "
            "duplicate 840, 1,014 and 1,055 ft entries. They are not deduplicated.")
u.uncertain([33, 34], "Two entries show 7.88-in holes, but another displayed row "
            "says only 'hole to 0.00ft' with no diameter. Hole size remains MISSING "
            "under the repeated-section rule; all three displayed MD depths are kept. "
            "Confirm whether the blank zero-depth row should represent a section.")
u.uncertain([35, 38, 39, 40, 81], "PLUG DETAILS is empty. The dated Primary cement "
            "stage identifies one fill with top and bottom MD; it is not a cement plug.")
u.uncertain([43, 44, 45, 46, 47, 48], "Tulare and San Joaquin/Etchegoin are "
            "explicitly listed under MARKER DETAILS, so they are recorded as markers "
            "rather than inferred formation or zone entries.")
u.uncertain([87, 88, 89], "The explicit Orientation: Vertical statement answers "
            "all three path points under checklist v4.2.")

u.add_excess("Well type", [
    ("type", "Injector", u.find("Injector"), "Well type is not a checklist point."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "1,180.99 ft", u.find("1,180.99ft", occurrence=2),
     "Plug-back MD is not an identified cement plug."),
])
u.add_excess("Total depth", [
    ("TD MD", "1,200 ft", u.find("1,200ft"), "Header total depth is not a separate point."),
])
u.add_excess("Flag joint", [
    ("flag joint", "514 ft", u.find("FLAG JOINT"), "Flag joint is not a scored point."),
])
u.add_excess("Intermediate casing-component endpoints", [
    ("upper production", "513.73 ft", u.find("513.73ft"),
     "Intermediate component endpoint is not a string shoe."),
    ("middle production", "1,180.99 ft", u.find("1,180.99ft", occurrence=0),
     "Intermediate component endpoint is not a string shoe."),
])
u.add_excess("Perforation shot density", [
    (f"interval {index}", "1.000 shot/ft", loc(1, 278, y, 329, y + 6),
     "Shot density is not scored.")
    for index, y in enumerate(perf_rows, 1)
])
u.uncertain([34], "Confirm the new excess category well type; hole and cement "
            "fields are not counted as excess when they answer scored points.")
u.add_provenance("Preparer initials", "xyz", u.find("xyz"))
u.add_provenance("Drawing date", "2/13/2023", u.find("2/13/2023"))

if __name__ == "__main__":
    u.build()
