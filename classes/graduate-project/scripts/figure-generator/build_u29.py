"""Reviewed source observations for U29; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U29", "Not stated")
u.page_panel(1, (25, 27, 570, 740))
u.badge_size = (9, 6)
u.row_aligned_badges = True
u.add(2, "Lease Name: N/A", u.find("N/A"))
u.add(3, "10-15UW", u.find("10-15UW", occurrence=1))
u.add(4, "0403023871", u.find("0403023871", occurrence=0))
u.add(5, "4/23/2004", u.find("4/23/2004"))
u.add(6, "Ground elevation 375.0000 ft MSL", u.find("375.0000"))
u.add(7, "Kelly Bushing elevation 387.0000 ft MSL", u.find("387.0000"))
u.add(8, "No Base of Fresh Water", loc(1, 350, 127, 405, 136))
casings = [loc(1, 350, 150, 500, 158), loc(1, 350, 241, 510, 250),
           loc(1, 350, 648, 510, 656), loc(1, 350, 656, 510, 664)]
u.add(10, "Casing sizes 15.000, 10.750, and 7.000 in", *casings)
u.add(11, "15-in conductor: Unknown Grade; 10.75-in and 7-in casing: J-55",
      *casings)
u.add(13, "15-in conductor: Unknown Weight; 10.75-in casing: 40.50 lb/ft; "
      "7-in casing: 23.00 lb/ft", *casings)
u.add(14, "15-in conductor bottom 50; 10.75-in shoe 650; 7-in guide shoe "
      "2,496 ft MD", casings[0], loc(1, 140, 265, 235, 274),
      loc(1, 350, 675, 510, 686))
perfs = [loc(1, 150, 424, 235, 433), loc(1, 350, 451, 480, 460),
         loc(1, 350, 482, 480, 491), loc(1, 350, 499, 480, 508),
         loc(1, 350, 551, 480, 560), loc(1, 160, 595, 235, 604)]
u.add(17, "Perforation tops 1,365; 1,389; 1,565; 1,599; 1,799; 1,989 ft MD, "
      "including tubing perforations", *perfs)
u.add(18, "Perforation intervals 1,365–1,368; 1,389–1,539; 1,565–1,568; "
      "1,599–1,739; 1,799–1,929; 1,989–2,119 ft MD", *perfs)
u.add(28, "Restricted ID at 1,421 ft", loc(1, 185, 444, 235, 452))
u.add(30, "ARROWSET 1XS packer, 1,768–1,771 ft MD",
      loc(1, 350, 518, 495, 527), loc(1, 350, 526, 495, 535))
u.add(32, "Tubing hanger, crossover, tubing segments, bushings, two perforated "
      "tubing subs, cup and seal assemblies, wireline re-entry guide, two float "
      "collars, and float/guide shoe",
      loc(1, 130, 120, 235, 127), loc(1, 350, 120, 405, 127),
      loc(1, 350, 134, 510, 142), loc(1, 350, 249, 510, 258),
      loc(1, 100, 413, 235, 444), loc(1, 350, 410, 500, 447),
      loc(1, 90, 458, 235, 493), loc(1, 350, 460, 500, 482),
      loc(1, 350, 507, 500, 516), loc(1, 90, 516, 235, 527),
      loc(1, 90, 664, 235, 673), loc(1, 350, 675, 510, 686))
holes = [loc(1, 350, 142, 510, 150), loc(1, 350, 258, 495, 266),
         loc(1, 150, 677, 235, 686)]
u.add(33, "Conductor hole size not reported; other hole diameters 14.7500 "
      "and 9.8750 in", *holes)
u.add(34, "Hole sections 12–50, 50–650, and 650–2,502 ft MD", *holes)
plug = loc(1, 160, 669, 235, 677)
u.add(35, "Plug - Cement", plug)
u.add(36, "Cement plug top 2,480 ft MD", plug)
u.add(37, "Cement plug bottom 2,496 ft MD", plug)
fills = [loc(1, 100, 127, 235, 139), loc(1, 350, 265, 535, 277),
         loc(1, 350, 664, 535, 675)]
u.add(38, "Cement behind the 15-in, 10.75-in, and 7-in casing", *fills)
u.add(39, "Cement-fill tops 12 ft MD", *fills)
u.add(40, "Cement-fill bottoms 50, 650, and 2,496 ft MD", *fills)
formations = [loc(1, 120, 246, 235, 253), loc(1, 350, 354, 500, 363),
              loc(1, 350, 385, 500, 394)]
marker = loc(1, 350, 593, 480, 602)
u.add(43, "Etchegoin (base of Tulare), Etchegoin-Diatomite, and Reef Ridge",
      *formations)
u.add(44, "Formation tops 583, 1,068, and 1,205 ft MD", *formations)
u.add(47, "Etchegoin/base of Tulare, C-marker, D-marker, and L Marker",
      *formations, marker)
u.add(48, "Marker tops 583, 1,068, 1,205, and 2,119 ft MD", *formations, marker)
u.add(81, "Three cement-behind-casing entries and one Plug - Cement", *fills, plug)
u.add(88, "Well Profile: Directional", u.find("Directional"))
u.single_borehole("One borehole shown", loc(1, 240, 114, 356, 687))

u.uncertain([1, 2, 3], "No operator is stated. Lease Name explicitly says N/A, "
            "which is an answer under the presence rule. The CalGEM well number "
            "is 10-15UW; the well-name field also contains 32G and a trailing L.")
u.uncertain([8, 53], "No Base of Fresh Water is treated as an explicit MD answer, "
            "not a TVD value. Confirm whether the unqualified statement should "
            "also answer the TVD point.")
u.uncertain([10, 11, 12, 13, 14], "The conductor explicitly says Unknown "
            "Grade/Thread/Weight, so its grade and weight are answers. The other "
            "casing connections are not stated, leaving connection MISSING. "
            "The conductor bottom and the two labelled shoes are used for point 14.")
u.uncertain([17, 18], "The four casing perforations and two explicitly labelled "
            "tubing perforations are all included; confirm whether tubing "
            "perforations belong in the same point.")
u.uncertain([28, 30, 32], "Restricted ID is counted as another flow/integrity "
            "feature. The two Arrowset lines describe one packer; the listed "
            "tubing, subs, collars and shoe are treated as other equipment.")
u.uncertain([33, 34], "The conductor hole size is explicitly 'not reported', "
            "treated as an answer rather than a blank. All three printed hole "
            "section MD ranges are retained.")
u.uncertain([35, 38, 39, 40, 81, 82, 83, 84, 85, 86], "Three cement fills and "
            "one cement plug are recorded as separately identified entries. "
            "Unknown volume/mix is an explicit volume answer for the conductor; "
            "the two other fills list slurry quantities. No separate slurry "
            "details are linked to the plug, which may share the production "
            "cement job. The repeated-job slurry points remain MISSING.")
u.uncertain([43, 44, 47, 48], "Named estimated formation tops are also treated "
            "as markers; the L Marker is not inferred to be a formation.")
u.uncertain([45, 46, 49, 50], "Producing Interval (Completion) 1,389–2,119 ft "
            "is not explicitly named as a zone or an injection zone.")
u.uncertain([87, 88, 89], "Directional states inclination only; no MD survey or "
            "azimuth is shown.")
u.uncertain([90], "Only one borehole is drawn; no original-hole label is visible.")
u.uncertain([8, 10, 17, 30, 33, 38, 43], "The schematic labels are rasterized and "
            "were transcribed and positioned manually; confirm the readings.")

u.add_excess("Well location", [
    ("field", "LOST HILLS", u.find("LOST HILLS"), "Location is not scored."),
    ("county", "Kern (2)", u.find("Kern (2)"), "Location is not scored."),
    ("state", "California", u.find("California"), "Location is not scored."),
    ("section", "32", u.find("32", occurrence=1), "PLSS location is not scored."),
    ("township", "26S", u.find("26S"), "PLSS location is not scored."),
    ("range", "21E", u.find("21E"), "PLSS location is not scored."),
    ("meridian", "MD", u.find("MD"), "PLSS location is not scored."),
])
u.add_excess("API12", [
    ("API12", "040302387100", u.find("040302387100"), "API12 is not the API10 point."),
])
u.add_excess("Datum correction factor", [
    ("correction factor", "12.0000 ft", u.find("12.0000"), "Datum height is not scored."),
])
u.add_excess("Completion date", [
    ("completion date", "5/5/2004", u.find("5/5/2004"), "Completion date is not scored."),
])
u.add_excess("Casing IDs and drift", [
    ("10.75-in", "10.050-in ID; 9.894-in drift", loc(1, 420, 241, 485, 250),
     "Casing ID and drift are not separately scored."),
    ("7-in", "6.388-in ID; 6.241-in drift", loc(1, 420, 648, 485, 656),
     "Casing ID and drift are not separately scored."),
])
u.add_excess("Tubing specifications", [
    ("upper tubing", "2.375-in OD; 4.70 lb/ft; 13–34 ft",
     loc(1, 350, 134, 510, 142), "Tubing dimensions are not separately scored."),
    ("upper run", "2.375-in OD; 4.70 lb/ft; 34–1,365 ft",
     loc(1, 100, 413, 235, 425), "Tubing dimensions are not separately scored."),
    ("upper pup", "2.375-in OD; 4.70 lb/ft; 1,372–1,382 ft",
     loc(1, 100, 432, 235, 443), "Tubing dimensions are not separately scored."),
    ("coated tubing", "3.500-in OD; 9.30 lb/ft; 1,382–1,562 ft",
     loc(1, 90, 458, 235, 468), "Tubing dimensions are not separately scored."),
    ("pup", "2.375-in OD; 4.70 lb/ft; 1,386–1,390 ft",
     loc(1, 350, 437, 510, 446), "Tubing dimensions are not separately scored."),
    ("middle tubing", "2.375-in OD; 4.70 lb/ft; 1,390–1,570 ft",
     loc(1, 350, 468, 510, 477), "Tubing dimensions are not separately scored."),
    ("lower tubing", "2.375-in OD; 4.70 lb/ft; 1,574–1,765 ft",
     loc(1, 350, 505, 510, 517), "Tubing dimensions are not separately scored."),
])
u.add_excess("Perforation status", [
    (name, "Open", where, "Perforation status is not a scored point.")
    for name, where in zip(
        ("tubing 1", "casing 1", "tubing 2", "casing 2", "casing 3", "casing 4"),
        (loc(1, 190, 424, 210, 433), loc(1, 388, 451, 405, 460),
         loc(1, 408, 482, 425, 491), loc(1, 388, 499, 405, 508),
         loc(1, 388, 551, 405, 560), loc(1, 193, 595, 210, 604)))
])
u.add_excess("Cement returns", [
    ("conductor", "Unknown returns", loc(1, 185, 127, 230, 136),
     "Returns are not slurry volume."),
    ("10.75-in", "20 bbl returns", loc(1, 350, 270, 400, 277),
     "Returns are not a separate scored point."),
    ("7-in", "10 bbl returns", loc(1, 350, 669, 400, 676),
     "Returns are not a separate scored point."),
])
u.add_excess("Producing interval", [
    ("completion", "1,389–2,119 ft", loc(1, 350, 600, 500, 608),
     "A producing interval is not explicitly an injection zone."),
])
u.uncertain([28, 38, 45], "Confirm the new excess categories tubing specifications, "
            "cement returns, and producing interval.")

if __name__ == "__main__":
    u.build()
