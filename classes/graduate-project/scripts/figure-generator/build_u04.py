"""Reviewed source observations for U04; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U04", "Seneca Resources", printed_date="09/25/2020")
u.page_panel(1, (25, 25, 820, 1075))

u.add(1, "Seneca Resources", loc(1, 33, 33, 164, 92))
u.add(2, "BLACKWELL", u.find("BLACKWELL", occurrence=1))
u.add(3, "TI-7X", u.find("TI-7X", occurrence=1))
u.add(4, "03066895", u.find("03066895", occurrence=1))
u.add(5, "2/24/2020", u.find("2/24/2020", occurrence=1))
u.add(6, "432 ft", u.find("432"))
u.add(10, "Conductor 12 1/4 in; injection string 5 1/2 in",
      u.find("12 1/4", occurrence=1), u.find("5 1/2", occurrence=0))
u.add(11, "Conductor K-55; injection string L-80", u.find("K-55"), u.find("L-80"))
u.add(13, "Conductor 35.00 lb/ft; injection string 17.00 lb/ft",
      u.find("35.00"), u.find("17.00"))
u.add(14, "Conductor 93 ftKB; injection string 325 ftKB",
      u.find("93", occurrence=3), u.find("325", occurrence=2))

perf_top = [u.find(str(depth), occurrence=0) for depth in (176, 182, 206, 209)]
perf_ranges = [
    loc(1, 720.7, y, 811.8, y + 11.4) for y in (591.9, 651.8, 711.7, 771.6)
]
u.add(17, "176, 182, 206, and 209 ftKB", *perf_top)
u.add(18, "176–176, 182–182, 206–206, and 209–209 ftKB", *perf_ranges)
u.add(30, "Packer, 142–152 ftKB", u.find("Packer"))
u.add(32, "Tubing, pup joints, expansion joint, and bell collar",
      u.find("Tubing"), u.find("pups"), u.find("Expansion jt"), u.find("pup 4'"),
      u.find("Bell, Coller"))
u.add(33, "Conductor hole 12 1/4 in; production hole 8 1/2 in",
      u.find("12 1/4", occurrence=0), u.find("8 1/2"))
u.add(34, "Conductor section bottom 93 ftKB; production section bottom 325 ftKB",
      u.find("93", occurrence=0), u.find("325", occurrence=0))
u.add(38, "Conductor String Cement; Injection String Cement",
      u.find("Conductor String Cement"), u.find("Injection String Cement"))
u.add(39, "Conductor cement top 13 ftKB; injection cement top 13 ftKB",
      loc(1, 711.6, 433.2, 723.1, 444.6), loc(1, 625.8, 495.1, 637.3, 506.5))
u.add(40, "Conductor cement bottom 93 ftKB; injection cement bottom 325 ftKB",
      u.find("93", occurrence=4), u.find("325", occurrence=3))
u.add(43, "Tulare", u.find("Tulare", occurrence=0))
u.add(44, "Tulare final top MD 150 ftKB", u.find("150", occurrence=0))
u.add(81, "Conductor String Cement; Injection String Cement",
      u.find("Conductor String Cement"), u.find("Injection String Cement"))
u.single_borehole("Original Hole", u.find("Original Hole"))

u.uncertain([4], "The visible source API is 03066895; the screening log uses 0403066895. "
            "The point is scored from the displayed value; reconcile the mismatch.")
u.uncertain([7], "The source gives 432 ft ground elevation and a 13 ft KB-to-ground distance, "
            "but no explicit absolute KB/reference elevation. Do not infer the sum.")
u.uncertain([14], "The casing table labels these values as set depths, used here as shoe depths.")
u.uncertain([17, 18], "Each perforation has identical displayed top and bottom; both the "
            "depth and interval points are counted as present under the presence-only rule.")
u.uncertain([32], "Pup joints, expansion joint, and bell collar are counted as other in-well "
            "equipment in addition to the tubing.")
u.uncertain([38, 81], "Both cement entries have distinct string-specific descriptions. "
            "Confirm that these descriptions count as job names for point 81.")
u.uncertain([79, 80], "The phrase 'Volume Calculations' describes a top-measurement method; "
            "calculation steps or an accompanying calculation document are not shown.")
u.uncertain([82, 84, 85], "The injection cement lists 25.0 bbl/47 sacks, yield 3.02, and "
            "Type III, but the conductor cement does not give these answers; repeated-job "
            "points are MISSING. These partial answers are not classified as excess.")
u.uncertain([87, 88, 89], "'Vertical schematic (actual)' describes the drawing and is not "
            "treated as an explicit statement of the borehole trajectory.")

u.add_excess("Well location (field and PLSS)", [
    ("field", "North Lost Hills", u.find("North Lost Hills", occurrence=1),
     "Location is not among the scored points."),
    ("surface legal location", "SEC24/T26S/R20E", u.find("SEC24/T26S/R20E"),
     "Location is not among the scored points."),
])
u.add_excess("KB-ground height", [
    ("KB-ground distance", "13 ft", loc(1, 427.5, 139.7, 439.0, 151.2),
     "A reference-to-ground distance is not an absolute reference elevation."),
])
u.add_excess("Casing inside diameters", [
    ("conductor ID", "12.00 in", u.find("12.00", occurrence=0),
     "The checklist requests casing size, not inside diameter."),
    ("injection ID", "4.89 in", u.find("4.89", occurrence=0),
     "The checklist requests casing size, not inside diameter."),
])
u.add_excess("Casing string lengths", [
    ("conductor length", "80.00 ft", u.find("80.00", occurrence=0),
     "Full-string length is not a scored point."),
    ("injection string length", "312.00 ft", u.find("312.00"),
     "Full-string length is not a scored point."),
])
u.add_excess("Intermediate casing-joint bottoms", [
    ("casing joint bottom", "283 ftKB", loc(1, 388.7, 741.7, 403.1, 751.2),
     "This intermediate joint bottom is not a casing shoe, stub, or liner top."),
    ("casing joint bottom", "324 ftKB", loc(1, 393.5, 897.4, 408.0, 906.9),
     "This intermediate joint bottom is not a casing shoe, stub, or liner top."),
])
u.add_excess("Cement-top measurement methods", [
    ("conductor top method", "Returns to Surface", u.find("Returns to Surface"),
     "Measurement method is not itself a scored point."),
    ("injection top method", "Volume Calculations", u.find("Volume Calculations"),
     "The method name is not calculation steps or an attached calculation."),
])
u.add_excess("Perforation hole diameters", [
    (f"perforation at {depth} ftKB", "0.250 in", u.find("0.250", occurrence=index),
     "Perforation hole diameter is not a scored point.")
    for index, depth in enumerate((176, 182, 206, 209))
])
u.add_excess("Perforation shot totals", [
    (f"perforation at {depth} ftKB", "1 shot", loc(1, 556.5, y, 562.2, y + 11.4),
     "Shot count is not a scored point.")
    for depth, y in zip((176, 182, 206, 209), (591.9, 651.8, 711.7, 771.6))
])
u.add_excess("Perforation shot density", [
    (f"perforation at {depth} ftKB", "1.0 shots/ft", u.find("1.0", occurrence=index),
     "Shot density is not a scored point.")
    for index, depth in enumerate((176, 182, 206, 209))
])
u.uncertain([33, 38], "Confirm the new excess categories: casing string length, "
            "cement-top measurement method, perforation hole diameter, and shot total.")
u.add_provenance("Drawing timestamp", "9/25/2020 1:12:50 PM",
                 loc(1, 226.0, 154.8, 319.5, 164.3))
u.add_provenance("Software website", "www.natfuel.com/seneca", u.find("www.natfuel.com/seneca"))
u.add_provenance("Page", "1/1", u.find("Page  1/1"))
u.add_provenance("Report printed", "9/25/2020",
                 loc(1, 681.9, 1056.1, 813.8, 1067.5))

if __name__ == "__main__":
    u.build()
