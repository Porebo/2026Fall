"""Reviewed source observations for U14; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U14", "Aera Energy LLC")
u.page_panel(1, (10, 10, 590, 764))
u.add(1, "Aera Energy LLC", u.find("Aera Energy LLC"))
u.add(2, "S1-PZ (within S1-PZ-2IR)", loc(1, 80.4, 24.9, 102.2, 32.3))
u.add(3, "2IR", loc(1, 103.5, 24.9, 115.9, 32.3))
u.add(4, "0401924187", u.find("0401924187"))
u.add(6, "Ground elevation 1,052.1 ft", u.find("1,052.1ft"))
u.add(7, "Kelly bushing 1,062.10 ft", u.find("1,062.10ft"))
u.add(9, "Base of USDW N/A", u.find("N/A"))
u.add(10, "12.500; 7.000; 5.500 in",
      u.find("12.500", occurrence=1), u.find("7.000", occurrence=6),
      u.find("5.500", occurrence=2))
u.add(12, "12.5-in: Plain End; 7-in and 5.5-in: LT&C",
      u.find("Plain End"), loc(1, 310.1, 125.7, 324.6, 131.4),
      loc(1, 300.7, 418.8, 315.2, 424.5))
u.add(13, "12.5-in: 33.38 ppf; 7-in: 23.00 ppf; 5.5-in: 15.50 ppf",
      u.find("33.38ppf"), u.find("23.00ppf", occurrence=0),
      u.find("15.50ppf", occurrence=0))
u.add(14, "Casing bases 50.0; 482.0; 824.0 ft MD",
      u.find("50.0", occurrence=1), u.find("482.0", occurrence=2),
      u.find("824.0", occurrence=2))
u.add(16, "5.5-in lower string top 464 ft MD", loc(1, 94.2, 144.2, 104.3, 150.3))
u.add(28, "Slots 476.4–481.4 and 481.4–783.4 ft",
      loc(1, 211.9, 426.3, 326.9, 432.0),
      loc(1, 211.9, 433.7, 326.9, 439.4))
u.add(32, "Kill string: tubing fatigue nipple, tubing, casing isolation cup tool",
      loc(1, 29.4, 400.2, 86.8, 406.3), u.find("Tubing", occurrence=1),
      u.find("Casing Isolation Cup Tool"), u.find("Tubing", occurrence=2))
u.add(34, "Hole labels: to 0.00; 482.00; 824.00; 841.00 ft MD",
      u.find("hole to 0.00ft"), u.find("hole to 482.00ft"),
      u.find("hole to 824.00ft"), u.find("8.75in hole to 841.00ft"))
u.add(38, "Primary cement stage for 7-in production casing", u.find("Primary"))
u.add(39, "Primary cement top 10 ft MD", loc(1, 116.8, 194.8, 123.4, 200.5))
u.add(40, "Primary cement bottom 482 ft MD", loc(1, 153.2, 194.8, 163.1, 200.5))
u.add(43, "Etchegoin and Temblor", u.find("Etchegoin"), u.find("Temblor"))
u.add(44, "Etchegoin 88.4 ft; Temblor 559.9 ft MD", u.find("88.4"), u.find("559.9"))
u.add(47, "Etchegoin and Temblor markers", u.find("Etchegoin"), u.find("Temblor"))
u.add(48, "Marker tops 88.4 and 559.9 ft MD", u.find("88.4"), u.find("559.9"))
u.add(81, "Primary cement 7/10/2002", u.find("7/10/2002"))
u.add(85, 'Lilly Blend = Class "C" cement', u.find('CLASS "C"'))
u.add(86, "35% silica flour, 10% gypsum, 10% fillite, 1% sodium metasilicate, "
      "3% CaCl2, 0.2% D46 antifoam, and cellophane flake",
      loc(1, 122.0, 289.6, 175.0, 295.3), loc(1, 22.2, 295.9, 171.1, 314.5))
u.add(88, "Directional", u.find("Directional"))
u.single_borehole("Wellbore 00", loc(1, 80.4, 41.9, 89.0, 49.3))

u.uncertain([2, 3], "S1-PZ-2IR is split into S1-PZ and 2IR for the draft, whereas "
            "screening lists Penn-Zier / 2-IR. Confirm whether the well name explicitly "
            "answers the separate lease and well-number points.")
u.uncertain([9], "The base-of-USDW field explicitly says N/A, which counts as an answer.")
u.uncertain([11, 12, 13, 14, 16], "The 12.5-in string has Sch20 but no explicit grade, "
            "so repeated-string grade is MISSING. Plain End is counted as a connection "
            "entry. Casing bases are treated as shoes, and the 5.5-in lower string as "
            "a liner even though the source calls it casing.")
u.uncertain([17, 18, 28], "Both SLOTS entries are treated as other flow/integrity features "
            "rather than explicit perforations; confirm the classification.")
u.uncertain([30, 32, 35], "The PLUG DETAILS table lists a kill-string assembly, tubing "
            "and a casing isolation cup tool, not an explicitly identified cement plug "
            "or packer. They are counted as other equipment.")
u.uncertain([33, 34], "Hole depths are labelled to 0, 482, 824, and 841 ft; only 8.75 in "
            "is stated, so repeated-hole diameter is MISSING. Confirm whether the zero-ft "
            "label is intended as a separate hole section.")
u.uncertain([43, 44, 47, 48], "Etchegoin and Temblor appear under MARKER DETAILS; "
            "the draft treats them as both formation names and markers. Confirm the "
            "formation classification.")
u.uncertain([81, 82, 83, 84, 85, 86], "The single primary job is linked to the Lilly "
            "Blend remarks for production casing, supplying cement class and additives "
            "but no explicit slurry quantity, density, or yield.")
u.uncertain([88], "Directional is treated as an explicit deviation statement answering "
            "inclination only; no path stations or azimuth are shown.")

u.add_excess("Well type", [
    ("well type", "Producer", u.find("Producer"), "Well type is not scored."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "824.0 ft", u.find("824.0ft"), "Plug-back depth is not a cement-plug endpoint."),
])
u.add_excess("Casing schedule", [
    ("12.5-in string", "Sch20", u.find("Sch20"), "Schedule is not an explicit casing grade."),
])
u.add_excess("Intermediate casing-joint bottoms", [
    (name, value, loc(1, x0, y, x1, y + 5.7),
     "A joint bottom is not the full string shoe.")
    for name, value, x0, y, x1 in (
        ("7-in joint 1", "52.5 ft", 341.5, 125.7, 352.4),
        ("7-in joint 2", "72.5 ft", 341.5, 140.3, 352.4),
        ("7-in joint 3", "92.6 ft", 341.5, 153.7, 352.4),
        ("7-in joint 4", "440.5 ft", 338.3, 278.1, 352.4),
        ("5.5-in joint 1", "476.4 ft", 338.3, 418.8, 352.4),
    )
])
u.add_excess("Slot specifications", [
    ("slot interval 1", '0.030, 2.000 in, 6.000', loc(1, 233.5, 426.3, 287.8, 432.0),
     "Slot dimensions are not separately scored."),
    ("slot interval 2", '0.030, 2.000 in, 6.000', loc(1, 233.5, 433.7, 287.8, 439.4),
     "Slot dimensions are not separately scored."),
])
u.uncertain([28, 38], "Confirm the new excess categories well type, casing schedule, "
            "and slot specifications.")
u.add_provenance("Preparer initials", "xyz", u.find("xyz"))
u.add_provenance("Preparation date", "5/8/2019", u.find("5/8/2019"))

if __name__ == "__main__":
    u.build()
