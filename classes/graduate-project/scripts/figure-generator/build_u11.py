"""Reviewed source observations for U11; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U11", "Sentinel Peak Resources California LLC")
u.page_panel(1, (20, 15, 596, 775))
u.add(1, "SENTINEL PEAK RESOURCES CALIFORNIA LLC",
      u.find("SENTINEL PEAK RESOURCES CALIFORNIA LLC"))
u.add(2, "WELPORT", u.find("WELPORT", occurrence=1))
u.add(3, "150", loc(1, 58.5, 28.7, 76.7, 39.2))
u.add(4, "0403069152", u.find("0403069152"))
u.add(5, "8/3/2021", u.find("8/3/2021"))
u.add(7, "KB: 704.00 ft", u.find("704.00ft"))
u.add(8, "BFW: N/A ft", u.find("BFW: N/A"))
u.add(10, "Conductor 14 in; surface 8 5/8 in; production liner 6 5/8 in",
      loc(1, 403.5, 103.7, 410.7, 110.9), u.find("8 5/8", occurrence=0),
      u.find("6 5/8", occurrence=0))
u.add(11, "Conductor: Unknown Grade; surface and production liner: K-55",
      loc(1, 560.1, 103.7, 589.1, 118.4),
      u.find("K-55", occurrence=0), u.find("K-55", occurrence=1))
u.add(14, "Conductor 54 ft; surface 891 ft; production liner 1,792 ft MD",
      u.find("54", occurrence=0), u.find("891", occurrence=0), u.find("1,792", occurrence=0))
u.add(16, "Production liner top 825.9 ft MD", u.find("825.9"))
perfs = [loc(1, 400.3, y, 435.6, y + 7.3) for y in (509.1, 535.0, 560.9, 578.9)]
u.add(17, "Semi-perf, full-perf, perf, and reperf tops: "
      "838; 848; 850; 870 ft MD", *perfs)
u.add(18, "Semi-perf 838–848; full-perf 848–1,789; perf 850–890; "
      "reperf 870–890 ft MD", *perfs)
u.add(28, "Gravel pack at 891–1,792 ft", u.find("Gravel Pack", occurrence=1))
holes = [
    loc(1, 226.0, 147.5, 304.6, 166.0),
    loc(1, 226.0, 293.7, 295.2, 312.0),
    loc(1, 226.0, 583.9, 300.2, 602.2),
]
u.add(33, "20, 11, and 14 in wellbore sections", *holes)
u.add(34, "Wellbore sections 14–54, 54–891, and 891–1,792 ft MD", *holes)
u.add(38, "Conductor Cement; Surface Cement",
      u.find("Conductor Cement"), u.find("Surface Cement"))
u.add(39, "Conductor top 14.0 ft; surface top 14.0 ft MD",
      u.find("14.0", occurrence=0), u.find("14.0", occurrence=1))
u.add(40, "Conductor bottom 54.0 ft; surface bottom 891.0 ft MD",
      u.find("54.0"), u.find("891.0"))
u.add(81, "Conductor Cement; Surface Cement (8/5/2021)",
      u.find("Conductor Cement"), u.find("Surface Cement"))
u.add(82, "Conductor: Unknown Mix/Volume; surface: 86 bbl, 168 sacks; "
      "tail 31.6 sacks", loc(1, 468.4, 177.1, 573.9, 191.8),
      u.find("86 BBLS"), u.find("31.6 sxs"))
u.add(88, "Directional", u.find("Directional"))
u.single_borehole("Original Hole", u.find("Original Hole", occurrence=0))

u.uncertain([6, 7], "The KB elevation is shown, but the datum height of 14 ft is not "
            "an explicit ground elevation. The draft does not calculate one.")
u.uncertain([8], "The explicit BFW N/A is an answer under the presence rule; "
            "it does not make the freshwater point NOT_APPLICABLE.")
u.uncertain([11, 13], "The conductor grade explicitly says Unknown Grade and is counted "
            "as an entry; its weight cell is blank, so repeated-string weight is MISSING. "
            "Confirm that Unknown Grade satisfies the explicit-entry rule.")
u.uncertain([14, 16], "The casing table's set depths are treated as shoe depths and "
            "its production-liner top as the liner top.")
u.uncertain([17, 18, 28], "The two slotted-liner intervals are explicitly described as "
            "Semi-Perf and Full-Perf, so they are included with the two lines labelled "
            "perf and reperf. The gravel pack is counted as another flow/integrity "
            "feature. Confirm both classifications.")
u.uncertain([28, 32], "Gravel Pack is treated as an other flow/integrity feature, not "
            "automatically as in-well equipment; no tubing or other equipment is "
            "explicitly listed as remaining in the well.")
u.uncertain([35, 36, 37], "The plug-back record specifies a liner shoe and the cement "
            "narrative mentions wiper plugs; neither is identified as a cement plug.")
u.uncertain([81, 82, 83, 84, 85, 86], "Conductor Cement and Surface Cement are used as "
            "job names. Conductor Unknown Mix/Volume is counted for slurry volume, but "
            "does not explicitly state density, yield, cement class, or additives; "
            "the corresponding repeated-job points are MISSING. Confirm.")
u.uncertain([88], "Directional is treated as an explicit deviation statement answering "
            "inclination only; there are no path stations or azimuth.")

u.add_excess("Well location", [
    ("field", "CYMRIC", u.find("CYMRIC"), "Field location is not a scored point."),
    ("PLSS", "Sec. 36, T. 29S, R. 21E", u.find("Sec. 36, T. 29S, R. 21E"),
     "Location is not a scored point."),
])
u.add_excess("Well type", [
    ("type", "Producer", u.find("Producer"), "Well type is not a scored point."),
])
u.add_excess("Datum height", [
    ("datum", "14 ft", u.find("Datum: 14ft"),
     "Datum height is not an explicit absolute ground elevation."),
])
u.add_excess("Completion date", [
    ("completion date", "9/7/2021", u.find("9/7/2021"), "Completion date is not scored."),
])
u.add_excess("Perforation and slot dates", [
    (f"interval {interval}", "8/7/2021", u.find("8/7/2021", occurrence=index + 2),
     "Perforation or slot date is not a scored point.")
    for index, interval in enumerate(("838–848", "848–1,789", "850–890", "870–890"))
])
u.add_excess("Perforation shot density", [
    (f"interval {interval}", "4.0 shots/ft", loc(1, 444.6, y, 453.7, y + 7.3),
     "Shot density is not a scored point.")
    for interval, y in (("850–890", 560.9), ("870–890", 578.9))
])
u.add_excess("Slot specifications", [
    ("semi-perf slots", '32R, 2"S, 6"C, 25M', loc(1, 487.8, 509.1, 529.5, 530.8),
     "Slot details are not separate scored points."),
    ("full-perf slots", '64R, 2"S, 6"C, 25M', loc(1, 487.8, 535.0, 529.5, 556.7),
     "Slot details are not separate scored points."),
])
u.add_excess("Perforation status", [
    (f"interval {interval}", "Open", u.find("Open", occurrence=index),
     "Open status is not a scored point.")
    for index, interval in enumerate(("838–848", "848–1,789", "850–890", "870–890"))
])
u.add_excess("Plug-back / tag details", [
    ("plug-back date", "8/7/2021", u.find("8/7/2021", occurrence=1),
     "Plug-back date is not a scored point."),
    ("plug-back depth", "1,792 ft MD", u.find("1,792", occurrence=2),
     "Plug-back depth is not a cement-plug endpoint."),
    ("tag method", "Tagged", u.find("Tagged"), "Tagging method is not a scored point."),
    ("tag type", "Liner Shoe", loc(1, 436.7, 453.6, 455.0, 468.1),
     "The tag type is not identified as a cement plug."),
])
u.add_excess("Cement-top measurement methods", [
    ("conductor", "Unknown Volumes", loc(1, 430.5, 177.1, 459.6, 191.8),
     "Top-measurement method is not a scored point."),
    ("surface", "Visual", u.find("Visual"), "Top-measurement method is not a scored point."),
])
u.add_excess("Cementing operational details", [
    (item, value, u.find(phrase), "The operation's fluid, pressure, or returns is not scored.")
    for item, value, phrase in [
        ("fresh-water preflush", "2 bbls", "2 bbls"),
        ("test pressure", "2500 psi", "2500 psi"),
        ("displacement water", "49.6 bbls", "49.6 bbls"),
        ("displacement pressure", "260 psi", "260 psi"),
        ("bump pressure", "570 psi", "570 psi"),
        ("cement returns", "40 bbls", "40 bbls"),
    ]
])
u.uncertain([28, 38], "Confirm the new excess categories well type, slot specifications, "
            "tag details, cement-top methods, and cementing operational details.")
u.add_provenance("Drawing timestamp", "12/8/2021 1:56:28 PM",
                 u.find("12/8/2021 1:56:28 PM"))

if __name__ == "__main__":
    u.build()
