"""Reviewed source observations for U08; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U08", "BreitBurn Operating, LP")
u.page_panel(1, (15, 0, 560, 45), layout=(230, 90, 538, 45))
u.page_panel(1, (15, 110, 318, 750), layout=(230, 145, 248, 630),
             label="Source page 1: schematic")
u.page_panel(1, (318, 110, 540, 265), layout=(485, 145, 220, 200),
             label="Upper source detail")
u.page_panel(1, (318, 350, 540, 371), layout=(485, 355, 220, 30),
             label="Mid-depth source detail")
u.page_panel(1, (318, 570, 540, 737), layout=(485, 400, 220, 220),
             label="Lower source detail")
u.badge_size = (8.5, 5.9)
u.add(1, "BreitBurn Operating, LP", u.find("BreitBurn Operating, LP"))
u.add(2, "Santa Fe Springs Unit", u.find("Santa Fe Springs Unit"))
u.add(3, "811B", u.find("811B"))
u.add(4, "040371671000", u.find("040371671000"))
u.add(5, "12/15/1949", u.find("12/15/1949"))
u.add(6, "GL 156 ft", u.find("GL - 156"))
u.add(7, "KB 168 ft", u.find("KB - 168"))
u.add(8, "BFW estimate 1,066 ft MD", u.find("1066"))
u.add(9, "BASE_USDW 2,224 ft MD", u.find("2,224"))
strings = [u.find("Casing: 7"), u.find("Casing: 11.75"),
           u.find("Liner: 5.5"), u.find("Liner: 4")]
u.add(10, "7, 11.75, 5.5, and 4 in", *strings)
u.add(11, "7, 11.75, 5.5, and 4 in strings: J-55",
      *(u.find("J-55", occurrence=i) for i in range(4)))
u.add(13, "7 in: 23; 11.75 in: 47#; 5.5 in: 17#; 4 in: 11.34#",
      u.find("23"), u.find("47#"), u.find("17#"), u.find("11.34#"))
shoes = [u.find("[0-4343]"), u.find("[0-892]", occurrence=1),
         u.find("[4272-4583]"), u.find("[4554-4610]", occurrence=1)]
u.add(14, "7 in: 4,343 ft; 11.75 in: 892 ft; "
      "5.5 in liner: 4,583 ft; 4 in liner: 4,610 ft MD", *shoes)
liner_tops = [u.find("[4272-4583]"), u.find("[4554-4610]", occurrence=1)]
u.add(16, "5.5 in liner: 4,272 ft; 4 in liner: 4,554 ft MD", *liner_tops)
perfs = [u.find("[3830-3860]"), u.find("[3860-3875]"),
         u.find("[3870-3950]"), u.find("[4010-4050]")]
u.add(17, "Perforation tops: 3,830; 3,860; 3,870; 4,010 ft MD", *perfs)
u.add(18, "Perforations: 3,830–3,860; 3,860–3,875; "
      "3,870–3,950; 4,010–4,050 ft MD", *perfs)
u.add(28, "Test holes at 3,803 and 3,947–3,951 ft; WSO at 4,343 ft; "
      "inactive slots at 4,346–4,544, 4,551–4,581, and 4,554–4,610 ft",
      u.find("Test Holes:", occurrence=0), u.find("Test Holes:", occurrence=1),
      u.find("WSO:"), *(u.find("Inactive Slots:", occurrence=i) for i in range(3)))
u.add(30, "Halliburton PLT packer", u.find("Halliburton PLT pkr"))
u.add(32, "Tubing; liner hanger; Baash-Ross adapter", u.find("Tubing:"),
      u.find("Liner Hanger", occurrence=0), u.find("Adapter:"))
holes = [u.find('Hole: 15"  [0-892]'),
         u.find('Hole: 10.625" Wall scraped to 11" f/ 4343\' to 4402\' [892-4402]'),
         u.find('Hole: 6.125"  [4402-4584]'),
         u.find('Hole: 4.625"  [4584-4610]')]
u.add(33, "15, 10.625, 6.125, and 4.625 in holes; wall scraped to 11 in",
      *holes, u.find("Wall scraped to 11"))
u.add(34, "Hole sections: 0–892, 892–4,402, 4,402–4,584, "
      "and 4,584–4,610 ft MD; scraped section 4,343–4,402 ft",
      *holes, u.find("Wall scraped to 11"))
plugs = [u.find("Cement Plug:", occurrence=i) for i in range(3)]
plug_ranges = [u.find("[4203-4272]"), u.find("[4272-4544]"), u.find("[4544-4610]")]
u.add(35, "Three cement plugs", *plugs)
u.add(36, "Cement plug tops: 4,203; 4,272; 4,544 ft MD", *plug_ranges)
u.add(37, "Cement plug bottoms: 4,272; 4,544; 4,610 ft MD", *plug_ranges)
fills = [u.find("Cement:", occurrence=i) for i in range(3)]
fill_ranges = [u.find("[0-892]", occurrence=3), u.find("[1746-4343]"),
               u.find("[4343-4402]")]
u.add(38, "Three cement fill entries: 15 in, 10.625 in, and 10.625 in", *fills)
u.add(39, "Cement fill tops: 0; 1,746; 4,343 ft MD", *fill_ranges)
u.add(40, "Cement fill bottoms: 892; 4,343; 4,402 ft MD", *fill_ranges)
u.add(43, "MEYER SHALE", u.find("MEYER SHALE"))
u.add(44, "MEYER SHALE: 4,159 ft MD", u.find("4,159"))
marker_text = ("UHZ_100 2,224; UHZ_200 2,704; UHZ_300 2,991; UHZ_400 3,280; "
               "UHZ_500 3,449; FOIX_100 3,592; FOIX_200 3,663; BELL_100 3,742; "
               "BELL_200 3,816; BELL_300 3,971; MEYER SHALE 4,159; "
               "MEYER_100 4,162; MEYER_200 4,338; MEYER_300 4,433 ft")
marker_column = loc(1, 114, 414, 205, 709)
u.add(47, "UHZ_100–500; FOIX_100–200; BELL_100–300; "
      "MEYER SHALE; MEYER_100–300", marker_column)
u.add(48, marker_text + " MD", marker_column)
u.add(53, "BFW estimate 1,066 ft TVD (MD=TVD)", u.find("1066"))
u.add(54, "BASE_USDW 2,224 ft TVD (MD=TVD)", u.find("2,224"))
u.add(55, "String shoes: 4,343; 892; 4,583; 4,610 ft TVD (MD=TVD)", *shoes)
u.add(57, "Liner tops: 4,272 and 4,554 ft TVD (MD=TVD)", *liner_tops)
u.add(58, "Perforation tops: 3,830; 3,860; 3,870; 4,010 ft TVD (MD=TVD)", *perfs)
u.add(59, "Perforations: 3,830–3,860; 3,860–3,875; 3,870–3,950; "
      "4,010–4,050 ft TVD (MD=TVD)", *perfs)
u.add(67, "Hole sections: 0–892, 892–4,402, 4,402–4,584, "
      "and 4,584–4,610 ft TVD; scraped section 4,343–4,402 ft (MD=TVD)",
      *holes, u.find("Wall scraped to 11"))
u.add(68, "Cement plug tops: 4,203; 4,272; 4,544 ft TVD (MD=TVD)", *plug_ranges)
u.add(69, "Cement plug bottoms: 4,272; 4,544; 4,610 ft TVD (MD=TVD)", *plug_ranges)
u.add(70, "Cement fill tops: 0; 1,746; 4,343 ft TVD (MD=TVD)", *fill_ranges)
u.add(71, "Cement fill bottoms: 892; 4,343; 4,402 ft TVD (MD=TVD)", *fill_ranges)
u.add(72, "MEYER SHALE: 4,159 ft TVD (MD=TVD)", u.find("4,159"))
u.add(74, marker_text + " TVD (MD=TVD)", marker_column)
u.single_borehole("One borehole is depicted", loc(1, 201, 120, 317, 735))

u.uncertain([2, 3, 4], "The source says Santa Fe Springs Unit, 811B, and API 040371671000; "
            "the screening log says Santa Fe, 811-B, and API 0403716710. The displayed "
            "source values are recorded; reconcile the formatting and identity differences.")
u.uncertain([13], "The 7 in string lists 23 without an explicit unit; it is treated as "
            "the string weight from its position between size and grade. Confirm.")
u.uncertain([17, 18, 28, 58, 59], "Only four lines labelled Perfs are counted as perforations. "
            "Test holes, inactive slots, and WSO are instead classified as other "
            "flow/integrity features; confirm this distinction.")
u.uncertain([20, 61], "WSO is shown at 4,343 ft, but the entry does not explicitly say "
            "water-shutoff holes. The dedicated hole points are MISSING; confirm.")
u.uncertain([33, 34, 67], "The 10.625 in hole is also described as scraped to 11 in "
            "from 4,343 to 4,402 ft. Both the section and the altered interval are listed.")
u.uncertain([38, 39, 40, 70, 71, 81, 82], "The two adjacent 10.625 in cement entries "
            "are treated as separate represented fills. The 4,343–4,402 ft entry lacks "
            "a job date/stage/name and sack count, so points 81 and 82 are MISSING. "
            "Confirm whether it belongs to the preceding 500-sack job. A separate Mud "
            "entry also says it was cemented with 85 sacks; confirm whether it represents "
            "an additional cement job rather than a mud entry.")
u.uncertain([41, 42], "Heavy mud is labelled in intervals that overlap cement-plug "
            "intervals; no fluid is explicitly identified as between plugs. These "
            "points are MISSING pending review, without judging the diagram's accuracy.")
u.uncertain([43, 44, 47, 48, 72, 74], "MEYER SHALE is counted as a formation; the "
            "UHZ, FOIX, BELL, and MEYER entries are counted as markers. Confirm which "
            "other named markers also qualify as formations or zones.")
u.uncertain([45, 46, 49, 50, 73, 75, 76], "The four perforation labels say Bell INJ, "
            "but do not explicitly label a zone name and separate injection-zone "
            "top/bottom entries. Those zone points are MISSING pending review.")
u.uncertain([53, 54, 55, 57, 58, 59, 67, 68, 69, 70, 71, 72, 74],
            "The source prominently states MD=TVD; each displayed depth is therefore "
            "also recorded for its separate TVD point. Confirm that this global equality "
            "satisfies the separate-TVD rule.")
u.uncertain([87, 88, 89], "MD=TVD is not an explicit vertical/straight statement or "
            "a directional survey, so wellbore-path MD, inclination, and azimuth "
            "remain MISSING. Confirm.")

u.add_excess("Well status", [
    ("status", "Injecting", u.find("Status: Injecting"),
     "Well status is not one of the scored points."),
])
u.add_excess("Perforation shot density", [
    (f"perforation {i + 1}", "4 SPF", u.find("4 SPF", occurrence=i),
     "Shot density is not a scored point.") for i in range(4)
])
u.add_excess("Test-hole shot counts", [
    ("test holes at 3,803 ft", "4 holes", u.find("Shot 4 holes"),
     "Shot count is not a scored point."),
    ("test holes at 3,947–3,951 ft", "8 holes", u.find("Shot 8 holes"),
     "Shot count is not a scored point."),
])
u.add_excess("Inactive-slot dates", [
    ("5.5 in slots", "12/30/1949–2/7/1955", u.find("12/30/1949 - 2/7/1955"),
     "Slot active dates are not scored."),
    ("5.5 in slots", "12/30/1949–6/9/1951", u.find("12/30/1949 - 6/9/1951"),
     "Slot active dates are not scored."),
    ("4 in slots", "6/10/1951–2/7/1955", u.find("6/10/1951 - 2/7/1955"),
     "Slot active dates are not scored."),
])
u.add_excess("Regulatory approvals", [
    (f"approval {i + 1}", "approved by DOGGR", u.find("Approved by DOGGR", occurrence=i),
     "An approval statement is not a scored data point.") for i in range(4)
])
u.add_excess("Mud types outside explicit plug gaps", [
    (f"heavy mud entry {i + 1}", "Heavy Mud", u.find("Heavy Mud", occurrence=i),
     "The entry is not explicitly identified as fluid between plugs.") for i in range(3)
])
u.uncertain([28, 38, 41], "Confirm the new excess categories well status, test-hole "
            "shot counts, slot dates, approvals, and mud entries outside explicit plug gaps.")
u.add_provenance("Preparer/reviewer", "LWillbanks", u.find("by LWillbanks"))
u.add_provenance("Review date", "3/3/2015", u.find("3/3/2015"))

if __name__ == "__main__":
    u.build()
