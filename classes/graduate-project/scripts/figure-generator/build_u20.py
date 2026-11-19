"""Reviewed source observations for U20; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U20", "Not stated")
u.page_panel(1, (28, 25, 568, 815))
u.add(2, "32", u.find("32", occurrence=1))
u.add(3, "6-10UWR", u.find("6-10UWR", occurrence=1))
u.add(4, "0403041412", u.find("0403041412", occurrence=0))
u.add(5, "4/3/2011", u.find("4/3/2011"))
u.add(6, "Ground elevation 400.90 ft MSL", u.find("400.90"))
u.add(7, "Kelly bushing elevation 412.90 ft MSL", u.find("412.90"))
casings = [loc(1, 359, 151, 538, 160), loc(1, 359, 192, 538, 202),
           loc(1, 359, 728, 538, 740)]
u.add(10, "Casing sizes 13.375, 8.625, and 5.500 in", *casings)
u.add(11, "All three casings K-55", *casings)
u.add(13, "Casing weights 54.40, 32.00, and 17.00 lb/ft", *casings)
u.add(14, "Casing bottoms/shoes 92, 347, and 2,187 ft MD",
      casings[0], loc(1, 359, 216, 481, 225), loc(1, 359, 755, 500, 764))
perfs = [
    loc(1, 431, 429, 474, 439), loc(1, 188, 454, 231, 464),
    loc(1, 431, 487, 474, 496), loc(1, 190, 494, 231, 504),
    loc(1, 190, 553, 231, 563), loc(1, 190, 649, 231, 659),
    loc(1, 190, 697, 231, 707),
]
perf_statuses = [
    loc(1, 416, 429, 431, 439), loc(1, 166, 454, 190, 464),
    loc(1, 416, 487, 431, 496), loc(1, 172, 494, 189, 504),
    loc(1, 172, 553, 189, 563), loc(1, 172, 649, 189, 659),
    loc(1, 172, 697, 189, 707),
]
u.add(17, "Perforation tops 1,012; 1,030; 1,171; 1,205; 1,405; 1,705; "
      "1,855 ft MD, including tubing perforations", *perfs)
u.add(18, "Perforated intervals 1,012–1,015; 1,030–1,155; 1,171–1,174; "
      "1,205–1,290; 1,405–1,485; 1,705–1,805; 1,855–1,955 ft MD", *perfs)
u.add(28, "Restricted ID at 1,520 ft", loc(1, 359, 565, 465, 575))
u.add(30, "Packer at 1,653 ft", loc(1, 359, 609, 430, 617))
u.add(32, "Tubing hanger, tubing, crossovers, steam-cup mandrels, seal assembly "
      "and packer mandrel",
      loc(1, 359, 115, 538, 142), loc(1, 359, 391, 538, 432),
      loc(1, 359, 462, 538, 488), loc(1, 359, 615, 538, 625))
holes = [loc(1, 359, 142, 510, 151), loc(1, 359, 225, 510, 235),
         loc(1, 359, 764, 510, 775)]
u.add(33, "Hole diameters 24.0000, 11.0000, and 7.8750 in", *holes)
u.add(34, "Hole sections 12–92, 92–360, and 360–2,200 ft MD", *holes)
plug = loc(1, 145, 764, 245, 774)
u.add(35, "Plug - Cement", plug)
u.add(36, "Cement plug top 2,141 ft MD", plug)
u.add(37, "Cement plug bottom 2,187 ft MD", plug)
fills = [loc(1, 70, 135, 232, 150), loc(1, 62, 207, 240, 225),
         loc(1, 70, 741, 239, 765)]
u.add(38, "Cement behind casing at 12–92, 12–347, and 12–2,187 ft MD", *fills)
u.add(39, "Cement-fill tops 12 ft MD", *fills)
u.add(40, "Cement-fill bottoms 92, 347, and 2,187 ft MD", *fills)
formation_names = [loc(1, 359, 169, 529, 180), loc(1, 359, 381, 538, 391),
                   loc(1, 359, 441, 537, 451)]
formation_depths = [loc(1, 404, 169, 419, 180), loc(1, 478, 381, 492, 391),
                    loc(1, 449, 439, 469, 448)]
u.add(43, "Tulare, Etchegoin-Diatomite, and Reef Ridge", *formation_names)
u.add(44, "Formation tops 210, 993, and 1,110 ft MD", *formation_depths)
marker = loc(1, 359, 699, 535, 709)
u.add(47, "Tulare top, C-marker, D-marker, and L Marker", *formation_names, marker)
u.add(48, "Marker tops 210, 993, 1,110, and 1,976 ft MD", *formation_depths, marker)
u.add(81, "Cement behind casing at 12–92, 12–347, 12–2,187 ft; Plug - Cement",
      *fills, plug)
u.add(88, "Well Profile: Directional", u.find("Directional"))
u.single_borehole("One borehole shown", loc(1, 240, 114, 356, 775))

u.uncertain([1, 2, 3], "No operator is stated. The diagram explicitly labels lease 32 and "
            "CalGEM well number 6-10UWR, while the displayed well name is 32G 6-10UWRL; "
            "confirm the distinction.")
u.uncertain([10, 11, 13, 14], "Three casing strings are distinguished from tubing. "
            "The 13.375-in casing bottom is treated as a shoe; guide shoes are explicitly "
            "labelled for the other two. Confirm the manual raster transcription.")
u.uncertain([17, 18], "The five casing perforations and two explicitly labelled tubing "
            "perforations are all included as repeated instances; confirm whether tubing "
            "perforations belong in the same point.")
u.uncertain([28, 30, 31, 32], "Restricted ID is counted as another flow/integrity feature. "
            "A packer is explicit; steam-cup and packer mandrels are treated as other "
            "equipment, not automatically as gas-lift mandrels.")
u.uncertain([35, 36, 37, 38, 39, 40, 81, 82, 83, 84, 85, 86], "Three cement-behind-casing "
            "entries and a cement plug are shown. It is not explicit whether the 2,141–2,187 "
            "ft plug is the same job as the production-casing cement. Each entry is treated "
            "as identified by its displayed description; slurry points are MISSING because "
            "no slurry details are explicitly linked to the plug. The first fill explicitly "
            "says Unknown Mix/Volume.")
u.uncertain([43, 44, 47, 48], "The named Tulare, Etchegoin-Diatomite and Reef Ridge tops "
            "are treated as both formation tops and markers; L Marker is a marker only. "
            "All four depths are expressly estimated.")
u.uncertain([45, 46, 49, 50], "Producing Interval (Completion) 1,030–1,955 ft is not "
            "explicitly identified as a named zone or an injection zone.")
u.uncertain([87, 88, 89], "Directional states inclination only; no MD survey or azimuth "
            "is shown.")
u.uncertain([90], "Only one borehole is drawn; there is no explicit original-hole label.")
u.uncertain([10, 17, 30, 33, 38], "The schematic labels are rasterized and were "
            "transcribed and positioned manually; confirm the readings.")

u.add_excess("Well location", [
    ("field", "Lost Hills", u.find("Lost Hills"), "Location is not scored."),
    ("county", "Kern (2)", u.find("Kern (2)"), "Location is not scored."),
    ("state", "California", u.find("California"), "Location is not scored."),
    ("section", "32", u.find("32", occurrence=2), "PLSS location is not scored."),
    ("township", "26S", u.find("26S"), "PLSS location is not scored."),
    ("range", "21E", u.find("21E"), "PLSS location is not scored."),
    ("meridian", "MD", u.find("MD"), "PLSS location is not scored."),
])
u.add_excess("API12", [
    ("API12", "040304141200", u.find("040304141200"), "The 12-digit API is not the API10 point."),
])
u.add_excess("Datum correction factor", [
    ("correction factor", "12.00 ft", u.find("12.00"), "Datum height is not a scored point."),
])
u.add_excess("Completion date", [
    ("completion date", "5/16/2011", u.find("5/16/2011"), "Completion date is not scored."),
])
u.add_excess("Casing IDs and drift", [
    ("13.375-in", "12.615-in ID; 12.459-in drift", loc(1, 427, 151, 492, 160),
     "Casing ID and drift are not separately scored."),
    ("8.625-in", "7.921-in ID; 7.796-in drift", loc(1, 427, 192, 490, 202),
     "Casing ID and drift are not separately scored."),
    ("5.500-in", "4.892-in ID; 4.767-in drift", loc(1, 427, 728, 490, 740),
     "Casing ID and drift are not separately scored."),
])
u.add_excess("Tubing specifications", [
    ("upper tubing", "2.375-in OD; 4.70 lb/ft; 1.995-in ID; 1.901-in drift",
     loc(1, 359, 132, 538, 142), "Tubing dimensions are not separately scored."),
    ("middle tubing", "3.500-in OD; 10.20 lb/ft; 2.992-in ID; 2.797-in drift",
     loc(1, 359, 406, 538, 416), "Tubing dimensions are not separately scored."),
    ("lower tubing", "2.375-in OD; 4.70 lb/ft; 1.995-in ID; 1.901-in drift",
     loc(1, 359, 594, 538, 606), "Tubing dimensions are not separately scored."),
])
u.add_excess("Intermediate casing-component depths", [
    ("float collar", "304 ft", loc(1, 359, 202, 493, 211), "Collar depth is not a shoe."),
    ("upper component", "346 ft", loc(1, 359, 210, 538, 220),
     "Intermediate component bottom is not a shoe."),
    ("lower float collar", "2,141 ft", loc(1, 359, 740, 505, 750),
     "Collar depth is not a shoe."),
    ("lower component", "2,186 ft", loc(1, 359, 748, 538, 757),
     "Intermediate component bottom is not a shoe."),
])
u.add_excess("Perforation status", [
    (name, status, location, "Perforation status is not a scored point.")
    for name, status, location in zip(
        ("tubing 1", "casing 1", "tubing 2", "casing 2", "casing 3", "casing 4", "casing 5"),
        ("Open", "Isolated", "Open", "Open", "Open", "Open", "Open"), perf_statuses)
])
u.add_excess("Cement returns", [
    ("upper fill", "Unknown", loc(1, 202, 133, 232, 141),
     "Return volume is not slurry volume."),
    ("middle fill", "10 bbl", loc(1, 203, 211, 231, 220),
     "Return volume is not slurry volume."),
    ("lower fill", "65 bbl", loc(1, 115, 748, 165, 757),
     "Return volume is not slurry volume."),
])
u.add_excess("Producing interval", [
    ("completion", "1,030–1,955 ft", loc(1, 106, 687, 242, 697),
     "A producing interval is not explicitly an injection zone."),
])
u.uncertain([28, 38, 45], "Confirm the new excess categories tubing specifications, "
            "cement returns, and producing interval.")

if __name__ == "__main__":
    u.build()
