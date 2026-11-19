"""Reviewed source observations for U17; Lester must verify the draft calls."""

from u_atomic_common import Diagram, loc

u = Diagram("U17", "Sentinel Peak Resources California, LLC")
u.page_panel(1, (20, 20, 596, 787))
u.add(1, "Sentinel Peak Resources California, LLC", loc(1, 22, 25, 205, 34))
u.add(2, "Dome", loc(1, 22, 36, 48, 45))
u.add(3, "228", loc(1, 52, 36, 69, 45))
u.add(4, "0403063692", loc(1, 52, 47, 105, 56))
u.add(5, "4/25/2018", loc(1, 303, 47, 350, 56))
u.add(7, "KB 1,357.00 ft", loc(1, 334, 58, 386, 67))
u.add(8, "BFW N/A", loc(1, 302, 58, 319, 67))
u.add(10, "Conductor 14 in; intermediate 7 in; production liner 5 1/2 in",
      loc(1, 400, 110, 416, 119), loc(1, 400, 120, 416, 129),
      loc(1, 395, 130, 418, 139))
u.add(11, "Conductor Q-125; intermediate and liner K-55",
      loc(1, 548, 110, 577, 119), loc(1, 548, 120, 577, 129),
      loc(1, 548, 130, 577, 139))
u.add(13, "Conductor 115.50; intermediate 23.00; liner 17.00 lb/ft",
      loc(1, 507, 110, 534, 119), loc(1, 507, 120, 534, 129),
      loc(1, 507, 130, 534, 139))
u.add(14, "Conductor 90.0; intermediate 1,595.0; liner 1,756.0 ft MD",
      loc(1, 438, 110, 460, 119), loc(1, 437, 120, 464, 129),
      loc(1, 437, 130, 464, 139))
u.add(16, "Production liner top 1,572.0 ft MD", loc(1, 472, 130, 497, 139))
perfs = [loc(1, 396, 383, 431, 393), loc(1, 396, 401, 431, 411)]
u.add(17, "Semi-perf top 1,574; full-perf top 1,592 ft MD", *perfs)
u.add(18, "Semi-perf 1,574–1,584; full-perf 1,592–1,756 ft MD", *perfs)
u.add(28, "Gravel packs 1,574–1,592 and 1,592–1,756 ft",
      loc(1, 322, 281, 468, 291), loc(1, 322, 291, 468, 301))
hole_sections = [
    loc(1, 225, 163, 300, 184), loc(1, 225, 459, 300, 480),
    loc(1, 225, 645, 300, 666),
]
u.add(33, "Wellbore sections 20, 9 7/8, and 13 in", *hole_sections)
u.add(34, "Wellbore sections 10–90, 90–1,956, and 1,595–1,756 ft MD", *hole_sections)
u.add(35, "Plug - OH Cement", loc(1, 322, 227, 392, 238))
u.add(36, "Open-hole cement plug top 1,756.0 ft MD", loc(1, 382, 242, 408, 252))
u.add(37, "Open-hole cement plug bottom 1,956.0 ft MD", loc(1, 417, 242, 442, 252))
u.add(38, "Conductor Cement; Production Cement",
      loc(1, 322, 153, 387, 163), loc(1, 322, 182, 390, 192))
u.add(39, "Conductor and production cement tops 10.0 ft MD",
      loc(1, 383, 170, 403, 180), loc(1, 383, 199, 403, 209))
u.add(40, "Conductor cement bottom 90.0; production bottom 1,595.0 ft MD",
      loc(1, 420, 170, 441, 180), loc(1, 417, 199, 444, 209))
u.add(81, "Conductor Cement; Production Cement 5/4/2018; Plug - OH Cement 5/4/2018",
      loc(1, 322, 153, 387, 163), loc(1, 331, 199, 358, 209),
      loc(1, 331, 242, 358, 252))
u.add(88, "Directional", loc(1, 85, 84, 125, 93))
u.single_borehole("Original Hole", loc(1, 317, 25, 361, 35))

u.uncertain([6, 7, 8], "The KB elevation is explicit, but the datum height is not an "
            "absolute ground elevation. BFW N/A counts as an answer.")
u.uncertain([14, 16], "The casing table's set depths are treated as shoe depths, and "
            "the explicitly named production-liner top is 1,572 ft.")
