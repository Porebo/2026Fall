"""Reviewed source observations for U09; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U09", "Aera Energy LLC")
u.page_panel(1, (10, 10, 590, 764))
u.add(1, "AERA ENERGY LLC", u.find("AERA ENERGY LLC"))
u.add(2, "Belridge V", u.find("Belridge V"))
u.add(3, "WD38-2", u.find("WD38-2"))
u.add(4, "0403069404", u.find("0403069404"))
u.add(5, "3/8/2023", u.find("3/8/2023", occurrence=0))
u.add(6, "588.14 ft", u.find("588.14ft"))
u.add(7, "KELLY BUSHING @ 602.14 ft", u.find("602.14ft"))
u.add(8, "Base of fresh water MD: N/A", u.find("N/A", occurrence=1))
u.add(9, "Base of USDW MD: N/A", u.find("N/A", occurrence=0))
u.add(10, "14.0000, 7.0000, and 5.0000 in",
      u.find("14.0000", occurrence=1), u.find("7.0000", occurrence=3), u.find("5.0000"))
u.add(14, "14 in: 54.0 ft MD; 7 in: 421.8 ft MD; 5 in: 566.0 ft MD",
      u.find("54.0", occurrence=3), u.find("421.8"), u.find("566.0", occurrence=2))
u.add(16, "5.0000 in lower string top: 390 ft MD", u.find("390"))
u.add(28, "SLOTS: 0.0400; 397.14–563.70 ft", loc(1, 219.8, 493.8, 332.0, 499.5))
holes = [u.find("24.00in hole to 54.00ft"), u.find("9.88in hole to 421.00ft"),
         u.find("13.00in hole to 566.00ft")]
u.add(33, "24.00, 9.88, and 13.00 in hole sections", *holes)
u.add(34, "Hole sections to 54.00, 421.00, and 566.00 ft", *holes)
u.add(38, "Primary cement for 7 in production casing", u.find("Primary", occurrence=0))
u.add(39, "Primary cement top 14 ft MD", loc(1, 114.1, 193.0, 120.3, 198.2))
u.add(40, "Primary cement bottom 422 ft MD", u.find("422"))
u.add(43, "Tulare", u.find("Tulare", occurrence=1))
u.add(44, "Tulare top 221.58 ft MD", u.find("221.58", occurrence=0))
u.add(47, "Tulare marker", u.find("Tulare", occurrence=1))
u.add(48, "Tulare marker top 221.58 ft MD", u.find("221.58", occurrence=0))
u.add(72, "Tulare top 221.58 ft TVD", u.find("221.58", occurrence=1))
u.add(74, "Tulare marker top 221.58 ft TVD", u.find("221.58", occurrence=1))
u.add(81, "Primary: 3/8/2023", u.find("3/8/2023", occurrence=1))
u.add(82, "Primary: 189.5 sacks", u.find("189.5 sks"))
u.add(83, "Primary: 14.5 ppg", u.find("14.5 ppg"))
u.add(84, "Primary: 1.9 cf/sk", u.find("1.9 cf/sk"))
u.add(85, "Primary: A-5 MODIFIED TYPE III", u.find("TYPE III"))
u.add(86, "Primary: 35% silica flour", u.find("35%wC SILICA"))
u.single_borehole("ORIG HOLE", u.find("ORIG HOLE"))

u.uncertain([8, 9], "Freshwater and USDW MD fields explicitly state N/A, which counts "
            "as MET; no corresponding TVD entry is shown.")
u.uncertain([11, 12, 13], "The 5 in lower string lacks displayed grade, thread, and weight; "
            "SCH 10 is a casing schedule, not an explicit grade. All three repeated-string "
            "points are MISSING despite information on the other strings.")
u.uncertain([14, 16, 55, 57], "The lower 5 in casing starts at 390 ft and is represented "
            "below the upper strings, so the draft treats it as a liner. Confirm that "
            "interpretation and the use of casing base as shoe. The adjacent unlabelled "
            "component values are not assumed to be TVD answers.")
u.uncertain([17, 18, 28], "SLOTS at 397.14–563.70 ft are counted as an other flow/integrity "
            "feature, not automatically as perforations or perforation intervals. "
            "Confirm this distinction.")
u.uncertain([40], "The cement-stage table gives a 422 ft bottom and the remark says "
            "421.75 ft; the table value is used without judging accuracy.")
u.uncertain([43, 44, 47, 48, 72, 74], "Tulare is listed under MARKER DETAILS; the draft "
            "counts it as both a formation and a marker, with explicitly labeled MD "
            "and TVD values. Confirm the formation classification.")
u.uncertain([67], "TD TVD 566 ft is shown, but TVD bottoms for the other two hole "
            "sections are not; the repeated-section TVD hole-depth point is MISSING.")
u.uncertain([87, 88, 89], "The orientation field says TULARE UNIT, not a directional "
            "survey, inclination, azimuth, or an explicit vertical-hole statement.")

u.add_excess("Well type", [
    ("well type", "WATER DISPOSAL INJ", u.find("WATER DISPOSAL INJ"),
     "Well type is not among the scored points."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "565.00 ft", u.find("565.00ft"), "Plug-back depth is not a cement-plug endpoint."),
])
u.add_excess("Casing schedule", [
    ("14 in casing schedule", "SCH 10", u.find("SCH 10"),
     "Casing schedule is not an explicitly named grade."),
])
u.add_excess("Intermediate casing-joint bottom", [
    ("7 in intermediate joint", "343.72 ft", u.find("343.72ft", occurrence=0),
     "Intermediate joint bottom is not a complete-string shoe."),
])
u.add_excess("Slot width", [
    ("slot width", "0.0400 in", u.find("0.0400"),
     "The dimension is not one of the scored points."),
])
u.add_excess("Cement returns", [
    ("cement returns", "19.5 bbls", u.find("19.5 bbls"),
     "Return volume is not slurry volume."),
])
u.add_excess("Abandonment tag depth", [
    ("abandonment tag depth", "N/A", u.find("N/A", occurrence=2),
     "An abandonment tag depth is not among the scored points."),
])
u.uncertain([28, 38], "Confirm the excess categories well type, casing schedule, slot "
            "width, cement returns, and the explicit N/A abandonment-tag entry.")
u.add_provenance("Preparer initials", "BU238287", u.find("BU238287"))
u.add_provenance("Preparation date", "11/12/2025", u.find("11/12/2025"))

if __name__ == "__main__":
    u.build()
