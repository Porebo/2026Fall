Lester Carcamo  
Principles of Information Quality  
HW04 - JDQ 3 and 4 Review  
September 29, 2026

# HW04: JDQ 3 and 4 Review

All answers are based on *Journey to Data Quality*, Chapter 3 (Assessing Data Quality, Part I) and Chapter 4 (Assessing Data Quality, Part II). For the Chapter 4 problems, I used the metric formulas as they appear in the book and show each step of the calculation.

# Chapter 3: Assessing Data Quality, Part I

## 3.1 TDQM

### (a) What the letters in TDQM stand for

TDQM stands for **Total Data Quality Management**. The book describes it as the process-oriented cycle that grew out of MIT's Total Data Quality Management Research Program.

### (b) Steps in the TDQM process

The TDQM cycle consists of four steps: define, measure, analyze, and improve.

1. **Define.** The organization defines what data quality means for its data and context. In the data integrity approach, this step produces the data integrity rules.
2. **Measure.** The organization measures the quality of the data against the definition. The measurement may be a simple metric, such as the percentage of violations, or a more elaborate one, such as the difference between the data and the defined quality standard.
3. **Analyze.** The organization analyzes the underlying causes of the violations or discrepancies that the measurement found.
4. **Improve.** The organization produces and carries out a plan to bring the data into conformance with the defined quality standard.

## 3.2 The three steps of the Comparative Approach (Subjective and Objective Assessments)

The book also calls this the diagnostic approach. It compares the subjective assessment (the data quality survey) with the objective assessment (quantifiable data quality metrics). It has three steps:

1. **Perform the data quality survey and measure data quality using data quality metrics.** The organization first decides which data quality dimensions matter to it. It then collects survey assessments of those dimensions from the three stakeholder groups (data collectors, data custodians, and data consumers). It also measures the same dimensions as objectively as it can with quantitative metrics.
2. **Compare the results of the two assessments, identify discrepancies, and determine the root causes of the discrepancies.** The survey result and the metric result for each dimension are compared, and the outcome is placed on the 2 x 2 Diagnostic Matrix.
3. **Determine and take the necessary actions for improvement.** The corrective action depends on which quadrant the result falls in.

## 3.3 Quadrant II of the Diagnostic Matrix

### (a) What Quadrant II means

The Diagnostic Matrix crosses the survey (subjective) assessment with the metric (objective) assessment. The book's goal is Quadrant IV, where both assessments show high quality. It describes Quadrant III as the case where the metrics show high quality but the survey shows low quality. Quadrant I is therefore the case where both assessments are low. Quadrant II is the mirror image of Quadrant III: **the survey assessment is high, but the metric assessment is low.**

In other words, the stakeholders believe the data is good, but the objective measurement says it is not. The book says that any result in Quadrant I, II, or III requires the company to investigate the root cause of the discrepancy and take corrective action. For Quadrant II, likely explanations are that the respondents are not aware of the problems in the data, or that the metric is measuring something different from what the stakeholders are evaluating.

### (b) Example: Completeness of customer master data

- **Dimension:** Completeness (Wang-Strong Framework, intrinsic/contextual category).
- **Data type:** Customer master data, such as the customer address and email fields.
- **Survey result (high):** Sales staff, who are the data consumers, rate completeness as high. They look up a few well-known, active accounts, and those records are always fully filled in.
- **Metric result (low):** The completeness metric, `1 - (number of incomplete items / total number of items)`, is run across the whole table. Many older or inactive records have blank email or address values, so the score is low.
- **Why this is Quadrant II:** The consumers only see a small, non-representative part of the data. Because of that, they do not know about the missing values in the rest of the population. The corrective action is to find out which records are incomplete, share the metric results with the stakeholders, and fix or retire the incomplete records.

## 3.4 Two types of Gap Analyses

The Information Quality Assessment (IQA) survey measures quality at the dimension level. Two gap analyses can be done with its results.

1. **Benchmark gap analysis.** This compares the organization's information quality assessment against a benchmark, usually a best-practice organization. The book's example is the "data are easy to use" dimension, which compares four companies against benchmark company #1. The y-axis is the quality level (0 to 10), and the x-axis is the percentage of respondents who rated quality at that level. The book says to consider three indicators: the size of the gap area, the location of the gap, and the different-sized gaps over the x-axis. A large gap shows how much room there is to improve.
2. **Role gap analysis.** This compares the quality assessments of respondents in different organizational roles, such as information systems professionals versus information consumers. It is useful for determining whether differences between roles are a source of a benchmark gap. The three indicators are the size of the gap, the location of the gap, and the direction of the gap. The direction is positive when the information systems professionals rate quality higher than the consumers do. A large positive gap means that the professionals are not aware of problems the consumers experience, so the organization should work toward consensus between the two groups. If the gap is small, the location matters. A high location calls for incremental improvements, and a low location calls for major improvement efforts.

## 3.5 Steps in the "process-embedded data integrity" approach

This approach embeds data integrity rules into the TDQM cycle. The purpose is to keep the rules in line with the changing real-world states that the data represents. The steps are:

1. **Define.** The organization defines what data quality means for its data and context. This produces the data integrity rules.
2. **Measure.** The organization measures the data against the integrity rules, using a simple metric such as the percentage of violations, or a more elaborate one such as the difference between the data and the defined standard.
3. **Analyze.** The organization analyzes the underlying causes of the violations. This produces a plan to improve the data so that it conforms to the integrity rules.
4. **Improve and redefine the rules.** The organization carries out the improvement plan. It also **redefines the integrity rules when the supposed violations turn out to be valid data**. The book calls this redefinition "of the utmost importance" and says it makes the process more than simply iterative.

