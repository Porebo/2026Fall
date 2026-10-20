# Midterm Review: Information Quality

## Support Documents

### Lecture Slides and Supporting Materials

Files are collected in the [Lecture Slides folder](Lecture%20Slides/) and named to match the Blackboard lecture list.

- [Program Overview.pdf](Lecture%20Slides/Program%20Overview.pdf)
- [Course Overview Fall 2026.pdf](Lecture%20Slides/Course%20Overview%20Fall%202026.pdf)
- [IQ Principles and Domains.pdf](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf)
- [IQ Value and Business Impact.pdf](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf)
- [(F1) IQ History.pdf](Lecture%20Slides/%28F1%29%20IQ%20History.pdf)
- [ISO 8000-61 DQM.pdf](Lecture%20Slides/ISO%208000-61%20DQM.pdf)
- [(H) IQ Data Governance.pdf](Lecture%20Slides/%28H%29%20IQ%20Data%20Governance.pdf)
- [(S1) Statistics Descriptive.pdf](Lecture%20Slides/%28S1%29%20Statistics%20Descriptive.pdf)
- [ECCMA_20261015_UALR-Guest lecture 2026-10-15.pdf](Lecture%20Slides/ECCMA_20261015_UALR-Guest%20lecture%202026-10-15.pdf)

**ISO sources:** The actual 61-page ISO 8000-61 lecture deck was recovered from GitHub during synchronization. The separately supplied 29-page standards document is preserved as [ISO 8000-61 supplied reference.pdf](documents/ISO%208000-61%20supplied%20reference.pdf). These are distinct sources.

### Class Notes

- [August 27 — IQ Principles and Domains](w01/2026-08-27.html)
- [September 1 — Information Quality Value and Business Impact](w02/2026-09-01.html)
- [September 3 — Data Categories, Requirements, and Data Exploration](w02/2026-09-03.html)
- [September 8 — Quality Management and Information Products](w03/2026-09-08.html)
- [September 10 — Data Quality Management and ISO 8000-61](w03/2026-09-10.html)
- [September 15 — Data Quality Dimensions and Profiling](w04/2026-09-15.html)

### Textbook

- [Journey to Data Quality, Chapter 1](../Books/Journey%20to%20Data%20Quality-%20Ch_01.html)
- [Journey to Data Quality, Chapter 3](../Books/Journey%20to%20Data%20Quality-%20Ch_03%20standalone.html)
- [Journey to Data Quality, full textbook PDF](../Books/Journey%20to%20Data%20Quality-%20Textbook.pdf)

### Answer Validation

Reviewed against the available local sources on October 20, 2026. Each answer below includes a source and a validation label:

- **Supported:** directly supported by the cited content, or calculated from its formula.
- **Qualified:** the content supports the idea, but not the exact wording or full claim.
- **Corrected:** the saved answer or terminology has been changed to match the source; the original is noted.
- **Unresolved:** the available content does not establish the requested answer.

PDF links use `#page=` for the PDF viewer's page number, not the document's printed page number. Class-note links open the relevant section. These are study-source checks, not an official answer key: the 50/60 score alone cannot identify which answers were marked wrong, and missing questions cannot be reconstructed. The statistics slides remain in the source collection, but none of the saved questions directly tests their statistics topics.

**Review summary:** 41 supported answers (including source-specific or conceptual support), 6 qualified answers (Q5, Q6, Q7, Q44, Q45, Q52), 2 corrected answers or terms (Q23, Q38), and 3 unresolved answers (Q1, Q14, Q50).

## Information quality principles and evolution

1. **Which word is most important in the UALR definition of information quality: product, value, customer, or accuracy?**  
   Customer.

   **Unresolved.** [IQ Principles and Domains, PDF p. 3](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=3) defines IQ in terms of maximizing value, minimizing risk, and creating value for users. [PDF p. 21](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=21) emphasizes consumer needs, but neither page calls "customer" the most important word. Retain this only as the recorded answer, not a verified one; the definition also makes "value" a plausible candidate.

