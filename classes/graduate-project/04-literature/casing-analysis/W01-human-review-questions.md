# W01 Human Review Questions

This checklist has **61 questions**, corresponding one-to-one with the 61 atomic
requirements stored in `spec_requirements`.

For every question, enter:

1. The value shown on W01, or **Not present**, or **Not applicable**.
2. The location on the diagram.
3. A short note when “not applicable” is used.

Repeat an interval-level answer for every occurrence in the diagram. Do not
combine separate casing strings, cement jobs, formations, or well features.

## (a) Casing-diagram data

### (a)(1) Well identity

1. **What operator name is shown?**  
   Answer: `________________`  
   Storage: `operators.operator_name`

2. **What lease name is shown?**  
   Answer: `________________`  
   Storage: `wells.lease_name`

3. **What well number is shown?**  
   Answer: `________________`  
   Storage: `wells.well_number`

4. **What API number is shown?**  
   Answer: `________________`  
   Storage: `wells.api_number`

### (a)(2) Spud date

5. **What spud date is shown?**  
   Answer: `________________`  
   Storage: `wells.spud_date`

### (a)(3) Ground elevation

6. **What ground elevation from sea level is shown, including the unit?**  
   Answer: `________________`  
   Storage: `wells.ground_elevation_ft`

### (a)(4) Reference elevation

7. **What reference elevation is shown, and is the reference a rig floor or Kelly bushing?**  
   Answer: `________________`  
   Storage: `wells.reference_elevation_ft` and `wells.reference_elevation_type`

### (a)(5)–(a)(6) Water-protection bases

8. **What is the depth of the base of freshwater?**  
   Answer: `________________`  
   Storage: `wells.base_freshwater_md_ft`

9. **What is the depth of the base of the lowermost USDW penetrated by the well?**  
   Answer: `________________`  
   Storage: `wells.base_usdw_md_ft`

### (a)(7) Casing specifications

For every casing string, answer questions 10–13:

10. **What is the casing size or outside diameter?**  
    Answers: `________________`  
    Storage: `casing_intervals.casing_diameter_in`

11. **What is the casing grade or schedule?**  
    Answers: `________________`  
    Storage: `casing_intervals.grade_or_schedule`

12. **What is the casing connection type?**  
    Answers: `________________`  
    Storage: `casing_intervals.connection_type`

13. **What is the casing weight, including the unit?**  
    Answers: `________________`  
    Storage: `casing_intervals.weight_ppf`

### (a)(8) Casing-set depths

14. **What depth is shown for each casing shoe?**  
    Answers: `________________`  
    Storage: `casing_intervals.bottom_md_ft` with `terminal_feature = 'SHOE'`

15. **What depth is shown for each casing stub, if any?**  
    Answers or applicability explanation: `________________`  
    Storage: `casing_intervals.bottom_md_ft` with `terminal_feature = 'STUB'`

16. **What depth is shown for each liner top, if any?**  
    Answers or applicability explanation: `________________`  
    Storage: `casing_intervals.top_md_ft` with `terminal_feature = 'LINER_TOP'`

### (a)(9) Flow and mechanical-integrity features

17. **What perforation depths are shown?**  
    Answers: `________________`  
    Storage: `perforation_intervals.top_md_ft` and `bottom_md_ft`

18. **What is the top and bottom of each perforation interval?**  
    Answers: `________________`  
    Storage: `perforation_intervals.top_md_ft` and `bottom_md_ft`

19. **Are open-hole completion intervals shown? Give the top and bottom of each.**  
    Answers or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'OPEN_HOLE_COMPLETION'`

20. **Are water-shutoff holes shown? Give the depth of each.**  
    Answers or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'WATER_SHUTOFF_HOLE'`

21. **Are cement ports shown? Give the depth of each.**  
    Answers or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'CEMENT_PORT'`

22. **Are cavity shots shown? Give the depth of each.**  
    Answers or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'CAVITY_SHOT'`

