"""Reviewed source observations for U07; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U07", "Aera Energy LLC")
u.page_panel(1, (10, 10, 590, 764))
u.add(1, "AERA ENERGY LLC", u.find("AERA ENERGY LLC"))
u.add(2, "Belridge IV", u.find("Belridge IV"))
u.add(3, "WD26-2", u.find("WD26-2"))
u.add(4, "0403069394", u.find("0403069394"))
u.add(5, "2/22/2023", u.find("2/22/2023"))
u.add(6, "593.55 ft", u.find("593.55ft"))
u.add(7, "KELLY BUSHING @ 607.55 ft", u.find("607.55ft"))
u.add(8, "Base of fresh water MD: N/A", u.find("N/A", occurrence=1))
u.add(9, "Base of USDW MD: N/A", u.find("N/A", occurrence=0))
u.add(10, "14.0000, 7.0000, and 5.0000 in",
      u.find("14.0000", occurrence=1), u.find("7.0000", occurrence=3), u.find("5.0000"))
u.add(14, "14 in: 54.0 ft MD; 7 in: 415.2 ft MD; 5 in: 547.0 ft MD",
      u.find("54.0", occurrence=3), u.find("415.2"), u.find("547.0", occurrence=1))
u.add(16, "5.0000 in lower string top: 392 ft MD", loc(1, 90.2, 142.8, 100.4, 148.9))
u.add(28, "SLOTS: 0.0400; 398.96–544.70 ft", loc(1, 219.8, 331.2, 313.2, 336.9))
hole_locations = [u.find("24.00in hole to 54.00ft"), u.find("13.00in hole to 547.00ft"),
                  u.find("9.88in hole to 970.00ft")]
u.add(33, "24.00, 13.00, and 9.88 in hole sections", *hole_locations)
u.add(34, "Hole sections to 54.00, 547.00, and 970.00 ft", *hole_locations)
u.add(35, "CEMENT PLUG", u.find("CEMENT PLUG"))
u.add(36, "Cement plug top 547 ft MD", loc(1, 101.6, 433.2, 111.8, 439.3))
u.add(37, "Cement plug bottom 970 ft MD", loc(1, 146.4, 430.6, 156.5, 436.6))
u.add(38, "Primary cement for 7 in production casing", u.find("Primary", occurrence=0))
u.add(39, "Primary cement top 36 ft MD", loc(1, 114.5, 227.2, 120.4, 232.4))
u.add(40, "Primary cement bottom 415 ft MD", loc(1, 141.1, 227.2, 149.9, 232.4))
u.add(43, "Tulare", u.find("Tulare", occurrence=1))
u.add(44, "Tulare top 217.32 ft MD", u.find("217.32", occurrence=0))
u.add(47, "Tulare marker", u.find("Tulare", occurrence=1))
u.add(48, "Tulare marker top 217.32 ft MD", u.find("217.32", occurrence=0))
u.add(72, "Tulare top 217.32 ft TVD", u.find("217.32", occurrence=1))
u.add(74, "Tulare marker top 217.32 ft TVD", u.find("217.32", occurrence=1))
u.add(81, "Plug: 2/23/2023; primary: 2/24/2023",
      u.find("2/23/2023"), u.find("2/24/2023"))
u.add(82, "Plug: 136 sacks; primary: 157 sacks", u.find("136 sks"), u.find("157 sks"))
u.add(83, "Plug and primary: 14.5 ppg", u.find("14.5 ppg", occurrence=0),
      u.find("14.5 ppg", occurrence=1))
u.add(84, "Plug and primary: 1.9 cf/sk", u.find("1.9 cf/sk", occurrence=0),
      u.find("1.9 cf/sk", occurrence=1))
u.add(85, "Plug and primary: A-5 MODIFIED TYPE III",
      u.find("TYPE III", occurrence=0), u.find("TYPE III", occurrence=1))
u.add(86, "Plug and primary: silica flour", u.find("SILICA FLOUR", occurrence=0),
      u.find("SILICA FLOUR", occurrence=1))
u.single_borehole("ORIG HOLE", u.find("ORIG HOLE"))

u.uncertain([8, 9], "Freshwater and USDW MD fields explicitly state N/A, which counts "
            "as MET; no corresponding TVD entry is shown.")
u.uncertain([11, 12, 13], "The 5 in lower string lacks displayed grade, thread, and weight; "
            "SCH 10 is a casing schedule, not an explicit grade. All three repeated-string "
            "points are MISSING despite information on the other strings.")
u.uncertain([14, 16, 55, 57], "The lower 5 in casing starts at 392 ft and is represented "
            "below the upper strings, so the draft treats it as a liner. Confirm that "
            "interpretation and the use of casing base as shoe. The adjacent unlabelled "
            "component values are not assumed to be TVD answers.")
u.uncertain([17, 18, 28], "SLOTS at 398.96–544.70 ft are counted as an other flow/integrity "
            "feature, not automatically as perforations or perforation intervals. "
            "Confirm this distinction.")
u.uncertain([19, 35, 36, 37], "The source describes an open hole plugged at 547–970 ft; "
            "the draft scores the cement plug and its endpoints, not an open-hole "
            "completion interval.")
u.uncertain([39], "The stage table gives a 36 ft top while the remark gives 36.5 ft; "
            "the table value is used without judging accuracy.")
u.uncertain([43, 44, 47, 48, 72, 74], "Tulare is listed under MARKER DETAILS; the draft "
            "counts it as both a formation and a marker, with explicitly labeled MD "
            "and TVD values. Confirm the formation classification.")
u.uncertain([67], "TD TVD 969.98 ft is shown, but TVD bottoms for the other two hole "
            "sections are not; the repeated-section TVD hole-depth point is MISSING.")
u.uncertain([87, 88, 89], "The orientation field says TULARE UNIT, not a directional "
            "survey, inclination, azimuth, or an explicit vertical-hole statement.")

u.add_excess("Well type", [
    ("well type", "WATER DISPOSAL INJ", u.find("WATER DISPOSAL INJ"),
     "Well type is not among the scored points."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "546.00 ft", u.find("546.00ft"), "Plug-back depth is not a cement-plug endpoint."),
])
u.add_excess("Casing schedule", [
    ("14 in casing schedule", "SCH 10", u.find("SCH 10"),
     "Casing schedule is not an explicitly named grade."),
])
u.add_excess("Intermediate casing-joint bottom", [
    ("7 in intermediate joint", "335.55 ft", u.find("335.55ft", occurrence=0),
     "Intermediate joint bottom is not a complete-string shoe."),
])
u.add_excess("Slot width", [
    ("slot width", "0.0400 in", loc(1, 241.4, 331.2, 260.2, 336.9),
     "The dimension is not one of the scored points."),
])
u.add_excess("Cement returns and fallback", [
    ("cement returns", "21 bbls", u.find("21 bbls"),
     "Return volume is not slurry volume."),
    ("cement fallback", "22.5 ft", u.find("22.5"),
     "Cement fallback is not a separately scored point."),
])
u.add_excess("Abandonment tag depth", [
    ("abandonment tag depth", "N/A", u.find("N/A", occurrence=2),
     "An abandonment tag depth is not among the scored points."),
])
u.uncertain([28, 38], "Confirm the new excess categories well type, casing schedule, slot "
            "width, cement returns/fallback, and the explicit N/A abandonment-tag entry.")
u.add_provenance("Preparer initials", "BU238287", u.find("BU238287"))
u.add_provenance("Preparation date", "11/12/2025", u.find("11/12/2025"))

if __name__ == "__main__":
    u.build()
