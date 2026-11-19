"""Reviewed source observations for U12; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U12", "Sentinel Peak Resources California LLC")
u.page_panel(1, (20, 15, 596, 775))
u.add(1, "SENTINEL PEAK RESOURCES CALIFORNIA LLC",
      u.find("SENTINEL PEAK RESOURCES CALIFORNIA LLC"))
u.add(2, "STAR FEE", u.find("STAR FEE", occurrence=1))
u.add(3, "H40-1", u.find("H40-1"))
u.add(4, "0403066907", u.find("0403066907"))
u.add(5, "3/25/2020", u.find("3/25/2020"))
u.add(7, "KB: 963.00 ft", u.find("963.00ft"))
u.add(8, "BFW: N/A ft", u.find("BFW: N/A"))
u.add(10, "Conductor 16 in; surface 10 3/4 in; intermediate 8 5/8 in; production 5 1/2 in",
      loc(1, 403.5, 97.2, 410.7, 104.4), u.find("10 3/4", occurrence=0),
      u.find("8 5/8", occurrence=0), u.find("5 1/2", occurrence=0))
u.add(14, "Conductor 94 ft; surface 360 ft; intermediate 1,305 ft; "
      "production 1,997 ft MD",
      u.find("94", occurrence=0), u.find("360", occurrence=0),
      u.find("1,305", occurrence=0), u.find("1,997", occurrence=0))
perf_ranges = [u.find(s) for s in ("1,430-1,450", "1,560-1,580", "1,690-1,710")]
u.add(17, "Perforation tops 1,430; 1,560; 1,690 ft MD", *perf_ranges)
u.add(18, "Perforations 1,430–1,450; 1,560–1,580; 1,690–1,710 ft MD", *perf_ranges)
u.add(26, "Broken-off cup assembly and tubing", u.find("Cup assembly broke off"),
      u.find("Tubing", occurrence=0))
u.add(27, "Broken tubing 1,590–1,680 ft MD", loc(1, 429.2, 612.0, 468.4, 619.2))
u.add(30, "Swell packer 1,274–1,276 ft", u.find("Packer", occurrence=0))
u.add(32, "Tubing 1,590–1,680 ft", u.find("Tubing", occurrence=0))
u.add(34, "Total depth 1,997.00 ftKB", loc(1, 273.7, 62.1, 324.1, 72.8))
u.add(35, "Plug-back type: Cement", loc(1, 436.7, 662.4, 459.2, 669.6))
u.add(36, "4/28/2022 cement plug top 1,460 ft MD", u.find("1,460", occurrence=0))
u.add(37, "4/28/2022 cement plug bottom 1,483 ft MD", u.find("1,483", occurrence=1))
cement_names = [u.find(name) for name in (
    "Conductor Cement", "Surface Cement", "Intermediate Cement", "Production Cement")]
cement_names += [u.find("Squeeze Cement", occurrence=0), u.find("Squeeze Cement", occurrence=1)]
u.add(38, "Conductor, surface, intermediate, production, and two squeeze cement entries",
      *cement_names)
cement_tops = [loc(1, 370.4, y, 377.6, y + 7.3)
               for y in (172.8, 223.9, 290.2, 348.5)]
cement_tops += [u.find("1,483", occurrence=0), u.find("1,460", occurrence=0)]
cement_bottoms = [loc(1, 397.4, y, 413.8, y + 7.3)
                  for y in (172.8, 223.9, 290.2, 348.5, 445.7, 542.9)]
u.add(39, "Cement tops: conductor 14; surface 14; intermediate 14; production 14; "
      "4/27 squeeze 1,483; 4/28 squeeze 1,460 ft MD", *cement_tops)
u.add(40, "Cement bottoms: conductor 94; surface 370; intermediate 1,305; "
      "production 1,997; 4/27 squeeze 1,955; 4/28 squeeze 1,483 ft MD",
      *cement_bottoms)
u.add(81, "Cement jobs: 3/1/2020; 3/26/2020; 3/28/2020; 3/29/2020; "
      "4/27/2022; 4/28/2022",
      u.find("3/1/2020"), u.find("3/26/2020"), u.find("3/28/2020", occurrence=0),
      u.find("3/29/2020", occurrence=0), u.find("4/27/2022", occurrence=0),
      u.find("4/28/2022", occurrence=0))
u.add(82, "Conductor Unknown Mix/Volume; surface 65 bbl; intermediate 110 bbl; "
      "production 70 bbl lead and 40 bbl tail; 4/27 squeeze 100 cu ft; "
      "4/28 squeeze 120 cu ft",
      loc(1, 468.4, 172.8, 572.0, 187.5), u.find("65BBLS"), u.find("110BBLS"),
      u.find("70BBLS"), u.find("40BBLS"), u.find("100cuft"), u.find("120cuft"))
u.add(88, "Directional", u.find("Directional"))
u.single_borehole("Original Hole", u.find("Original Hole", occurrence=0))

u.uncertain([6, 7, 8], "KB elevation is explicit, but the datum height does not explicitly "
            "state ground elevation. BFW N/A counts as an answer under the presence rule.")
u.uncertain([11, 13], "The conductor grade and weight cells are blank; values for the "
            "other three strings do not satisfy the repeated-string points.")
u.uncertain([14, 34], "Set depths are treated as shoe depths and the header TD as hole "
            "depth. No explicitly labelled hole diameters are given.")
u.uncertain([17, 18], "All three intervals shown on the schematic are included, including "
            "1,690–1,710 ft, which does not appear in the visible perforation table. "
            "For 1,560–1,580 ft, the schematic date differs from the table date.")
u.uncertain([26, 27, 32], "The Other in Hole table says a cup assembly broke off and "
            "describes tubing at 1,590–1,680 ft. It is counted as a fish and as other "
            "equipment; confirm the intended interpretation and extent.")
u.uncertain([35, 36, 37, 38, 39, 40], "The plug-back type is Cement, and the 4/28/2022 "
            "squeeze entry shows 1,460–1,483 ft on the same date as the 1,460-ft tag. "
            "The draft links those entries as the cement plug and also lists the squeeze "
            "among cement records; confirm that association and whether other squeeze "
            "entries represent additional plugs.")
u.uncertain([81, 82, 83, 84, 85, 86], "Six cement records have dates. The conductor "
            "explicitly says Unknown Mix/Volume, counted for volume; the other five "
            "give volumes. Conductor and/or squeeze entries lack separate slurry density, "
            "yield, class, or additives, so those repeated-job points are MISSING. "
            "The 14.5# mud is not treated as cement-slurry density.")
u.uncertain([88], "Directional is treated as an explicit deviation statement answering "
            "inclination only; no path stations or azimuth are shown.")

u.add_excess("Well location", [
    ("field", "CYMRIC", u.find("CYMRIC"), "Field location is not a scored point."),
    ("PLSS", "Sec. 7, T. 30S, R. 22E", u.find("Sec. 7, T. 30S, R. 22E"),
     "Location is not a scored point."),
])
u.add_excess("Well type", [
    ("type", "Producer", u.find("Producer"), "Well type is not a scored point."),
])
u.add_excess("Datum height", [
    ("datum", "14 ft", u.find("14.00ft"),
     "Datum height is not an explicit absolute ground elevation."),
])
u.add_excess("Rig release and completion dates", [
    ("rig release", "3/29/2020", u.find("3/29/2020", occurrence=1),
     "Rig release date is not a scored point."),
    ("completion", "4/30/2020", u.find("4/30/2020", occurrence=1),
     "Completion date is not a scored point."),
])
u.add_excess("Perforation dates", [
    ("1,430–1,450 ft", "4/29/2022", u.find("4/29/2022", occurrence=1),
     "Perforation date is not a scored point."),
    ("1,560–1,580 ft schematic", "4/27/2022", u.find("4/27/2022", occurrence=2),
     "Perforation date is not a scored point."),
    ("1,560–1,580 ft table", "4/30/2020", u.find("4/30/2020", occurrence=0),
     "Perforation date is not a scored point."),
    ("1,690–1,710 ft", "4/27/2022", u.find("4/27/2022", occurrence=1),
     "Perforation date is not a scored point."),
])
u.add_excess("Perforation shot density", [
    ("1,430–1,450 ft", "6.0 shots/ft", u.find("6.0"), "Shot density is not scored."),
    ("1,560–1,580 ft", "4.0 shots/ft", u.find("4.0", occurrence=0),
     "Shot density is not scored."),
])
u.add_excess("Perforation gun size", [
    ("1,430–1,450 ft", "2 in", loc(1, 473.5, 717.9, 477.1, 725.1),
     "Gun size is not a scored point."),
    ("1,560–1,580 ft", "3.3858 in", loc(1, 469.9, 735.9, 482.6, 750.6),
     "Gun size is not a scored point."),
])
u.add_excess("Perforation status", [
    ("1,430–1,450 ft", "Open", u.find("Open"), "Status is not a scored point."),
    ("1,560–1,580 ft", "Abandoned", u.find("Abandoned"), "Status is not a scored point."),
])
u.add_excess("Equipment run dates", [
    ("packer", "3/28/2020", u.find("3/28/2020", occurrence=1),
     "Equipment run date is not a scored point."),
    ("tubing", "2/18/2022", u.find("2/18/2022"),
     "Equipment run date is not a scored point."),
])
u.add_excess("Plug-back tag details", [
    ("tag date", "4/28/2022", u.find("4/28/2022", occurrence=1),
     "Tag date is not a scored point."),
    ("tag method", "Tagged", u.find("Tagged"), "Tagging method is not a scored point."),
])
u.add_excess("Cement-top measurement methods", [
    (name, "Visual", u.find("Visual", occurrence=i),
     "Top-measurement method is not a scored point.")
    for i, name in enumerate(("conductor", "surface", "intermediate", "production"))
])
u.add_excess("Cementing operational details", [
    ("surface returns", "25 bbl", u.find("25BBLS"), "Return volume is not slurry volume."),
    ("intermediate returns", "No Traces of Cement Returns",
     u.find("No Traces of Cement Returns"), "Return information is not a scored point."),
    ("production returns", "42 bbl", u.find("42BBLS"), "Return volume is not slurry volume."),
    ("kill mud", "14.5# mud", u.find("14.5# mud"), "Mud is not cement-slurry density."),
])
u.uncertain([26, 38], "Confirm the new excess categories well type, equipment run dates, "
            "tag method, cement-top methods, and cementing operational details.")
u.add_provenance("Drawing timestamp", "7/12/2022 10:39:21 AM",
                 u.find("7/12/2022 10:39:21 AM"))

if __name__ == "__main__":
    u.build()