u.uncertain([17, 18, 28], "The two slotted-liner intervals are explicitly described as "
            "Semi Perfs and Full Perfs, so the draft counts them as perforations. Both "
            "gravel packs are counted as other flow/integrity features; confirm.")
u.uncertain([33, 34], "The diagram shows three overlapping or adjacent wellbore sections "
            "with diameters 20, 9 7/8, and 13 in; all displayed values are retained.")
u.uncertain([81, 82, 83, 84, 85, 86], "Three jobs are identified by their names, though "
            "the conductor date is blank. Production and open-hole plug volumes are "
            "given, but conductor slurry details are blank; all repeated-job slurry "
            "points are MISSING. Cement returns are not treated as slurry volume.")
u.uncertain([88], "Directional is treated as an explicit deviation statement answering "
            "inclination only; the schematic does not provide a directional survey.")
u.uncertain([1, 10, 17, 33, 81], "The source page is scanned; evidence boxes and readings "
            "were checked visually. Confirm the manual transcription.")

u.add_excess("Well location", [
    ("field", "Midway Sunset", loc(1, 82, 58, 147, 67), "Field location is not scored."),
    ("PLSS", "Sec. 23, T. 31S, R. 22E, MD B&M", loc(1, 22, 69, 220, 78),
     "Location is not scored."),
])
u.add_excess("Well type", [
    ("type", "Producer", loc(1, 303, 36, 346, 45), "Well type is not scored."),
])
u.add_excess("Datum height", [
    ("datum", "10.00 ft", loc(1, 439, 58, 469, 67),
     "Height is not an explicit absolute ground elevation."),
])
u.add_excess("Completion date", [
    ("completion", "5/5/2018", loc(1, 388, 47, 426, 56),
     "Completion date is not a scored point."),
])
u.add_excess("Perforation and slot dates", [
    ("semi-perf", "5/5/2018", loc(1, 326, 383, 355, 393), "Date is not a scored point."),
    ("full-perf", "5/5/2018", loc(1, 326, 401, 355, 411), "Date is not a scored point."),
])
u.add_excess("Perforation status", [
    ("semi-perf", "Open", loc(1, 539, 383, 579, 399), "Status is not a scored point."),
    ("full-perf", "Open", loc(1, 539, 401, 579, 417), "Status is not a scored point."),
])
u.add_excess("Slot specifications", [
    ("full-perf", '0.040", 2"L, 6"C, 36R', loc(1, 481, 401, 531, 417),
     "Slot specifications are not separately scored."),
])
u.add_excess("Gravel-pack details", [
    ("first run date", "5/5/2018", loc(1, 376, 281, 411, 291), "Run date is not scored."),
    ("second run date", "5/5/2018", loc(1, 376, 291, 411, 301), "Run date is not scored."),
    ("first OD", "6.32 in", loc(1, 459, 281, 478, 291), "Pack OD is not scored."),
    ("second OD", "13 in", loc(1, 459, 291, 478, 301), "Pack OD is not scored."),
    ("gravel quantity", "189 cu ft of 8/16 gravel", loc(1, 482, 291, 585, 301),
     "Gravel quantity is not a scored point."),
])
u.add_excess("Plug-back / tag details", [
    ("date", "5/5/2018", loc(1, 322, 324, 356, 334), "Tag date is not scored."),
    ("PBTD", "1,756 ft", loc(1, 361, 324, 383, 334), "PBTD is not a cement-plug endpoint."),
    ("method", "Liner Shoe", loc(1, 400, 324, 433, 334), "Tag method is not scored."),
    ("type", "Casing Shoe", loc(1, 438, 324, 464, 344), "Tag type is not scored."),
])
u.add_excess("Cement-top measurement methods", [
    ("conductor", "Visual", loc(1, 464, 170, 484, 180), "Top method is not scored."),
    ("production", "Visual", loc(1, 464, 199, 484, 209), "Top method is not scored."),
    ("OH plug", "Tagged", loc(1, 464, 242, 484, 252), "Top method is not scored."),
])
u.add_excess("Cement returns", [
    ("production", "15 bbls cement to surface", loc(1, 486, 204, 586, 219),
     "Return volume is not slurry volume."),
])
u.uncertain([28, 38], "Confirm the new excess categories well type, slot specifications, "
            "gravel-pack details, tag details, and cement-top measurement methods.")
u.add_provenance("Drawing timestamp", "1/9/2019 2:43:30 PM", loc(1, 165, 84, 255, 93))

if __name__ == "__main__":
    u.build()
