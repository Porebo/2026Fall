# Study Design Assignment: Draft

## 1. Problem

Organizations are interested in using large language models (LLMs) to find and correct data-quality problems more quickly. However, an LLM may also make a plausible-looking change that is wrong, creating an error that is difficult to detect. This creates a practical problem for data-quality staff and their managers: they need evidence about whether AI-assisted remediation improves data quality, which prompting approaches are dependable, and how often AI introduces new errors. This study will evaluate the methods rather than assign blame to any person or organization.

## 2. Research objectives and questions

The objective of this study is to compare several prompting strategies for AI-assisted data cleaning and measure their effects on data quality. The strategies may include zero-shot, few-shot, role-based, and multi-step prompts. The study will address these questions:

1. To what extent do different prompting strategies improve or worsen data-quality measures after AI intervention?
2. Which prompting strategy produces the most reliable data-quality improvements?
3. How frequently do AI-generated corrections introduce new errors or reduce data quality?

For this study, reliability will mean that a strategy corrects known errors while making few or no incorrect changes to values that were already correct. The exact measures and decision rules will be defined before testing.

## 3. Evidence and data needed

I will use only publicly available oil-production data from the State of California, which may include related fact and dimension tables. I will not use data from my employer. A public dataset avoids exposing private business information and makes the study easier to reproduce. I will identify the specific public dataset and document its source before selecting the sample.

The dataset alone may not provide a dependable answer key for every value. Therefore, I will select a manageable sample and establish reference values using the original source records and documented business or data rules. Where necessary, I can create controlled test cases by introducing known errors into copies of valid records. This will let me distinguish a successful correction from a plausible but incorrect one. I will retain an unchanged baseline copy, the test cases, the prompts, model outputs, and the reference answers as evidence.

I will assess a defined set of dimensions, such as completeness, accuracy, consistency, and validity. Before testing, I will specify how each dimension is measured for the selected fields. For example, validity can be assessed against documented formats or permitted ranges; consistency can be assessed against relationships between fields or tables; accuracy can be assessed by comparison with the verified reference values. I will define completeness in a way that accounts for whether a missing value can actually be verified rather than assuming that every blank should be filled.

## 4. Data-collection methods

I will create a fixed sample of records and apply the same set of known data-quality problems to a copy of that sample. I will then run each selected prompting strategy against equivalent copies of the test data, keeping the model, model version, task instructions, and other available settings the same. This will help make the prompt strategy the main difference between conditions. If the model can produce different outputs on repeated runs, I will repeat the runs and record that variation.

For each run, I will save the input data, exact prompt, model output, proposed changes, and any explanation or audit information returned by the model. I will compare each proposed change with the reference values and rules. I will classify changes as correct corrections, incorrect changes, newly introduced errors, or unchanged values. I will also record whether each change can be traced through the saved prompt and output. No AI-generated change will be treated as correct solely because the model describes it confidently.

## 5. Tentative analysis plan

First, I will calculate the selected data-quality measures for the baseline dataset. Next, I will calculate the same measures for each AI-processed version and compare the results with both the baseline and the reference answers. I will report, for each prompting strategy, the number and proportion of known errors corrected, incorrect changes made, new errors introduced, and correct values left unchanged. I will also report changes in each selected quality dimension rather than relying only on one overall score.

I will summarize the results in tables so the prompting strategies can be compared directly. If I conduct repeated runs, I will report how much the outcomes vary between runs. The analysis will identify which strategies performed best on this sample and under these test conditions; it will not assume that the results automatically generalize to every dataset, organization, or LLM. I will also describe limitations, including the choice of dataset, the quality of the reference answers, and the fact that a public test dataset may not represent all workplace data-cleaning situations.