Chapter 4 illustrates this with the Glocom example. Its column integrity rule said the CASE_BK (cases booked) values must not be negative. The check found negative values. The data quality manager and the sales managers determined that the negatives were cancellations, so they added a new CASE_CNL field and moved the cancellations into it. The book's five activities for that example were identifying the problem, diagnosing the problem, planning the solution, implementing the solution, and reflecting and learning.

The result is that the use of data integrity tools is linked to organizational improvement processes. The book says this makes the integrity rules more visible, supports discussion of them, and helps communicate them across the organization.

# Chapter 4: Assessing Data Quality, Part II

## 4.1 Codd Integrity Constraints

Codd's integrity constraints are:

1. **Entity integrity.** No primary key value in a table may be null.
2. **Referential integrity.** The value of a foreign key must match a primary key value in the related table, or the foreign key must be null.
3. **Domain integrity.** The values in a column must come from the set of permissible values defined for that domain.
4. **Column integrity.** The values in a column must be drawn from the set of permissible values.
5. **Business rules.** This is Codd's all-purpose category for integrity rules specific to an organization.

The book says the metrics for the first four constraints are task-independent, because they reflect the state of the data without knowing the application. Business rules are the exception, since they depend on the organization.

The book lists the constraints in the order entity, referential, domain, and column integrity, and it gives metrics for entity, referential, and column integrity. It does not give a metric for domain integrity.

## 4.2 Free-of-error rating

Formula from the book:

$$
\text{Free-of-error rating} = 1 - \frac{\text{Number of data units in error}}{\text{Total number of data units}}
$$

Given: total data units = 12,500 and data units in error = 475.

- Step 1: Error ratio = 475 / 12,500 = 0.038
- Step 2: Rating = 1 - 0.038 = **0.962**

The Free-of-error rating is **0.962** (96.2%).

## 4.3 Appropriate-amount-of-data rating

Formula from the book:

$$
\text{Appropriate amount of data} = \min\left(\frac{\text{Number of data units provided}}{\text{Number of data units needed}},\ \frac{\text{Number of data units needed}}{\text{Number of data units provided}}\right)
$$

Given: provided = 1,600 and needed = 1,200.

- Step 1: Provided / needed = 1,600 / 1,200 = 1.3333
- Step 2: Needed / provided = 1,200 / 1,600 = 0.75
- Step 3: Rating = min(1.3333, 0.75) = **0.75**

The Appropriate-amount-of-data rating is **0.75**. The book says a working definition should reflect that the amount of data is neither too little nor too much. Here the data provided is more than needed, and the rating is penalized for that excess.

## 4.4 Timeliness rating

Formula from the book (Ballou et al., 1998):

$$
\text{Timeliness rating} = \left(\max\left(1 - \frac{\text{Currency}}{\text{Volatility}},\ 0\right)\right)^{s}
$$

Given: currency = 3 hours, volatility = 5 hours, and sensitivity s = 0.5.

- Step 1: Currency / volatility = 3 / 5 = 0.6
- Step 2: 1 - 0.6 = 0.4
- Step 3: max(0.4, 0) = 0.4
- Step 4: 0.4 raised to the power 0.5 = the square root of 0.4 = 0.6325

The Timeliness rating is **0.6325** (about 0.63).

Check against the book: the book states that a ratio of 0.19 gives 0.81 when s = 1, 0.49 when s = 2, and 0.9 when s = 0.5. My calculation follows the same pattern, because a sensitivity of 0.5 is less sensitive and gives a higher rating than s = 1 would (0.4).

## 4.5 Aggregate rating

The three ratings from the previous problems are:

| Dimension | Rating |
| --- | --- |
| Free-of-error (4.2) | 0.962 |
| Appropriate-amount-of-data (4.3) | 0.75 |
| Timeliness (4.4) | 0.6325 |

### (a) Weighted average

Formula from the book:

$$
\text{Rating} = \sum_{i=1}^{n} a_i M_i, \quad 0 \le a_i \le 1, \quad a_1 + a_2 + \dots + a_n = 1
$$

The weights are 0.30 (Free-of-error), 0.20 (Appropriate amount), and 0.50 (Timeliness). They sum to 1.00, so the formula's condition is satisfied.

- Free-of-error: 0.30 x 0.962 = 0.2886
- Appropriate amount: 0.20 x 0.75 = 0.1500
- Timeliness: 0.50 x 0.6325 = 0.3162 (using the unrounded 0.632456, the product is 0.316228)
- Sum: 0.2886 + 0.1500 + 0.3162 = 0.7548

The weighted-average aggregate rating is **0.755** (about 0.75).

### (b) Minimum

Formula from the book:

$$
\text{Rating} = \min(M_1, M_2, \dots, M_n)
$$

- min(0.962, 0.75, 0.6325) = **0.6325**

The minimum aggregate rating is **0.6325** (about 0.63), which is the Timeliness rating.

### Comparison of the two aggregates

The weighted average (0.755) is higher than the minimum (0.6325). The book describes the min operator as conservative: it gives a value no higher than the weakest indicator, so it shows that Timeliness is the limiting factor. The weighted average lets the strong Free-of-error rating (0.962) offset the weaker Timeliness rating, and it only makes sense if the organization understands how important each variable is. The book also warns that weighted averages can be misleading when the ratings are ordinal data rather than interval data. These three ratings come from ratio-style formulas, so that concern is smaller here.

# Summary of Numeric Answers

| Problem | Metric | Result |
| --- | --- | --- |
| 4.2 | Free-of-error | 0.962 |
| 4.3 | Appropriate-amount-of-data | 0.75 |
| 4.4 | Timeliness | 0.6325 |
| 4.5(a) | Weighted-average aggregate | 0.755 |
| 4.5(b) | Minimum aggregate | 0.6325 |
