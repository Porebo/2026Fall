"""Reviewed source observations for U22; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U22", "Berry Corporation")
u.page_panel(1, (55, 65, 521, 606))
u.add(1, "Berry Corporation", loc(1, 115, 98, 169, 108))
u.add(2, "FAIRFIELD", loc(1, 60, 98, 102, 108))
u.add(3, "R", loc(1, 102, 98, 110, 108))
u.add(4, "0403055314", loc(1, 170, 98, 219, 108))
u.add(5, "7/18/2014", loc(1, 230, 115, 267, 124))
u.add(6, "Ground elevation 1,356.14 ft", loc(1, 60, 115, 102, 124))
u.add(7, "KB datum elevation 1,366.14 ft", loc(1, 115, 115, 160, 124))
conductor = loc(1, 66, 188, 155, 210)
production = loc(1, 66, 230, 155, 251)
shoe = loc(1, 66, 536, 155, 554)
u.add(10, "Conductor 10.750; production 3.500 in", conductor, production)
u.add(11, "Conductor H-40; production J-55", conductor, production)
u.add(13, "Conductor 32.75; production 9.30 lb/ft", conductor, production)
u.add(14, "Conductor 90.0; production 1,825.0 ft MD", conductor, shoe)
perf = loc(1, 250, 377, 335, 391)
u.add(17, "Perforation depths 1,625.0 and 1,665.0 ft MD", perf)
u.add(18, "Perforation interval 1,625.0–1,665.0 ft MD", perf)
u.add(32, "Latch-in baffle; float collar; shoe track",
      loc(1, 66, 463, 155, 483), loc(1, 66, 514, 155, 534), shoe)
holes = [loc(1, 66, 210, 155, 226), loc(1, 66, 250, 155, 266)]
u.add(33, "Openhole sections 24.000 and 7.875 in", *holes)
u.add(34, "Openhole sections 10.0–90.0 and 90.0–1,830.0 ft MD", *holes)
plug = loc(1, 250, 391, 335, 408)
u.add(35, "Production Casing Cement (plug)", plug)
u.add(36, "Production cement plug top 1,786.0 ft MD", plug)
u.add(37, "Production cement plug bottom 1,830.0 ft MD", plug)
fills = [loc(1, 250, 185, 335, 200), loc(1, 250, 200, 335, 216)]
u.add(38, "Conductor Cement; Production Casing Cement", *fills)
u.add(39, "Conductor and production fill tops 10.0 ft MD", *fills)
u.add(40, "Conductor fill bottom 90.0; production fill bottom 1,830.0 ft MD", *fills)
zone_y = (248, 272, 296, 320, 438)
u.add(45, "San Joaquin; MYA Sand; Etchegoin; RR Potter; RR Diatomite",
      *(loc(1, 335, y, 390, y + 9) for y in zone_y))
u.add(46, "Zone tops 914.4, 1,086.2, 1,267.3, 1,315.6, and 1,685.4 ft MD",
      *(loc(1, 390, y, 421, y + 9) for y in zone_y))
perf_tvd = [loc(1, 445, 387, 471, 395), loc(1, 445, 411, 471, 419)]
u.add(58, "Survey TVD at the perforation endpoints: 1,617.7 and 1,657.7 ft",
      *perf_tvd)
u.add(59, "Perforation interval 1,617.7–1,657.7 ft TVD at matching MD stations",
      *perf_tvd)
u.add(81, "Conductor Cement; Production Casing Cement; production cement plug",
      *fills, plug)
u.add(87, "Original-hole survey stations, 9.8–1,830.1 ft MD",
      loc(1, 421, 201, 446, 585))
u.add(88, "Original-hole survey inclinations; header says Deviated (15° to 30°)",
      loc(1, 471, 201, 496, 585), loc(1, 280, 114, 335, 132))
u.add(89, "Original-hole survey azimuths", loc(1, 496, 201, 521, 585))
u.single_borehole("Original Hole", loc(1, 327, 159, 376, 167))

u.uncertain([2, 3], "FAIRFIELD R is split into lease FAIRFIELD and well number R; "
            "confirm the split against the source rather than relying on screening.")
u.uncertain([10, 11, 13, 14], "The production string is represented by several "
            "components. The shoe-track bottom, 1,825.0 ft, is treated as its shoe; "
            "the conductor bottom is 90.0 ft.")
u.uncertain([17, 18, 58, 59], "The 1,625.0–1,665.0 ft label is interpreted as a "
            "perforation because it points to the red completion marks and gives JHPF. "
            "The survey table has corresponding MD endpoint rows with TVD 1,617.7 "
            "and 1,657.7 ft. The scanned station values are small; confirm the match.")
u.uncertain([32, 33, 34], "Latch-in baffle, float collar and shoe track are treated "
            "as other in-well equipment; both openhole sections are recorded as hole "
            "diameters and depths, not automatically as open-hole completions.")
u.uncertain([35, 36, 37, 38, 39, 40, 81], "The production cement plug is separately "
            "labelled but repeats the production-fill slurry narrative and date; it may "
            "share a cement job with the fill. The draft records the displayed fill "
            "and plug and their stated MD endpoints without deduplicating the evidence.")
u.uncertain([55, 67, 68, 69, 70, 71, 73], "The survey station MDs do not exactly "
            "match all represented shoe, hole, plug, fill, or zone depths: for example "
            "the Etchegoin zone top is 1,267.3 ft but its nearby station is 1,267.4 ft. "
            "No interpolation or rounding is used, so those TVD points remain MISSING.")
u.uncertain([82, 83, 84, 85, 86], "The production-fill and plug narratives give "
            "slurry details, but the conductor-cement entry gives only a name, interval "
            "and date. Repeated-job slurry points therefore remain MISSING.")
u.uncertain([87, 88, 89], "The header says Deviated (15° to 30°); all three path "
            "points are credited from the displayed MD/inclination/azimuth table, "
            "not from that deviation range alone.")
u.uncertain([1, 14, 17, 46, 58, 59], "The source is scanned. All text and evidence "
            "coordinates were reviewed visually; confirm the small survey numerals.")

u.add_excess("Well location", [
    ("area", "NSFL - MID NORTH", loc(1, 226, 98, 278, 111), "Location is not scored."),
    ("county", "Kern 030", loc(1, 280, 98, 318, 108), "Location is not scored."),
    ("state", "CA", loc(1, 335, 98, 350, 108), "Location is not scored."),
    ("section", "11", loc(1, 390, 98, 402, 108), "PLSS location is not scored."),
    ("township", "31S", loc(1, 410, 98, 427, 108), "PLSS location is not scored."),
    ("range", "22E", loc(1, 465, 98, 483, 108), "PLSS location is not scored."),
    ("latitude", "35.2388763400", loc(1, 110, 144, 169, 154), "Location is not scored."),
    ("longitude", "-119.5885620100", loc(1, 170, 144, 229, 154), "Location is not scored."),
    ("north distance", "194.0 ft N", loc(1, 230, 144, 315, 154), "Location is not scored."),
    ("east distance", "291.0 ft E", loc(1, 315, 144, 400, 154), "Location is not scored."),
    ("survey", "SW Corner", loc(1, 400, 144, 446, 154), "Survey reference is not scored."),
    ("datum", "NAD 83", loc(1, 60, 144, 91, 154), "Location datum is not scored."),
])
u.add_excess("Well status", [
    ("status", "Steam Injector", loc(1, 335, 115, 391, 125),
     "Well status is not a checklist point."),
])
u.add_excess("Total depth", [
    ("total depth", "1,830.0 ft", loc(1, 175, 115, 220, 125),
     "Header total depth is not a separate scored point."),
])
u.add_excess("Flag joint", [
    ("flag joint", "1,360.0–1,370.0 ft", loc(1, 66, 349, 155, 371),
     "Flag joint is not a scored point."),
])
u.add_excess("Intermediate casing-component endpoints", [
    ("upper joints", "1,360.0 ft", production, "Intermediate endpoint is not a string shoe."),
    ("flag joint", "1,370.0 ft", loc(1, 66, 349, 155, 371),
     "Intermediate endpoint is not a string shoe."),
    ("middle joints", "1,786.0 ft", loc(1, 66, 380, 155, 400),
     "Intermediate endpoint is not a string shoe."),
    ("baffle", "1,787.0 ft", loc(1, 66, 463, 155, 483),
     "Intermediate endpoint is not a string shoe."),
    ("lower joints", "1,818.0 ft", loc(1, 66, 488, 155, 508),
     "Intermediate endpoint is not a string shoe."),
    ("float collar", "1,819.0 ft", loc(1, 66, 514, 155, 534),
     "Intermediate endpoint is not a string shoe."),
])
u.add_excess("Perforation details", [
    ("shot density and size", '1 JHPF; 1/4 in', perf,
     "Shot density and hole size are not scored."),
    ("date", "9/18/2014", perf, "Perforation date is not scored."),
])
u.add_excess("Cement operation details", [
    ("production job", "wash pumps and lines; displacement and pressure test",
     loc(1, 250, 290, 335, 347), "Operational details are not scored."),
])
u.uncertain([32, 38], "Confirm the new excess categories well status and grouped "
            "cement-operation details; no inferred elevation difference is counted.")
u.add_provenance("Drawing timestamp", "10/27/2022 1:51:57 PM",
                 loc(1, 380, 159, 485, 168))
u.add_provenance("Last modified", "10/27/2022", loc(1, 465, 115, 513, 125))

if __name__ == "__main__":
    u.build()