23. **Are casing cuts shown? Give the depth and extent of each.**  
    Answers or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'CUT'`

24. **Is any type of casing damage shown or described? What type?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features.description` with `feature_type = 'CASING_DAMAGE'`

25. **What is the extent of each identified casing-damage condition?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features.top_md_ft`, `bottom_md_ft`, and `description`

26. **Is junk or fish shown or described? What type?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features.description` with `feature_type = 'JUNK_OR_FISH'`

27. **What is the extent or depth range of each junk/fish condition?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features.top_md_ft`, `bottom_md_ft`, and `description`

28. **Is there any other feature that affects flow or may compromise mechanical integrity?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features.description` with `feature_type = 'OTHER_FLOW_OR_INTEGRITY_FEATURE'`

### (a)(10) Downhole equipment

29. **What subsurface safety-valve information is shown?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'SUBSURFACE_SAFETY_VALVE'`

30. **What packer information is shown?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'PACKER'`

31. **What gas-lift-mandrel information is shown?**  
    Answer or applicability explanation: `________________`  
    Storage: `well_features` with `feature_type = 'GAS_LIFT_MANDREL'`

### (a)(11) Drilled-hole intervals

For every drilled interval:

32. **What hole diameter is shown?**  
    Answers: `________________`  
    Storage: `drilled_intervals.hole_diameter_in`

33. **What top and bottom depths are shown for the drilled interval?**  
    Answers: `________________`  
    Storage: `drilled_intervals.top_md_ft` and `bottom_md_ft`

### (a)(12) Cement plugs inside casing

34. **What cement plugs inside casing are identified?**  
    Answers or applicability explanation: `________________`  
    Storage: `cement_placements` with `placement_type = 'INSIDE_CASING'`

35. **What is the top depth of each cement plug inside casing?**  
    Answers or applicability explanation: `________________`  
    Storage: `cement_placements.top_md_ft`

36. **What is the bottom depth of each cement plug inside casing?**  
    Answers or applicability explanation: `________________`  
    Storage: `cement_placements.bottom_md_ft`

### (a)(13) Cement behind casing

37. **What cement fill behind casing is identified?**  
    Answers: `________________`  
    Storage: `cement_placements` with `placement_type = 'BEHIND_CASING'`

38. **What is the top depth of each cement-fill interval?**  
    Answers: `________________`  
    Storage: `cement_placements.top_md_ft`

39. **What is the bottom depth of each cement-fill interval?**  
    Answers: `________________`  
    Storage: `cement_placements.bottom_md_ft`

### (a)(14) Fluid between cement plugs

40. **What type of fluid is shown between cement plugs?**  
    Answer or applicability explanation: `________________`  
    **Schema gap:** no `fluid_type` column currently exists.

41. **What is the density or weight of the fluid between plugs, including the unit?**  
    Answer or applicability explanation: `________________`  
    **Schema gap:** no `fluid_density` or `fluid_density_unit` columns currently exist.

### (a)(15) Geological and injection intervals

42. **What formation names are shown?**  
    Answers or applicability explanation: `________________`  
    Storage: `geological_features.feature_name` with `feature_class = 'FORMATION'`

43. **What depth or top/bottom interval is shown for each formation?**  
    Answers or applicability explanation: `________________`  
    Storage: `geological_features.top_md_ft` and `bottom_md_ft`

44. **What zone names are shown?**  
    Answers or applicability explanation: `________________`  
    Storage: `geological_features.feature_name` with `feature_class = 'ZONE'`

45. **What depth or top/bottom interval is shown for each zone?**  
    Answers or applicability explanation: `________________`  
    Storage: `geological_features.top_md_ft` and `bottom_md_ft`

46. **What geological marker names are shown?**  
    Answers: `________________`  
    Storage: `geological_features.feature_name` with `feature_class = 'MARKER'`

