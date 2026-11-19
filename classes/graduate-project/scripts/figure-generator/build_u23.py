"""Reviewed source observations for U23; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U23", "Cat Canyon Resources (logo)")
u.row_aligned_badges = True
u.page_panel(1, (15, 12, 580, 770))
u.page_panel(2, (15, 494, 280, 530), inset=True,
             label="Source page 2: proposed liner")
u.add(1, "Cat Canyon Resources (letterhead)", loc(1, 23, 16, 275, 65))
u.add(2, "G.W.P.", loc(1, 110, 88, 135, 98))
u.add(3, "848-24", loc(1, 135, 70, 160, 79))
u.add(4, "083-21273-02", loc(1, 110, 79, 156, 88))
u.add(5, "7/28/1979", loc(1, 110, 98, 144, 107))
u.add(6, "Ground elevation 556 ft", loc(1, 110, 125, 125, 135))
u.add(7, "Kelly Bushing 13 ft", loc(1, 110, 116, 121, 125))
u.add(8, "Base of fresh water 748 ft MD", loc(1, 417, 346, 433, 355))
u.add(9, "Base of USDW 1,932 ft MD", loc(1, 417, 437, 436, 446))
u.add(28, "Four torch-cut holes in top cement basket; liner slots "
      "2,528–2,988 ft MD; gravel pack",
      loc(1, 307, 50, 572, 68), loc(1, 350, 620, 476, 648),
      loc(1, 40, 720, 236, 730))
u.add(32, "Bull-nose guide shoe and two cement baskets",
      loc(1, 307, 50, 519, 59))
hole_sizes = [loc(1, 350, 246, 400, 273), loc(1, 442, 80, 464, 88),
              loc(1, 443, 89, 455, 97), loc(1, 442, 108, 464, 116),
              loc(1, 443, 117, 455, 125), loc(1, 446, 163, 479, 180)]
hole_depths = [loc(1, 435, 246, 474, 273), loc(1, 489, 80, 529, 97),
               loc(1, 489, 108, 529, 125), loc(1, 492, 163, 543, 180)]
u.add(33, "Current 02 holes: unknown, 9.875, 13 in; original 00: 9.875 "
      "and 12 in; replacement 00: 9.875 and 14 in; redrill 01: 9.875 and 13 in",
      *hole_sizes)
u.add(34, "Current 02: surface–50, 50–2,549, 2,549–2,990 ft; original and "
      "replacement 00: 50–2,215 and 2,215–2,369 ft; redrill 01: "
      "50–2,542 and 2,542–2,976 ft MD", *hole_depths)
plugs = [
    loc(1, 308, 135, 362, 144), loc(1, 419, 135, 485, 144),
    loc(1, 420, 135, 570, 153), loc(1, 301, 191, 355, 199),
    loc(1, 407, 191, 470, 199), loc(1, 472, 191, 538, 199),
    loc(1, 418, 200, 482, 209),
]
u.add(35, "Cement intervals in Abandonment 00 (three) and Abandonment 01 (four)",
      *plugs)
u.add(36, "Abandonment 00 plug tops 20, 1,062, 1,903 ft; "
      "Abandonment 01 plug tops 20, 952, 1,076, 1,925 ft MD", *plugs)
u.add(37, "Abandonment 00 plug bottoms 200, 1,363, 2,369 ft; "
      "Abandonment 01 plug bottoms 220, 1,076, 1,209, 2,976 ft MD", *plugs)
u.add(38, "Redrill 02: 7-in casing cemented", loc(1, 23, 346, 261, 355))
u.add(41, "Mud between cement intervals: 00 at 200–1,062 and 1,363–1,903 ft; "
      "01 at 220–952 and 1,209–1,925 ft",
      loc(1, 364, 135, 417, 144), loc(1, 487, 135, 543, 144),
      loc(1, 357, 191, 405, 199), loc(1, 396, 191, 577, 209))
names = loc(1, 55, 656, 72, 711)
md_ranges = loc(1, 135, 656, 174, 711)
tvd_ranges = loc(1, 218, 656, 258, 711)
u.add(43, "Sisquoc; table labelled Formation: S1A, S2, S3, S4, S5, S6",
      loc(1, 337, 455, 392, 473), names)
u.add(44, "Sisquoc top 1,932 ft; S1A–S6 ranges 2,494–2,552, 2,552–2,632, "
      "2,632–2,754, 2,754–2,796, 2,796–2,894, and 2,894–2,990 ft MD",
      loc(1, 417, 465, 436, 473), md_ranges)
u.add(45, "Producing zones S1A, S2, S3, S4, S5, S6", names)
u.add(46, "S1A–S6 ranges 2,494–2,552, 2,552–2,632, 2,632–2,754, "
      "2,754–2,796, 2,796–2,894, and 2,894–2,990 ft MD", md_ranges)
u.add(53, "Base of fresh water 746 ft TVD", loc(1, 417, 337, 433, 346))
u.add(54, "Base of USDW 1,886 ft TVD", loc(1, 417, 428, 436, 437))
u.add(72, "Sisquoc top 1,886 ft; S1A–S6 ranges 2,442–2,500, 2,500–2,580, "
      "2,580–2,702, 2,702–2,744, 2,744–2,842, and 2,842–2,990 ft TVD",
      loc(1, 417, 456, 436, 464), tvd_ranges)
u.add(73, "S1A–S6 ranges 2,442–2,500, 2,500–2,580, 2,580–2,702, "
      "2,702–2,744, 2,744–2,842, and 2,842–2,990 ft TVD", tvd_ranges)
u.add(90, "Original Completion 00; Redrill 01; Redrill 02",
      u.find("Original Completion - 00"), u.find("Redrill - 01", occurrence=1),
      u.find("Redrill - 02", occurrence=1))
u.applicable_boreholes()

u.uncertain([1, 2, 3, 4], "The named Cat Canyon Resources letterhead is treated as "
            "the operator. The source API is 083-21273-02, while screening uses "
            "0408321273; the source value is not silently normalized.")
u.uncertain([7], "The header says Kelly Bushing 13 ft, without explicitly calling it "
            "an elevation or a height above ground. The draft credits the stated "
            "reference value; verify whether it is instead a KB–ground height.")
u.uncertain([10, 11, 12, 13, 14, 16, 55, 57], "Page 1 describes current 02, "
            "historical 00 and 01, and page 2 explicitly adds a proposed 3.5-in "
            "liner to 02. The draft includes every represented casing and liner, "
            "including the proposed one, without treating it as completed. The "
            "current slotted-liner diameter and conductor grade, connection and "
            "weight are not stated; historical shoe depths and the old replacement "
            "liner top are not explicitly given. Proposed liner top 2,500 ft has "
            "no TVD. Thus the repeated-string points remain MISSING.")
u.uncertain([28, 32], "Slots and gravel pack are treated as other flow/integrity "
            "features. The torch-cut holes are in the cement basket, not explicitly "
            "casing cuts, and no MD is provided for them. The guide shoe and cement "
            "baskets are treated as other equipment.")
u.uncertain([33, 34, 67], "The surface-hole diameter is explicitly 'unknown', an "
            "answer under the presence-only rule. Historical hole intervals are "
            "included in addition to the current table; no complete corresponding "
            "TVD intervals are shown.")
u.uncertain([35, 36, 37, 38, 39, 40, 41, 81], "All three cement intervals in "
            "Abandonment 00 and all four in Abandonment 01 are retained as plugs; "
            "mud is explicitly listed between plugs in both histories. Current 02 "
            "casing is described as cemented, but the casing interval and cement "
            "returns do not explicitly give the fill endpoints. The abandonment "
            "headings identify those work stages, while the current casing-cement "
            "entry has no explicitly identified cement-job name, stage, or date, "
            "so point 81 remains MISSING. Confirm whether the adjacent Redrill 02 "
            "date identifies that cement job.")
u.uncertain([43, 44, 45, 46, 72, 73], "The six S1A–S6 rows appear under Producing "
            "Zones in a column labelled Formation, so the draft credits both "
            "formation and zone points and records all MD and TVD ranges as printed. "
            "Sisquoc is a separate formation top. The S6 TVD bottom is printed "
            "as 2,990 ft; no plausibility correction is made.")
u.uncertain([82, 83, 84, 85, 86], "Current 02 casing cement gives volume, density, "
            "yield, type and additives, but the seven displayed historical cement "
            "intervals do not; repeated-job slurry points are MISSING.")
u.uncertain([87, 88, 89, 90], "The file identifies original 00 and redrills 01 "
            "and 02. Page 2's proposed liner belongs to 02 and is not counted as "
            "a fourth borehole. No MD/inclination/azimuth path is supplied for all "
            "three boreholes. Explicit vertical statements are absent.")

u.add_excess("Well location", [
    ("county", "Santa Barbara", loc(1, 110, 107, 160, 116),
     "County is not a scored point."),
])
u.add_excess("Historical operation dates", [
    (name, value, loc(1, 110, y, 150, y + 9), "Operation date is not a scored point.")
    for name, value, y in (("liner replacement 00", "3/27/1984", 135),
                           ("abandonment 00", "10/9/2016", 144),
                           ("redrill 01", "11/8/2016", 153),
                           ("abandonment 01", "6/18/2020", 163),
                           ("redrill 02", "10/30/2020", 172))
])
u.add_excess("Cement returns", [
    ("current casing", "80 bbl returned to surface", loc(1, 101, 373, 270, 391),
     "Returns are not a separate scored point."),
])
u.add_excess("Slotted-liner details", [
    ("slot description", '64R-25M-2"S-6"C', loc(1, 417, 639, 476, 648),
     "Slot configuration is not a separate scored point."),
])
u.add_excess("Gravel-pack details", [
    ("gravel", "350 CF 12x20 HOT gravel", loc(1, 150, 720, 236, 730),
     "Gravel quantity and size are not scored points."),
])
u.uncertain([28, 32, 38], "Confirm the new excess categories operation dates, "
            "slotted-liner configuration and gravel-pack details.")
u.add_provenance("Drawing scale", "Not to scale", u.find("Not to scale"))

if __name__ == "__main__":
    u.build()
