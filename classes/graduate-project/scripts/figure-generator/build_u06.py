"""Reviewed source observations for U06; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U06", "Aera Energy LLC")
u.page_panel(1, (10, 10, 590, 760))
u.add(1, "Aera Energy LLC", u.find("Aera Energy LLC"))
u.add(3, "566S6-1N", u.find("566S6-1N"))
u.add(4, "0403066227", u.find("0403066227"))
u.add(6, "607.63 ft", u.find("607.63ft"))
u.add(7, "KELLY BUSHING @ 621.63 ft", u.find("621.63ft"))
u.add(9, "Base of USDW, MD: N/A", u.find("N/A", occurrence=1))
u.add(10, "14.000, 9.625, and 5.500 in",
      u.find("14.000", occurrence=1), u.find("9.625", occurrence=2),
      u.find("5.500", occurrence=4))
u.add(12, "14 in: PLAIN END; 9.625 and 5.500 in: LTC",
      u.find("PLAIN END"), u.find("LTC", occurrence=0), u.find("LTC", occurrence=1))
u.add(13, "14 in: 36.71 ppf; 9.625 in: 36.00 ppf; 5.500 in: 15.50 ppf",
      u.find("36.71ppf"), u.find("36.00ppf"), u.find("15.50ppf", occurrence=0))
u.add(14, "14 in: 54.0 ft MD; 9.625 in: 233.0 ft MD; 5.500 in: 2,280.7 ft MD",
      u.find("54.0", occurrence=2), u.find("233.0", occurrence=1), u.find("2,280.7"))

tops = [1760, 1780, 1800, 1820, 1840, 1860, 1880, 1900, 1920,
        1970, 1990, 2010, 2035, 2055, 2075, 2095, 2115]
perf_ranges = [
    loc(1, 224.8, 529.0, 264.2, 542.2),
    loc(1, 224.8, 551.2, 264.2, 624.0),
    loc(1, 224.8, 632.9, 264.2, 668.6),
]
u.add(17, "Perforation tops (ft MD): " + ", ".join(f"{n:,}" for n in tops), *perf_ranges)
u.add(18, "Perforation intervals (ft MD): " +
      ", ".join(f"{n:,}–{n+1:,}" for n in tops), *perf_ranges)
u.add(24, "No casing damage", u.find("No casing damage"))
u.add(30, "Permanent Packer, 1,950–1,952 ft MD", u.find("Permanent Packer"))
hole_locations = [u.find("24.00in hole to 54.00ft"), u.find("12.25in hole to 238.00ft"),
                  u.find("8.75in hole to 2291.00ft")]
u.add(33, "24.00, 12.25, and 8.75 in hole sections", *hole_locations)
u.add(34, "Hole sections to 54.00, 238.00, and 2,291.00 ft", *hole_locations)
u.add(38, "Primary cement for 9.625 in and 5.500 in casing",
      u.find("Primary", occurrence=0), u.find("Primary", occurrence=1))
u.add(39, "9.625 in casing: top 15 ft MD; 5.500 in casing: top 14 ft MD",
      loc(1, 116.8, 199.9, 123.4, 205.7), loc(1, 116.8, 234.0, 123.4, 239.7))
u.add(40, "9.625 in casing: bottom 233 ft MD; 5.500 in casing: bottom 2,281 ft MD",
      loc(1, 153.4, 199.9, 163.1, 205.7), loc(1, 147.8, 234.0, 163.0, 239.7))
names = [u.find("Tulare"), u.find("San Joaquin/Etchegoin"), u.find("Reef Ridge Diatomite")]
depths = [u.find("251.91"), u.find("1,119.05"), u.find("1,220.55")]
u.add(43, "Tulare; San Joaquin/Etchegoin; Reef Ridge Diatomite", *names)
u.add(44, "Tulare 251.91 ft; San Joaquin/Etchegoin 1,119.05 ft; "
      "Reef Ridge Diatomite 1,220.55 ft MD", *depths)
u.add(47, "Tulare; San Joaquin/Etchegoin; Reef Ridge Diatomite", *names)
u.add(48, "Tulare 251.91 ft; San Joaquin/Etchegoin 1,119.05 ft; "
      "Reef Ridge Diatomite 1,220.55 ft MD", *depths)
u.add(81, "9.625 in primary: 7/27/2019; 5.500 in primary: 7/29/2019",
      u.find("7/27/2019"), u.find("7/29/2019"))
u.add(82, "9.625 in primary: 104 sacks; 5.500 in primary: 300 sacks",
      u.find("104 sks"), u.find("300 sks"))
u.add(83, "9.625 in primary: 14.5 ppg; 5.500 in primary: 12 ppg",
      u.find("14.5 ppg"), u.find("12 ppg"))
u.add(84, "9.625 in primary: 1.9 cf/sk; 5.500 in primary: 2.57 cf/sk",
      u.find("1.9 cf/sk"), u.find("2.57 cf/sk"))
u.add(85, "9.625 in: A-5 MODIFIED TYPE III; 5.500 in: B-3 EconoCem TYPE III",
      loc(1, 16.0, 309.7, 75.8, 315.5), loc(1, 22.0, 341.5, 81.9, 347.3))
u.add(86, "Both primary jobs list silica flour (35% wC and 25.2 lb/sk)",
      u.find("SILICA FLOUR", occurrence=0), u.find("SILICA FLOUR", occurrence=1))
u.add(88, "Orientation: Directional", u.find("Directional"))
u.single_borehole("Wellbore: 00", u.find("Wellbore: 00"))

u.uncertain([2, 3], "The source identifies the well as 566S6-1N but does not state a lease "
            "name. The screening log says lease Unspecified and well 566S6-1; reconcile "
            "the trailing N against the source rather than silently changing the evidence.")
u.uncertain([9], "The explicit USDW MD entry is N/A; under the presence rule it is MET. "
            "The TVD cell is not separately answered.")
u.uncertain([11], "K-55 is shown for the two smaller casings, but the 14 in string shows "
            "SCH 10, a schedule rather than an explicitly stated material grade; the "
            "repeated-casing grade point is MISSING.")
u.uncertain([14], "The casing table reports the 5.5 in base as 2,280.7 ft MD, while a "
            "component line ends at 2,280.21 ft. Both are present; confirm the shoe interpretation.")
u.uncertain([17, 18], "The first number of each of the 17 displayed perforation intervals "
            "is used for the depth point; the interval point lists both endpoints.")
u.uncertain([24, 25, 65], "'No casing damage' is an explicit answer about damage type. "
            "The draft leaves both MD and TVD damage extent MISSING because no extent "
            "entry is separately given; confirm how explicit absence applies to extent.")
u.uncertain([30, 35, 36, 37], "PLUG DETAILS contains a Permanent Packer, not a cement plug; "
            "it is counted as a packer only.")
u.uncertain([43, 44, 47, 48], "The three named geologic units appear under MARKER DETAILS; "
            "the draft counts their names and depths both as markers and formations. "
            "Confirm this classification and whether each is a formation.")
u.uncertain([88], "'Directional' is treated as an explicit deviation statement, answering "
            "inclination only; no survey stations or azimuth are shown.")
u.uncertain([86], "Both cement remarks list silica flour; the additive amount spans a line "
            "break, but the named additive is explicit for each job.")

u.add_excess("Well type", [
    ("type", "Injector", u.find("Injector"), "Well type is not among the scored points."),
])
u.add_excess("Plug-back depth", [
    ("PBMD", "2,255.37 ft", u.find("2,255.37ft", occurrence=1),
     "Plug-back depth is not a cement-plug endpoint."),
])
u.add_excess("Completion date", [
    ("completion date", "08/12/2019", u.find("08/12/2019"),
     "Completion date is not a scored point."),
])
u.add_excess("Casing schedule", [
    ("14 in casing schedule", "SCH 10", u.find("SCH 10"),
     "Schedule is not a casing grade or a separately scored point."),
])
u.add_excess("Flag joint", [
    ("flag joint", "1,782 ft", loc(1, 296.8, 543.9, 355.6, 549.6),
     "Flag-joint position is not a casing shoe, stub, or liner top."),
])
u.add_excess("Intermediate casing-joint bottoms", [
    ("5.5 in joint bottom", "1,781.76 ft", u.find("1,781.76ft"),
     "An intermediate joint bottom is not a complete-string shoe."),
    ("5.5 in joint bottom", "2,255.37 ft", u.find("2,255.37ft", occurrence=0),
     "An intermediate joint bottom is not a complete-string shoe."),
])
u.add_excess("Perforation shot density", [
    (f"interval {depth:,}–{depth+1:,} ft", f"{density} shots/ft",
     loc(1, 265.8, y, 295.3, y + 5.8), "Shot density is not a scored point.")
    for depth, y, density in zip(
        tops,
        (529.1, 536.4, 551.3, 558.7, 566.2, 573.6, 581.1, 588.5, 595.9,
         603.3, 610.7, 618.1, 633.0, 640.5, 647.9, 655.3, 662.8),
        (2, 2, 2, 4, 4, 4, 4, 4, 4, 2, 2, 2, 4, 4, 4, 4, 4))
])
u.add_excess("Cement return volumes", [
    ("9.625 in job returns", "15 bbls", loc(1, 110.5, 316.2, 128.6, 321.9),
     "Return volume is not the slurry-volume point."),
    ("5.500 in job returns", "10 bbls", loc(1, 113.5, 347.9, 131.7, 353.6),
     "Return volume is not the slurry-volume point."),
])
u.add_excess("Abandonment tag depth", [
    ("abandonment tag depth", "N/A", u.find("N/A", occurrence=0),
     "An abandonment tag depth is not among the scored points."),
])
u.uncertain([11, 38], "Confirm the new excess categories well type, casing schedule, "
            "cement return volumes, and the explicit N/A abandonment-tag entry.")
u.add_provenance("Preparer initials", "KB", u.find("Initials: KB"))
u.add_provenance("Preparation date", "3/10/2020", u.find("3/10/2020"))

if __name__ == "__main__":
    u.build()