47. **What depth or top/bottom interval is shown for each marker?**  
    Answers: `________________`  
    Storage: `geological_features.top_md_ft` and `bottom_md_ft`

48. **What is the top of the underground-injection zone?**  
    Answer or applicability explanation: `________________`  
    Storage: `geological_features.top_md_ft` with `feature_class = 'INJECTION_ZONE'`

49. **What is the bottom of the underground-injection zone?**  
    Answer or applicability explanation: `________________`  
    Storage: `geological_features.bottom_md_ft` with `feature_class = 'INJECTION_ZONE'`

50. **What is the top of each confining layer?**  
    Answers or applicability explanation: `________________`  
    Storage: `geological_features.top_md_ft` with `feature_class = 'CONFINING_LAYER'`

51. **What is the bottom of each confining layer?**  
    Answers or applicability explanation: `________________`  
    Storage: `geological_features.bottom_md_ft` with `feature_class = 'CONFINING_LAYER'`

## (b) Supporting documentation

### (b)(1) Cement calculations

52. **What steps are shown for each cement-yield calculation?**  
    Answers: `________________`  
    **Schema gap:** `cement_jobs.calculation_steps` combines yield and other calculation steps; they cannot be distinguished one-to-one.

53. **What steps are shown for each other cement calculation performed?**  
    Answers: `________________`  
    **Schema gap:** the same `cement_jobs.calculation_steps` field is currently reused.

### (b)(2) Cement-slurry information

54. **What inputs and supporting information are shown for calculating slurry volume for each cement job?**  
    Answers: `________________`  
    Storage: `cement_jobs.cement_volume_cf` for the result; supporting inputs are not separately structured.

55. **What slurry density is shown for each cement job?**  
    Answers: `________________`  
    Storage: `cement_jobs.density_ppg`

56. **What slurry yield is shown for each cement job?**  
    Answers: `________________`  
    Storage: `cement_jobs.yield_cf_per_sack`

57. **What cement type is shown for each cement job?**  
    Answers: `________________`  
    Storage: `cement_components.component_name` for cement-type components, or `cement_jobs.remarks`

58. **What additives, quantities, and units are shown for each cement job?**  
    Answers: `________________`  
    Storage: `cement_components.component_name`, `quantity`, and `unit`

### (b)(3) Wellbore path

59. **What measured depths are shown along the wellbore path?**  
    Answers: `________________`  
    Storage: `borehole_surveys.md_ft`

60. **What inclination measurement is shown at each survey depth?**  
    Answers: `________________`  
    Storage: `borehole_surveys.inclination_deg`

61. **What azimuth measurement is shown at each survey depth?**  
    Answers: `________________`  
    Storage: `borehole_surveys.azimuth_deg`

## Cross-cutting checks

These checks are legal application rules rather than additional atomic data items:

- **(c)** Did the reviewer identify every original, redrilled, and sidetracked borehole?  
  Answer: `________________`
- **(d)** Does every required depth have both MD and TVD?  
  Answer: `________________`  
  **Schema gap:** only `borehole_surveys.tvd_ft` exists. The current interval tables do
  not have separate TVD columns.
- **(e)** Is W01 supplied as a graphical diagram or complete flat-file dataset?  
  Answer: `________________`  
  Storage: `diagrams.submission_format`

## Storage-validation conclusion

The current database can store the basic answers, but it is not yet
one-to-one with every possible answer:

1. Add `fluid_type` and fluid-density fields for `(a)(14)`.
2. Separate yield-calculation steps from other cement-calculation steps for `(b)(1)`.
3. Store slurry-calculation inputs separately from calculated volume.
4. Add TVD fields to every table containing regulatory depths, including drilled
   intervals, casing intervals, cement placements, perforations, geological
   features, downhole components, and well features.
5. Store explicit applicability reasons where “not applicable” differs from
   “not shown.” These can currently be placed in
   `diagram_requirement_results.explanation`.

