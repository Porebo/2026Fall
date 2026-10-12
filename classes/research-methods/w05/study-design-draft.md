# Study Design Assignment: Draft

## 1. Problem Description

Organizations are interested in using large language models (LLMs) to find and correct data-quality problems more quickly. However, an LLM may also make a plausible-looking change that is wrong, creating an error that is difficult to detect. This creates a practical problem for data-quality staff and their managers: they need evidence about whether AI-assisted remediation improves data quality, which prompting approaches are dependable, and how often AI introduces new errors. This study will evaluate the methods rather than assign blame to any person or organization.

## 2. Research Objectives and Questions

The objective of this study is to compare prompting strategies for specification-driven AI data cleaning. Each strategy will receive documented data-quality specifications and deliberately modified data, then be evaluated on its ability to identify specification violations and restore the data to a public California reference dataset. The strategies may include zero-shot, few-shot, role-based, and multistep prompts. The study will address the following questions:

1. To what extent do prompting strategies improve or worsen data-quality measures after AI intervention?
2. Which prompting strategy produces outputs with the highest agreement with the reference dataset and the fewest unintended changes?
3. How frequently do AI-generated corrections leave introduced errors unresolved or alter values that were originally correct?

Correction effectiveness will be assessed by measuring whether each AI output conforms to the specifications and how closely it matches the reference dataset. Measures will include the proportion of injected violations identified and correctly corrected, the number of violations remaining, and the number of originally conforming values changed incorrectly. Agreement with the reference measures effectiveness, not efficiency. If efficiency is also evaluated, I will measure it separately using indicators such as completion time or token use. I will define all measures and decision rules before testing.

## 3. Evidence and Data Needed

I will use only publicly available California oil-production data. I will not use data from my employer. I will identify the dataset, document its source and structure, and select a manageable sample. The original, unmodified sample will serve as the reference dataset for this experiment. I will treat its values as the expected target state while recognizing that the source may contain errors. Therefore, this study will measure agreement with the selected reference; it will not independently establish the real-world accuracy of every source value.

Following ISO 8000-61:2016, I will define data-quality errors as nonconformities with documented data requirements and assess quality control by checking whether the data meet those requirements (International Organization for Standardization, 2016). For this study, each injected error will be a deliberate violation of a written specification for a selected field or relationship. Depending on the structure of the selected dataset, specifications may cover required values, permitted formats or ranges, uniqueness, or relationships between fields or tables.

I will create a separate test copy of the reference sample and deliberately introduce a documented set of specification violations. The reference dataset will be kept separate and will not be provided to the AI prompts. It will provide the expected target for evaluating whether each AI output restores the test data. I will choose violations for which the specifications and information provided to the model make the required correction determinable. If a specification identifies a problem but does not determine a unique correction, the appropriate outcome will be to flag the issue or abstain rather than guess. I will retain the original sample, the modified test data, a change log linking each injected error to its specification, the prompts, the model outputs, and the evaluation results.

Before testing, I will define which errors to introduce and how to score them. I will assess dimensions such as accuracy, completeness, consistency, and validity when the selected fields and error types support those measures. For example, I will compare altered values with the reference to assess agreement, introduce verifiable missing values to assess completeness, and apply documented field rules or relationships to assess validity and consistency. I will not assume that every blank should be filled or that a value is incorrect merely because it is unusual.

## 4. Data-Collection Methods

I will create equivalent copies of the same modified test data and apply each prompting strategy to a copy. Each prompt will receive the same data-quality specifications, modified data, and task to identify violations and propose corrections. I will hold the model and version, input data, specifications, task, and other available settings constant so that the prompting strategy is the primary planned difference between conditions. The prompts will not receive the reference dataset. If feasible, I will repeat each condition and record variation across runs.

For each run, I will save the exact input, prompt, model output, proposed changes, and available explanation or audit information. I will compare each output with the reference dataset and the change log. I will record the errors corrected, errors remaining, incorrect changes to originally correct values, and any other new errors. I will also assess whether each change can be traced through the saved prompt and output. A model's confident explanation will not, by itself, establish that a correction is accurate.

## 5. Tentative Analysis Plan

First, I will document baseline conformance for the reference sample and the modified test data. I will then evaluate each AI output against both the specifications and the reference. For each prompting strategy and error type, I will report the number and proportion of injected violations identified, correctly corrected, and left unresolved, as well as originally conforming values changed incorrectly. I will also calculate field-level agreement with the reference and report results separately for each applicable data-quality dimension rather than relying only on an overall score. This will distinguish a model's ability to detect a violation from its ability to correct it accurately.

I will summarize the strategy comparisons by error type in tables and, if I conduct repeated runs, report variation across runs. If I evaluate efficiency as well as effectiveness, I will report completion time or token use separately from conformance and agreement with the reference. The findings will identify which strategies performed best on this sample and under these test conditions; they will not necessarily generalize to other datasets, organizations, or LLMs. I will discuss limitations, including the assumption that the public source is an appropriate reference, the specifications and violations selected, and the use of a single dataset.

## References

International Organization for Standardization. (2016). *Data quality—Part 61: Data quality management: Process reference model* (ISO 8000-61:2016).