2. **Which quality pioneer is best known for the “Seven Deadly Sins”?**  
   W. Edwards Deming.

   **Supported.** [(F1) IQ History, PDF pp. 7 and 9](Lecture%20Slides/%28F1%29%20IQ%20History.pdf#page=7) explicitly attributes "7 Deadly Sins of Management" to Deming and lists them. The earlier concern about "Sins" versus "Diseases" does not apply to the wording used in this class deck.

3. **What does the first principle of information quality tell us?**  
   Data is a resource for creating value; data collected, processed, and formatted for a particular use becomes an information product or service.

   **Supported.** [IQ Principles and Domains, PDF p. 13](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=13), "Information Quality Principle #1," directly states both ideas.

4. **In the evolution of information quality, MIT TDQM was part of which phase?**  
   The information product and process management (product management) phase.

   **Supported.** [IQ Principles and Domains, PDF p. 7](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=7) labels this phase "Information Product & Process Management" and places the TDQM product perspective there.

5. **Which phase brought enterprise architecture planning into the evolution of information quality?**  
   The information-as-an-organizational-asset (enterprise architecture) phase.

   **Qualified.** [IQ Principles and Domains, PDF p. 9](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=9) supports the enterprise-asset interpretation. However, [PDF p. 8](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=8) separately names an "Information Architecture View: The Quality by Design Phase." Without the original choices, distinguish enterprise-wide asset management (p. 9) from information architecture design (p. 8); the wording saved here does not conclusively select between them.

6. **What is the current phase in the evolution of information quality, according to the class notes?**  
   The interoperability phase.

   **Qualified.** The [August 27 notes, Evolution of Information Quality](w01/2026-08-27.html#history-heading) call this the interoperability phase. [IQ Principles and Domains, PDF p. 10](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=10) presents shared standards, interoperability, and portability under "What's Next?" Thus the notes support the answer, but the slide frames it as the next development rather than explicitly the current phase.

7. **Which proposed future development best fits the class discussion of interoperability?**  
   Shared data governance across independent but cooperating enterprises.

   **Qualified.** [IQ Principles and Domains, PDF p. 10](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=10) shows multiple enterprises connected through shared standards, data interoperability, and data portability. Shared cross-enterprise governance is a reasonable inference, not the specific wording stated on the slide.

8. **When does information produce value?**  
   When it is used to achieve a purpose.

   **Supported.** [IQ Principles and Domains, PDF p. 19](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=19), Principle #3, states that information can only produce value when used for some purpose.

9. **What is data processed and organized for a specific application or use called?**  
   An information product.

   **Supported.** [IQ Principles and Domains, PDF p. 19](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=19) defines data transformed and organized for use in an application as an information product.

10. **Understanding information-consumer needs is most closely associated with which principle?**  
    Information should be managed as a product.

    **Supported.** [IQ Principles and Domains, PDF pp. 20 and 21](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=20) connects Principle #4 with understanding information-consumer needs as the first product-management practice.

11. **How does the information-quality-versus-data-quality principle distinguish the two?**  
    Data quality is measured by conformance to data requirements; information quality focuses more broadly on value.

    **Supported.** [IQ Principles and Domains, PDF pp. 22 and 23](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=22) contrasts inward-looking conformance measures with outward-looking value measures.

12. **Which principle is most closely associated with data stewardship?**  
    Information is an organizational asset requiring governance.

    **Supported.** [IQ Principles and Domains, PDF p. 17](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=17) states Principle #2. [(H) IQ Data Governance, PDF p. 8](Lecture%20Slides/%28H%29%20IQ%20Data%20Governance.pdf#page=8) explicitly ties stewardship to recognition of information as an organizational asset.

13. **How many dimensions and categories are in the Wang and Strong framework?**  
    16 dimensions in 4 categories.

    **Supported.** [IQ Principles and Domains, PDF p. 28](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=28) lists 16 dimensions under Intrinsic, Contextual, Representational, and Accessibility.

14. **Which is the most important Wang and Strong dimension among timeliness, completeness, accessibility, and accuracy?**  
    Accuracy was offered as a best guess, but the class notes do not identify any one dimension as most important.

    **Unresolved.** [IQ Principles and Domains, PDF p. 28](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=28) lists the dimensions without ranking them. The [September 15 notes, Dimensional Frameworks](w04/2026-09-15.html#frameworks-heading) emphasize thinking beyond accuracy rather than naming a universally most important dimension. The saved guess cannot be confirmed as the exam answer.

## Business value, business cases, and governance

15. **In the bottom-up search for business value, what do you start with?**  
    A data quality assessment.

    **Supported.** [IQ Value and Business Impact, PDF p. 3](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=3) shows a path beginning with data quality assessment, discovering an issue, and determining whether it causes a business problem.

16. **What is a main reason for building a business case for a data-quality improvement project?**  
    To justify the resources necessary for success and gain management support.

    **Supported.** [IQ Value and Business Impact, PDF p. 17](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=17), "The Importance of a Business Case," directly lists both purposes.

17. **What should a business case for information-quality improvement connect the project to?**  
    Organizational goals and objectives.

    **Supported.** [IQ Value and Business Impact, PDF p. 18](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=18), "Align with Business Goals," requires a clear connection between IQ improvement and achieving business goals and objectives.

18. **What dimensions are used in the cost-benefit matrix for comparing improvement opportunities?**  
    Cost versus benefit.

    **Supported.** [IQ Value and Business Impact, PDF p. 21](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=21) explicitly labels the two axes COST and BENEFIT.

19. **If a project costs $80,000 and is expected to produce $100,000 in benefits, what is its ROI?**  
    25%.

    **Supported.** Applying the ROI formula in [IQ Value and Business Impact, PDF p. 7](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=7): `100 * (100,000 - 80,000) / 80,000 = 25%`. This is simple ROI; no time horizon or discount rate is supplied in the saved question.

20. **What is data governance?**  
    A framework of roles, responsibilities, and rules for making decisions about data management in an organization.

    **Supported.** [(H) IQ Data Governance, PDF p. 4](Lecture%20Slides/%28H%29%20IQ%20Data%20Governance.pdf#page=4) gives this definition and distinguishes the decision-making structure from management decisions themselves.

21. **When establishing a data governance program, what are the first two steps in the provided choices?**  
    Define the mission and decide on an initial focus.

    **Supported.** [(H) IQ Data Governance, PDF p. 9](Lecture%20Slides/%28H%29%20IQ%20Data%20Governance.pdf#page=9), "Setting Up a Program," starts with these two bullets. This was previously unverified before the deck was added.

22. **Which data-governance structure statement was selected as correct?**  
    The data governance council reports directly to the executive committee.

    **Supported in the depicted model.** The organization chart in [(H) IQ Data Governance, PDF p. 11](Lecture%20Slides/%28H%29%20IQ%20Data%20Governance.pdf#page=11) places the Data Governance Council immediately below the Executive Committee. This supports the selected hierarchy, not a requirement that every organization use it.

23. **The concept that data is an organizational asset and no one person or group owns and controls it was identified as what?**  
    Data stewardship.

    **Corrected.** The saved answer was "Data policy." [(H) IQ Data Governance, PDF p. 8](Lecture%20Slides/%28H%29%20IQ%20Data%20Governance.pdf#page=8), titled "Data Stewardship," explicitly says information is an organizational asset and no person, department, or group owns the data; they are its caretakers on behalf of the organization. This directly matches the question and supersedes the earlier review correction.

## Data categories, requirements, and standards

24. **What category describes the people, places, and things critical to an organization?**  
    Master data.

    **Supported.** [IQ Value and Business Impact, PDF p. 44](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=44) defines master data as describing people, places, and things critical to the organization.

25. **What category labels, describes, or characterizes other data to help people retrieve, interpret, and use it?**  
    Metadata.

    **Supported.** [IQ Value and Business Impact, PDF p. 47](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=47) says metadata labels, describes, or characterizes other data to make it easier to retrieve, interpret, or use.

26. **What category of data has formal syntax and is directly machine-readable?**  
    Structured data.

    **Supported.** [IQ Value and Business Impact, PDF p. 40](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=40) lists direct machine readability and formal syntax as its characteristics.

27. **What does it mean for an asset to be fungible?**  
    It is interchangeable with another equivalent asset.

    **Supported.** [IQ Value and Business Impact, PDF p. 36](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=36) defines fungible assets as interchangeable and contrasts them with non-fungible information about identifiable entities.

28. **What are authoritative rules and guidelines for naming data, defining it, establishing valid values, and specifying business rules called?**  
    Data standards.

    **Supported.** [IQ Value and Business Impact, PDF p. 53](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=53) lists naming, defining, formatting, establishing valid values, and specifying business rules as the scope of data standards.

29. **What are data quality requirements commonly expressed in?**  
    Data quality dimensions.

    **Supported.** [IQ Principles and Domains, PDF p. 28](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=28), Principle #7, says data dimensions can be used to express data requirements.

30. **Data specifications, data decay, and transactability are dimensions in which framework?**  
    McGilvray’s data quality framework.

    **Supported by class notes.** The [September 15 notes, Dimensional Frameworks](w04/2026-09-15.html#frameworks-heading) explicitly puts data specifications, data decay, and transactability in McGilvray's 12-dimension framework. This citation is to the notes, not to a corresponding slide in the collected decks.

31. **According to ISO 8000-61, what are the three major parts of the data quality management reference model?**  
    The implementation process, data-related support processes, and resource provisioning.

    **Supported.** [ISO 8000-61 DQM lecture deck, PDF p. 8](Lecture%20Slides/ISO%208000-61%20DQM.pdf#page=8) names Implementation, Data-Related Support, and Resource Provisioning. The [standards reference, PDF pp. 8 and 9, clause 5.1 and Figure 1](documents/ISO%208000-61%20supplied%20reference.pdf#page=8) gives the same three-part structure.

32. **What are the four parts of the ISO 8000-61 implementation process?**  
    Data quality planning and requirements, data quality control, data quality assurance, and data quality analysis and improvement.

    **Supported by the recovered lecture deck.** [ISO 8000-61 DQM, PDF p. 9](Lecture%20Slides/ISO%208000-61%20DQM.pdf#page=9) uses these four labels. This supersedes the earlier terminology correction based only on the [standards reference, PDF pp. 9 and 10, clause 5.2](documents/ISO%208000-61%20supplied%20reference.pdf#page=9), whose shorter formal labels are Data Quality Planning, Control, Assurance, and Improvement. The original "planning and requirements" wording was appropriate for the class slide.

## POSMAD and data quality concepts

33. **In POSMAD, what does A stand for?**  
    Apply.

    **Supported.** [IQ Value and Business Impact, PDF p. 26](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=26) expands POSMAD, including "Apply the information to accomplish your goals."

34. **Cleaning, deduplicating, and enhancing data occur in which POSMAD phase?**  
    Maintain.

    **Supported.** [IQ Value and Business Impact, PDF p. 31](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=31), "Maintain Life-Cycle Activities," lists cleansing, enhancement, de-duplication, linking, and merging.

35. **Understanding limitations and restrictions on data use occurs in which POSMAD phase?**  
    Plan.

    **Supported.** [IQ Value and Business Impact, PDF p. 28](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=28), "Plan Life-Cycle Activities," explicitly includes understanding limitations and restrictions on data use.

36. **What are the four parts of the full context of a data quality issue?**  
    Data, people, process, and technology.

    **Supported.** [IQ Value and Business Impact, PDF p. 19](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=19), "Understand the Full IQ Context," lists these four components.

37. **What is the process of determining whether data values fall within the expected domain called?**  
    Validity (validation).

    **Supported by class notes.** The [September 15 notes, Validity Is Not Accuracy](w04/2026-09-15.html#validity-heading) describes range, reasonable-combination, set-membership, and dependency checks. Validation establishes conformance to allowed values or rules, not factual accuracy.

38. **What dimension describes expressing values for the same attribute in the same format and with the same meaning?**  
    Representational consistency (consistent representation).

    **Corrected terminology.** [IQ Principles and Domains, PDF p. 28](Lecture%20Slides/IQ%20Principles%20and%20Domains.pdf#page=28) uses the formal label "Representational consistency." The [September 15 notes, Data Standardization](w04/2026-09-15.html#standardization-heading) discusses standardizing representations. The saved wording conveyed the concept but was not the slide's exact dimension name.

39. **What are the four forms of missing data values?**  
    Null, empty, blank, and placeholder.

    **Supported by class notes.** The [September 15 notes, Missing Values](w04/2026-09-15.html#missing-heading) lists and distinguishes these four forms.

40. **Which date format meets the ISO calendar-date standard?**  
    YYYY-MM-DD (for example, 2014-06-16). The dotted option is not the format specified in class.

    **Supported by class notes.** The [September 15 notes, Action Items](w04/2026-09-15.html#action-items-heading) explicitly asks students to adopt `YYYY-MM-DD` as the ISO date format. This verifies the format taught in class; the original dotted answer choice is not saved here for comparison.

## Data profiling and completeness

41. **What are the three dimensions of data profiling analysis?**  
    Column analysis, dependency profiling within a table, and cross-table relationships.

    **Supported by class notes.** The [September 15 notes, Three-Dimensional Analysis](w04/2026-09-15.html#profiling-heading) lists column analysis (linear), dependency profiling (planar), and cross-table relationships (three-dimensional).

42. **Which profiling task is most suited to column profiling?**  
    Determining the percentage of null values.

    **Supported by class notes.** The [September 15 notes, Three-Dimensional Analysis](w04/2026-09-15.html#profiling-heading) explicitly includes null and blank counts and percentages in column analysis.

43. **What is counting the frequency of strings with a pattern such as “999Aaa As” called?**  
    Character pattern analysis.

    **Supported in concept.** The [September 15 notes, Three-Dimensional Analysis](w04/2026-09-15.html#profiling-heading) describes counting the "frequency of unique patterns," using uppercase/lowercase string patterns as examples. This matches the operation described; "character pattern analysis" is not the exact label used in those notes.

44. **Which column-analysis task is closest to looking at maximum and minimum values, among the choices of redundancy, invalid values, cardinality, and referential integrity?**  
    Searching for invalid values. Maximum/minimum values can help identify outliers; the earlier answer of data redundancy was incorrect.

    **Qualified.** The [September 15 notes, Three-Dimensional Analysis](w04/2026-09-15.html#profiling-heading) includes largest and smallest values as outlier checks. The [validity section](w04/2026-09-15.html#validity-heading) explains range checks. Together they make invalid-value detection the closest saved choice, but an extreme value is not automatically invalid without a requirement it violates.

45. **Measuring whether every product has one and only one product-master record assesses what?**  
    Completeness in breadth of coverage.

    **Qualified.** The [September 15 notes, Breadth vs. Depth of Coverage](w04/2026-09-15.html#completeness-heading) supports checking that every product is represented. However, "one and only one" also tests uniqueness/non-duplication, addressed in [Duplication Depends on the Requirement](w04/2026-09-15.html#redundancy-heading). The saved answer captures the coverage aspect, not the entire statement.

## Additional review questions

46. **Which quality pioneer is known as the father of statistical process control?**  
    Walter Shewhart.

    **Supported.** [(F1) IQ History, PDF pp. 3 and 4](Lecture%20Slides/%28F1%29%20IQ%20History.pdf#page=3) names Shewhart and calls him the father of statistical process control.

47. **Which quality pioneer was a major contributor to the Toyota Production System?**  
    Shigeo Shingo.

    **Supported.** [(F1) IQ History, PDF pp. 23 and 24](Lecture%20Slides/%28F1%29%20IQ%20History.pdf#page=23) names Shingo and identifies him as a major contributor to the Toyota Production System.

48. **Who developed the quality trilogy of planning, control, and improvement?**  
    Joseph Juran.

    **Supported.** [(F1) IQ History, PDF pp. 11 and 12](Lecture%20Slides/%28F1%29%20IQ%20History.pdf#page=11) pairs Juran with the Quality Trilogy of planning, control, and improvement.

49. **Who wrote *Quality Is Free*?**  
    Philip Crosby.

    **Supported.** [(F1) IQ History, PDF pp. 18 and 19](Lecture%20Slides/%28F1%29%20IQ%20History.pdf#page=18) states that Crosby published *Quality Is Free* in 1979.

50. **In Chapter 3, what did the author describe as critical to all functions of management?**  
    Measurement.

    **Unresolved.** The saved question does not identify which book's Chapter 3 it means. [Journey to Data Quality, Chapter 3 opening, PDF p. 42 (printed p. 27)](../Books/Journey%20to%20Data%20Quality-%20Textbook.pdf#page=42) discusses assessing data quality for decision making, strategy, and performance, but the specific statement "critical to all functions of management" was not located. Do not treat "measurement" as verified without the original chapter or question context.

51. **Creating a compelling business case for information quality projects is a key strategy for what?**  
    Information quality improvement.

    **Supported.** [IQ Value and Business Impact, PDF p. 17](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=17) explicitly says a convincing business case is necessary for successful IQ improvement. [Journey to Data Quality, PDF p. 28 (printed p. 13)](../Books/Journey%20to%20Data%20Quality-%20Textbook.pdf#page=28) likewise explains the economic justification needed to sustain a data quality program.

52. **Authoritative principles or guidelines describing business interactions are best described as what?**  
    Business rules.

    **Qualified.** [IQ Value and Business Impact, PDF p. 48](Lecture%20Slides/IQ%20Value%20and%20Business%20Impact.pdf#page=48) connects business metadata to business terminology and rules. The [September 3 notes, Metadata, Catalogs, and Glossaries](w02/2026-09-03.html#metadata-heading) gives operational-rule examples. These support the concept, but neither supplies the exact "authoritative principles or guidelines describing business interactions" definition saved in this question.
