"""Reviewed source observations for U18; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U18", "Not stated")
u.page_panel(1, (18, 30, 596, 782))
u.add(2, "21Z (in well name 21Z C-19)", loc(1, 299, 116, 315, 125))
u.add(3, "C-19", loc(1, 315, 116, 335, 125))
u.add(4, "0403068616", loc(1, 378, 116, 425, 125))
u.add(5, "7/10/2021 02:00", loc(1, 388, 81, 448, 91))
u.add(7, "KB datum elevation 990.37 ft", loc(1, 299, 81, 330, 91))
u.add(10, "Conductor 14.000; production 7.000; slotted liner 5.500 in",
      loc(1, 355, 304, 377, 314), loc(1, 358, 363, 378, 373),
      loc(1, 358, 447, 378, 457))
u.add(13, "Conductor 32.70; production 23.00; liner 17.00 lb/ft",
      loc(1, 490, 304, 512, 314), loc(1, 490, 363, 512, 373),
      loc(1, 490, 447, 512, 457))
u.add(14, "Conductor 91.0; production 550.0; liner 793.0 ft MD",
      loc(1, 538, 285, 560, 295), loc(1, 538, 344, 562, 354),
      loc(1, 538, 428, 562, 438))
u.add(16, "Slotted-liner assembly top 515.0 ft MD", loc(1, 531, 447, 558, 457))
u.add(28, "Semi slots 538–548; full slots 548–791; gravel packs 538–550 and "
      "550–793 ft",
      loc(1, 299, 501, 594, 517), loc(1, 299, 522, 594, 539),
      loc(1, 299, 708, 563, 719), loc(1, 299, 726, 563, 738))
u.add(32, "Tubing hanger, fatigue nipple, tubing, liner landing nipple and pump",
      loc(1, 121, 177, 280, 190), loc(1, 121, 207, 284, 226),
      loc(1, 121, 239, 280, 252), loc(1, 120, 367, 285, 381),
      loc(1, 120, 421, 284, 439), loc(1, 120, 662, 283, 681))
hole_sizes = [loc(1, 480, 164, 494, 174), loc(1, 471, 175, 494, 185),
              loc(1, 480, 187, 494, 197)]
hole_depths = [loc(1, 532, y, 595, y + 10) for y in (164, 175, 187)]
u.add(33, "Wellbore sections 24; 9 7/8; 13 in", *hole_sizes)
u.add(34, "Wellbore sections 11–91; 91–550; 550–793 ft MD", *hole_depths)
u.add(38, "Conductor Cement; Production Casing Cement",
      loc(1, 299, 593, 375, 604), loc(1, 299, 638, 395, 649))
u.add(39, "Conductor and production cement tops 11.0 ft MD",
      loc(1, 408, 608, 430, 619), loc(1, 408, 654, 430, 665))
u.add(40, "Conductor cement bottom 91.0; production cement bottom 550.0 ft MD",
      loc(1, 470, 608, 491, 619), loc(1, 470, 654, 493, 665))
u.add(81, "Conductor Cement; Production Casing Cement",
      loc(1, 299, 593, 375, 604), loc(1, 299, 638, 395, 649))
for point in (87, 88, 89):
    u.add(point, "Vertical (0° to 15°)", loc(1, 59, 64, 164, 74))
u.single_borehole("Original Hole", loc(1, 168, 64, 230, 74))

u.uncertain([1, 2, 3], "No operator is explicitly stated. The draft treats 21Z as a lease "
            "identifier and C-19 as the well number within 21Z C-19; screening lists the "
            "lease as Unspecified. Confirm the split.")
u.uncertain([6, 7], "KB datum elevation and KB–ground height are shown, but no absolute "
            "ground elevation is stated; the draft does not calculate one.")
u.uncertain([11, 12, 13, 14, 16], "The conductor grade is blank and no casing connections "
            "are shown. Casing set depths are treated as shoes; the slotted-liner top is "
            "taken from its first SSA component at 515 ft. Confirm that interpretation.")
u.uncertain([17, 18, 28], "The slotted-liner rows say Semi Slots and Full Slots, while the "
            "perforation table is blank. The draft classifies the slots and gravel packs "
            "as other flow/integrity features, not as explicit perforations.")
u.uncertain([32, 33, 34], "The schematic shows tubing and a pump; the three Openhole "
            "wellbore sections provide diameters and MD depths but are not automatically "
            "treated as open-hole completions.")
u.uncertain([35, 36, 37], "Plug-back type says Top of shoe, not cement; no cement plug "
            "is identified.")
u.uncertain([81, 82, 83, 84, 85, 86], "Both cement jobs have names, but their slurry "
            "amounts and properties are not shown. The 8-bbl figure is explicitly "
            "cement returns and does not answer slurry volume.")
u.uncertain([87, 88, 89], "The header says Vertical (0° to 15°). Checklist v4.2 treats "
            "an explicit vertical-hole statement as answering all three path points, "
            "although no survey is shown. VS Dir 341.28° is a vertical-section direction, "
            "not itself an explicitly identified survey azimuth. Confirm the combined "
            "vertical label and 0°–15° range.")
u.uncertain([1, 10, 28, 33, 38], "The source page is scanned; evidence boxes and "
            "transcriptions were checked visually.")

u.add_excess("Well location", [
    ("PLSS", "SEC21, T30S, R22E MDBM", loc(1, 456, 116, 585, 126),
     "Location is not a scored point."),
])
u.add_excess("KB–ground height", [
    ("KB–ground", "11.00 ft", loc(1, 299, 99, 326, 109),
     "Height is not an absolute ground elevation."),
])
u.add_excess("Rig-release date", [
    ("rig release", "7/11/2021 12:00", loc(1, 492, 81, 562, 91), "Date is not scored."),
])
u.add_excess("Vertical-section direction", [
    ("VS Dir", "341.28°", loc(1, 531, 145, 558, 155),
     "Vertical-section direction is not an explicit wellbore azimuth."),
])
u.add_excess("Plug-back / tag details", [
    ("date", "7/11/2021", loc(1, 299, 218, 350, 228), "Tag date is not scored."),
    ("depth", "791.0 ft", loc(1, 369, 218, 399, 228), "Top of shoe is not a cement plug."),
    ("type", "Top of shoe", loc(1, 398, 218, 455, 228), "Tag type is not scored."),
])
u.add_excess("Casing inside diameters", [
    ("conductor", "13.500 in", loc(1, 389, 304, 413, 314), "Inside diameter is not scored."),
    ("production", "6.366 in", loc(1, 393, 363, 414, 373), "Inside diameter is not scored."),
    ("liner", "4.892 in", loc(1, 393, 447, 414, 457), "Inside diameter is not scored."),
])
u.add_excess("Casing run dates", [
    ("conductor", "4/13/2021", loc(1, 378, 285, 413, 295), "Casing run date is not scored."),
    ("production", "7/10/2021", loc(1, 378, 344, 413, 354), "Casing run date is not scored."),
    ("liner", "7/11/2021", loc(1, 378, 428, 413, 438), "Casing run date is not scored."),
])
u.add_excess("Intermediate casing-joint bottoms", [
    (name, value, loc(1, 569, y, 594, y + 10), "Component bottom is not a string shoe.")
    for name, value, y in (("production joints", "528.0 ft", 363),
                           ("production float", "528.0 ft", 375),
                           ("production joints 2", "549.0 ft", 387),
                           ("liner SSA", "516.0 ft", 447),
                           ("liner landing nipple", "518.0 ft", 459),
                           ("blank liner", "538.0 ft", 489),
                           ("semi slots", "548.0 ft", 501),
                           ("full slots", "791.0 ft", 522))
])
u.add_excess("Gravel-pack run details", [
    ("first run", "7/11/2021, 5.50 in ID", loc(1, 398, 708, 595, 719),
     "Run date and ID are not separate scored points."),
    ("second run", "7/11/2021, 5.50 in ID", loc(1, 398, 726, 595, 738),
     "Run date and ID are not separate scored points."),
])
u.add_excess("Cement returns", [
    ("production", "8.0 bbl", loc(1, 530, 654, 550, 665), "Return volume is not slurry volume."),
])
u.uncertain([28, 38], "Confirm the new excess categories vertical-section direction, "
            "plug-back details, casing and gravel-pack run details, and cement returns.")
u.add_provenance("Drawing timestamp", "9/9/2021 11:58:09 AM", loc(1, 231, 64, 355, 74))

if __name__ == "__main__":
    u.build()
