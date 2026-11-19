"""Reviewed source observations for U19; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U19", "Seneca Resources", printed_date="3/10/2022")
u.page_panel(1, (25, 25, 824, 1075))
u.page_panel(2, (402, 180, 824, 365), inset=True)
u.add(1, "Seneca Resources", loc(1, 34, 34, 165, 92))
u.add(2, "SEC 19", u.find("SEC 19"))
u.add(3, "SUNSET 251SI-7", u.find("SUNSET 251SI-7", occurrence=1))
u.add(4, "03062255", u.find("03062255", occurrence=1))
u.add(5, "1/6/2018", u.find("1/6/2018", occurrence=2))
u.add(6, "Ground elevation 1,017 ft", u.find("1,017"))
u.add(10, "Conductor 12 in; injection string 3 1/2 in",
      u.find("12", occurrence=1), u.find("3 1/2", occurrence=0))
u.add(11, "Conductor H-40; injection string N-80", u.find("H-40"), u.find("N-80"))
u.add(13, "Conductor 33.41; injection string 9.20 lb/ft",
      u.find("33.41"), u.find("9.20"))
u.add(14, "Conductor shoe 88; injection string shoe 668 ft MD",
      u.find("88", occurrence=3), u.find("668", occurrence=2))
u.add(17, "Perforation top 450 ft MD", u.find("450", occurrence=0))
u.add(18, "Perforated 450–490 ft MD", u.find("450", occurrence=0),
      u.find("490", occurrence=0))
u.add(32, "Landing joint, casing pup joints and float shoe",
      u.find("Landing Joint"), u.find("Casing Pup Joint", occurrence=0),
      u.find("Casing Pup Joint", occurrence=1), u.find("Float Shoe"))
u.add(33, "Conductor hole 12; production hole 6 3/4 in",
      u.find("12", occurrence=0), u.find("6 3/4"))
u.add(34, "Conductor section 8–88; production section 88–668 ft MD",
      loc(1, 723, 205, 822, 218), loc(1, 720, 229, 822, 242))
cement_names = [u.find("Conductor String Cement"), u.find("Steam Injector Cement")]
u.add(38, "Conductor String Cement; Steam Injector Cement", *cement_names)
u.add(39, "Conductor and injection cement tops 8 ft MD",
      loc(1, 709, 448, 717, 460), loc(1, 612, 534, 621, 546))
u.add(40, "Conductor cement bottom 88; injection cement bottom 668 ft MD",
      u.find("88", occurrence=4), u.find("668", occurrence=3))
formation_names = [u.find("Top Etchegoin / Base Lower Tulare"),
                   u.find("Top Antelope / Base Etchegoin")]
formation_depths = [u.find("215", occurrence=0), u.find("332")]
u.add(43, "Lower Tulare, Etchegoin, and Antelope formations", *formation_names)
u.add(44, "Top Etchegoin / base Lower Tulare 215; top Antelope / base Etchegoin "
      "332 ft MD", *formation_depths)
u.add(47, "Top Etchegoin / base Lower Tulare; top Antelope / base Etchegoin markers",
      *formation_names)
u.add(48, "Formation-boundary markers at 215 and 332 ft MD", *formation_depths)
u.add(81, "Conductor String Cement; Steam Injector Cement", *cement_names)
u.add(87, "MWD survey MD stations 0–339 and 371–668 ft",
      loc(1, 427, 927, 445, 1059), loc(2, 427, 216, 445, 364))
u.add(88, "Vertical; survey inclinations shown on both pages",
      loc(1, 461, 927, 483, 1059), loc(2, 461, 216, 483, 364))
u.add(89, "Survey azimuths shown on both pages",
      loc(1, 495, 927, 529, 1059), loc(2, 495, 216, 529, 364))
u.single_borehole("Original Hole", u.find("Vertical, Original Hole"))

u.uncertain([1, 2, 3, 4], "The visible Seneca Resources logo is treated as the operator. "
            "SEC 19 is the labelled lease, and SUNSET 251SI-7 is the displayed well name. "
            "The visible API is 03062255; reconcile it with the screening-log API.")
u.uncertain([6, 7], "The visible header states ground elevation 1,017 ft and KB–ground "
            "distance 8 ft, but no visible absolute reference elevation; do not calculate it. "
            "The PDF text layer also contains 1,025 beneath the visible header, so the draft "
            "does not count that hidden text.")
u.uncertain([14, 32], "Set depths are treated as shoes; the landing joint, pup joints and "
            "float shoe are treated as other in-well equipment. Confirm that classification.")
u.uncertain([33, 34], "The 12-in and 6 3/4-in entries are wellbore sections; values are "
            "recorded as printed without judging engineering plausibility.")
u.uncertain([43, 44, 47, 48], "The Formations table names top/base boundaries. The draft "
            "counts the named formations and those same boundaries as markers; confirm.")
u.uncertain([55, 58, 59, 67, 70, 71, 72, 74], "Survey and schematic TVDs are present, "
            "but do not explicitly match every corresponding MD endpoint; no interpolation "
            "or rounding between near values is used.")
u.uncertain([81, 82, 83, 84, 85, 86], "Conductor and injection cement have distinct names. "
            "The injection job has slurry details, but the conductor entry lacks them, "
            "so all repeated-job slurry points are MISSING. Its lead and tail amounts are "
            "partial answers, not excess data.")
u.uncertain([87, 88, 89, 90], "Both pages were reviewed: page 2 continues the original "
            "hole survey and repeats the schematic; it does not add a second borehole.")

u.add_excess("Well location", [
    ("field", "Midway Sunset South", u.find("Midway Sunset South", occurrence=1),
     "Location is not scored."),
    ("PLSS", "SEC19/T11N/R23W", u.find("SEC19/T11N/R23W", occurrence=1),
     "Location is not scored."),
])
u.add_excess("Well type", [
    ("status", "Steam Injector", u.find("Steam Injector", occurrence=1),
     "Well type is not scored."),
])
u.add_excess("KB–ground height", [
    ("KB–ground", "8 ft", loc(1, 429, 139, 438, 152),
     "Height is not an absolute reference elevation."),
])
u.add_excess("Casing details", [
    ("conductor ID", "12.00 in", u.find("12.00"), "Inside diameter is not scored."),
    ("injection ID", "2.99 in", u.find("2.99", occurrence=0), "Inside diameter is not scored."),
    ("conductor length", "80.00 ft", u.find("80.00"), "String length is not scored."),
    ("injection length", "660.21 ft", u.find("660.21"), "String length is not scored."),
    ("pup-joint bottom", "16 ft", loc(1, 356, 396, 382, 407),
     "Intermediate joint bottom is not a string shoe."),
    ("joint bottom", "636 ft", loc(1, 343, 547, 373, 558),
     "Intermediate joint bottom is not a string shoe."),
    ("pup-joint bottom 2", "637 ft", loc(1, 356, 809, 392, 820),
     "Intermediate joint bottom is not a string shoe."),
    ("joint bottom 2", "667 ft", loc(1, 343, 884, 378, 895),
     "Intermediate joint bottom is not a string shoe."),
])
u.add_excess("Perforation details", [
    ("date", "2/9/2018", u.find("2/9/2018"), "Perforation date is not scored."),
    ("hole diameter", "0.290 in", u.find("0.290"), "Perforation hole diameter is not scored."),
    ("shot total", "40", loc(1, 489, 726, 501, 738), "Shot count is not scored."),
    ("shot density", "1.0 shots/ft", u.find("1.0"), "Shot density is not scored."),
    ("status", "Open - Flowing", u.find("Open - Flowing"), "Status is not scored."),
])
u.add_excess("Cement-top measurement methods", [
    ("conductor", "Cement to Surface", u.find("Cement to Surface"), "Method is not scored."),
    ("injection", "Volume Calculations", u.find("Volume Calculations"),
     "A method name is not the calculation steps."),
])
u.add_excess("Cement operational details", [
    ("test pressure", "2300 psi", u.find("2300"), "Pressure-test details are not scored."),
    ("water ahead", "10 bbl", u.find("10 bbls water ahead"), "Pump details are not scored."),
    ("excess", "50%", u.find("50% excess"), "A result is not a calculation's steps."),
    ("displacement water", "5.5 bbl", u.find("5.5"), "Displacement details are not scored."),
    ("returns", "NO RETURNS", u.find("NO RETURNS"), "Return status is not slurry volume."),
    ("plug pressure", "1074 psi", u.find("1074"), "Bump pressure is not scored."),
    ("CIP time", "18:24", u.find("18:24"), "Operation time is not scored."),
])
u.add_excess("Survey offsets, DLS, method and company", [
    ("page 1 offsets", "VS, NS and EW stations", loc(1, 592, 927, 695, 1055),
     "Survey offsets are not separate scored points."),
    ("page 2 offsets", "VS, NS and EW stations", loc(2, 592, 216, 695, 364),
     "Survey offsets are not separate scored points."),
    ("page 1 dogleg severity", "DLS stations", loc(1, 709, 927, 731, 1055),
     "Dogleg severity is not a scored point."),
    ("page 2 dogleg severity", "DLS stations", loc(2, 709, 216, 731, 364),
     "Dogleg severity is not a scored point."),
    ("page 1 method", "MWD", loc(1, 736, 927, 764, 1055), "Survey method is not scored."),
    ("page 2 method", "MWD", loc(2, 736, 216, 764, 364), "Survey method is not scored."),
    ("page 1 company", "Geo Guidance", loc(1, 781, 927, 824, 1055),
     "Survey company is not scored."),
    ("page 2 company", "Geo Guidance", loc(2, 781, 216, 824, 364),
     "Survey company is not scored."),
])
u.uncertain([32, 87], "Confirm the new excess categories cement operational details and "
            "survey offsets, dogleg severity, method, and company. Survey-column entries "
            "are grouped by page rather than counting every station as a separate item.")
u.add_provenance("Drawing timestamp", "3/10/2022 11:08:41 AM",
                 loc(1, 215, 185, 337, 195))
u.add_provenance("Page number", "Page 1/2", u.find("Page  1/2"))
u.add_provenance("Report printed", "3/10/2022", loc(1, 681, 1057, 814, 1069))
u.add_provenance("Report website", "www.natfuel.com/seneca", u.find("www.natfuel.com/seneca"))

if __name__ == "__main__":
    u.build()
