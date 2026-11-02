# Statistical Problems – Answers

Principles of IQ (INFQ 7303) – Week 11

---

## Time Sample Data (n = 30)

10, 15, 11, 17, 22, 14, 23, 8, 15, 11, 16, 12, 19, 26, 12, 11, 9, 16, 15, 24, 12, 17, 16, 14, 19, 13, 11, 15, 13, 21

---

## Exercise 1 – Frequency Table, Histogram, Polygon, Skew

**Given:**

bin size = 4: width of each class interval

first bin starts at 7: lower limit of the first class

n = 30: number of workers in the sample

**Formulas:**

Relative frequency = frequency / n

Cumulative relative frequency = cumulative frequency / n

**Step 1: Count the values in each bin**

7–10: 8, 9, 10 → 3 values

11–14: 11 (×4), 12 (×3), 13 (×2), 14 (×2) → 11 values

15–18: 15 (×4), 16 (×3), 17 (×2) → 9 values

19–22: 19 (×2), 21, 22 → 4 values

23–26: 23, 24, 26 → 3 values

**Step 2: Apply the formulas**

Bin 7–10: 3 / 30 = 0.1000

Bin 11–14: 11 / 30 = 0.3667

Bin 15–18: 9 / 30 = 0.3000

Bin 19–22: 4 / 30 = 0.1333

Bin 23–26: 3 / 30 = 0.1000

**Frequency table**

| Class | Midpoint | Frequency | Cumulative Frequency | Relative Frequency | Cumulative Relative Frequency |
|---|---|---|---|---|---|
| 7–10 | 8.5 | 3 | 3 | 0.1000 | 0.1000 |
| 11–14 | 12.5 | 11 | 14 | 0.3667 | 0.4667 |
| 15–18 | 16.5 | 9 | 23 | 0.3000 | 0.7667 |
| 19–22 | 20.5 | 4 | 27 | 0.1333 | 0.9000 |
| 23–26 | 24.5 | 3 | 30 | 0.1000 | 1.0000 |
| **Total** | | **30** | | **1.0000** | |

**Histogram**

x-axis = class, y-axis = frequency:

```
Freq
11 |        ███
10 |        ███
 9 |        ███  ███
 8 |        ███  ███
 7 |        ███  ███
 6 |        ███  ███
 5 |        ███  ███
 4 |        ███  ███  ███
 3 |  ███   ███  ███  ███  ███
 2 |  ███   ███  ███  ███  ███
 1 |  ███   ███  ███  ███  ███
   +------------------------------
     7-10  11-14 15-18 19-22 23-26
```

To build the chart in Word: Insert > Chart > Column, using the Class and Frequency columns (set gap width to 0).

**Frequency polygon**

Plot frequency against class midpoint and join the points with straight lines. Add a point with frequency 0 at midpoints 4.5 and 28.5 so the polygon touches the axis at both ends.

| Midpoint | 4.5 | 8.5 | 12.5 | 16.5 | 20.5 | 24.5 | 28.5 |
|---|---|---|---|---|---|---|---|
| Frequency | 0 | 3 | 11 | 9 | 4 | 3 | 0 |

To build the chart in Word: Insert > Chart > Line with Markers, using the two rows above.

**Skewness**

Rule: if mean > median, the distribution is positively skewed (tail to the right).

Mean = 15.23, median = 15

15.23 > 15

**Answer: Positively skewed.** The peak is on the low side (11–14) and the long tail stretches to the right (up to 26).

---

## Exercise 2 – Descriptive Statistics

**Given:**

n = 30: number of workers in the sample

Σx = 457: sum of all 30 times

smallest value = 8: shortest time

largest value = 26: longest time

**Mean**

Formula: x̄ = Σx / n

Step 1: x̄ = 457 / 30

Step 2: x̄ = **15.23**

**Median**

Formula: the middle value of the ordered data; with n = 30 it is the average of the 15th and 16th values

Step 1: 15th value = 15, 16th value = 15

Step 2: Median = (15 + 15) / 2 = **15**

**Mode**

Formula: the value(s) that occur most often

Step 1: 11 appears 4 times, 15 appears 4 times, every other value appears 3 times or fewer

Step 2: Mode = **11 and 15** (bimodal)

**Range**

Formula: Range = maximum − minimum

Step 1: Range = 26 − 8

Step 2: Range = **18**

**Variance**

Formula: variance is the square of the standard deviation, s² = Σ(x − x̄)² / (n − 1)

Step 1: Σ(x − x̄)² = 603.37 (sum of the squared deviations from 15.23)

Step 2: s² = 603.37 / (30 − 1) = 603.37 / 29

Step 3: s² = **20.81**

**Standard deviation**

Formula: s = √( Σ(x − x̄)² / (n − 1) ), so s = √s²

Step 1: s = √20.81

Step 2: s = **4.56**

(If the 30 workers are treated as the whole population, divide by n instead: σ² = 603.37 / 30 = 20.11 and σ = √20.11 = 4.48.)

---

## Exercise 3 – Z-Scores

**Given:**

x̄ = 15.23: sample mean (Exercise 2)

s = 4.56: sample standard deviation (Exercise 2)

population is assumed normally distributed

**Formula:**

z = (x − μ) / σ, with the sample mean x̄ as the estimate of μ and the sample standard deviation s as the estimate of σ, so z = (x − x̄) / s

**Step 1: Apply the given in the formula (example, x = 8)**

z = (8 − 15.23) / 4.56

**Step 2: Continue solving**

z = −7.23 / 4.56

z = −1.59

The same steps are applied to every value:

| Time (sorted) | x − 15.23 | Z-score |
|---|---|---|
| 8 | -7.23 | -1.59 |
| 9 | -6.23 | -1.37 |
| 10 | -5.23 | -1.15 |
| 11 | -4.23 | -0.93 |
| 11 | -4.23 | -0.93 |
| 11 | -4.23 | -0.93 |
| 11 | -4.23 | -0.93 |
| 12 | -3.23 | -0.71 |
| 12 | -3.23 | -0.71 |
| 12 | -3.23 | -0.71 |
| 13 | -2.23 | -0.49 |
| 13 | -2.23 | -0.49 |
| 14 | -1.23 | -0.27 |
| 14 | -1.23 | -0.27 |
| 15 | -0.23 | -0.05 |
| 15 | -0.23 | -0.05 |
| 15 | -0.23 | -0.05 |
| 15 | -0.23 | -0.05 |
| 16 | 0.77 | 0.17 |
| 16 | 0.77 | 0.17 |
| 16 | 0.77 | 0.17 |
| 17 | 1.77 | 0.39 |
| 17 | 1.77 | 0.39 |
| 19 | 3.77 | 0.83 |
| 19 | 3.77 | 0.83 |
| 21 | 5.77 | 1.26 |
| 22 | 6.77 | 1.48 |
| 23 | 7.77 | 1.70 |
| 24 | 8.77 | 1.92 |
| 26 | 10.77 | 2.36 |

---

## Exercise 4 – Face Cards

**Given:**

52: number of cards in the deck

12: number of face cards (3 per suit × 4 suits)

cards are drawn without replacement, so the counts drop after each draw

### a) Three face cards

**Formula:**

A = first card is a face card, B = second card is a face card, C = third card is a face card

Product rule: P(A and B and C) = P(A) × P(B | A) × P(C | A and B)

**Step 1: Apply the given in the formula**

P(A and B and C) = (12 / 52) × (11 / 51) × (10 / 50)

**Step 2: Continue solving**

P(A and B and C) = 1,320 / 132,600

P(A and B and C) = **0.00995** (about 1%)

### b) Three face cards, all of the same suit

**Formula:**

Same as part (a), but after the first card the next two must come from the 2 remaining face cards of that suit.

**Step 1: Apply the given in the formula**

P(A and B and C) = (12 / 52) × (2 / 51) × (1 / 50)

**Step 2: Continue solving**

P(A and B and C) = 24 / 132,600

P(A and B and C) = **0.000181** (about 0.018%)

---

## Exercise 5 – Committee

**Given:**

8 female seniors: pool to choose from, choose 3

7 male seniors: pool to choose from, choose 2

order does not matter, so use combinations

**Formula:**

C(N, M) = N! / (M! × (N − M)!)

Committees = C(8, 3) × C(7, 2)

**Step 1: Apply the given in the formula**

C(8, 3) = 8! / (3! × 5!)

C(7, 2) = 7! / (2! × 5!)

**Step 2: Continue solving**

C(8, 3) = 40,320 / (6 × 120) = 56

C(7, 2) = 5,040 / (2 × 120) = 21

Committees = 56 × 21 = **1,176**

---

## Exercise 6 – Source A / Source B

**Given:**

P(A) = 0.70: probability a record came from Source A

P(B) = 0.30: probability a record came from Source B

P(correct | A) = 0.80: probability the name is correct, given the record is from Source A

P(correct | B) = 0.50: probability the name is correct, given the record is from Source B

### a) Probability the record came from Source B

**Formula:**

P(B) is given directly.

**Answer:**

P(B) = **0.30**

### b) Probability of a correct name

**Formula:**

P(correct) = P(correct | A) × P(A) + P(correct | B) × P(B)

**Step 1: Apply the given in the formula**

P(correct) = (0.80)(0.70) + (0.50)(0.30)

**Step 2: Continue solving**

P(correct) = 0.56 + 0.15

P(correct) = **0.71**

### c) Probability the record came from Source A, given a correct name

H = record is from Source A, ~H = record is from Source B, D = the name is correct

**Given (in this notation):**

P(H) = 0.70

P(~H) = 0.30

P(D | H) = 0.80

P(D | ~H) = 0.50

**Formula (Bayes' Theorem):**

P(H | D) = P(D | H) × P(H) / [ P(D | H) × P(H) + P(D | ~H) × P(~H) ]

**Step 1: Apply the given in the formula**

P(H | D) = (0.80)(0.70) / [ (0.80)(0.70) + (0.50)(0.30) ]

**Step 2: Continue solving**

P(H | D) = 0.56 / (0.56 + 0.15)

P(H | D) = 0.56 / 0.71

P(H | D) = **0.7887** (about 78.9%)

---

## Exercise 7 – Loan Default Screening (Bayes)

H = the loan defaults, ~H = the loan does not default, D = the test is positive

**Given:**

P(H) = 0.01: probability a loan defaults

P(~H) = 0.99: probability a loan does not default (1 − 0.01)

P(D | H) = 0.97: probability the test is positive, given the loan defaults

P(D | ~H) = 0.02: probability the test is positive, given the loan does not default (false positive)

**Formula (Bayes' Theorem):**

P(H | D) = P(D | H) × P(H) / [ P(D | H) × P(H) + P(D | ~H) × P(~H) ]

**Step 1: Apply the given in the formula**

P(H | D) = (0.97)(0.01) / [ (0.97)(0.01) + (0.02)(0.99) ]

**Step 2: Continue solving**

P(H | D) = 0.0097 / (0.0097 + 0.0198)

P(H | D) = 0.0097 / 0.0295

P(H | D) = **0.3288** (about 32.9%)

Even with a positive test, a loan is more likely not to default (about 67%), because defaults are rare (1%) and the 2% false-positive rate applies to the much larger group of non-defaulting loans.

---

## Exercise 8 – Overdue Accounts (Binomial, cumulative)

**Given:**

n = 8: number of accounts sampled (trials)

p = 0.15: probability an account is overdue (success)

1 − p = 0.85: probability an account is not overdue

s ≤ 2: no more than 2 overdue accounts (s = number of successes)

**Formula:**

P(X = s | p, n) = [ n! / (s! × (n − s)!) ] × p^s × (1 − p)^(n − s)

Cumulative: P(X ≤ 2) = P(X = 0) + P(X = 1) + P(X = 2)

**Step 1: Apply the given in the formula**

P(X = 0 | 0.15, 8) = [ 8! / (0! × 8!) ] × (0.15)^0 × (0.85)^8

P(X = 1 | 0.15, 8) = [ 8! / (1! × 7!) ] × (0.15)^1 × (0.85)^7

P(X = 2 | 0.15, 8) = [ 8! / (2! × 6!) ] × (0.15)^2 × (0.85)^6

**Step 2: Continue solving**

P(X = 0) = 1 × 1 × 0.2725 = 0.2725

P(X = 1) = 8 × 0.15 × 0.3206 = 0.3847

P(X = 2) = 28 × 0.0225 × 0.3771 = 0.2376

**Step 3: Add them up**

P(X ≤ 2) = 0.2725 + 0.3847 + 0.2376

P(X ≤ 2) = **0.8948** (about 89.5%)

Excel check: BINOM.DIST(2, 8, 0.15, TRUE) = 0.8948

---

## Exercise 9 – Survey Responses (Binomial)

**Given:**

n = 500: number of customers surveyed (trials)

p = 0.05: probability a customer completes the survey (success)

1 − p = 0.95: probability a customer does not complete the survey

n × p = 25: expected number of responses

### a) Exactly 20 respond

**Formula:**

P(X = s | p, n) = [ n! / (s! × (n − s)!) ] × p^s × (1 − p)^(n − s)

**Step 1: Apply the given in the formula**

P(X = 20 | 0.05, 500) = [ 500! / (20! × 480!) ] × (0.05)^20 × (0.95)^480

**Step 2: Continue solving** (500! is too large to evaluate by hand, so use Excel)

BINOM.DIST(20, 500, 0.05, FALSE) = **0.0516** (about 5.2%)

### b) At least 20 respond

**Formula:**

P(X ≥ 20) = 1.0 − P(X ≤ 19), where P(X ≤ 19) = BINOM.DIST(19, 500, 0.05, TRUE)

**Step 1: Apply the given in the formula**

P(X ≥ 20) = 1.0 − BINOM.DIST(19, 500, 0.05, TRUE)

**Step 2: Continue solving**

P(X ≥ 20) = 1.0 − 0.1272

P(X ≥ 20) = **0.8728** (about 87.3%)

---

## Exercise 10 – Normal Distribution

**Given:**

μ = 160: population mean

σ = 8: population standard deviation

**Formula:**

z = (x − μ) / σ

### a) P(X < 160)

**Step 1: Apply the given in the formula**

z = (160 − 160) / 8

**Step 2: Continue solving**

z = 0 / 8 = 0

P(X < 160) = P(Z < 0) = NORM.S.DIST(0) = **0.5000**

### b) P(X > 152)

**Step 1: Apply the given in the formula**

z = (152 − 160) / 8

**Step 2: Continue solving**

z = −8 / 8 = −1

P(Z > −1) = 1 − P(Z < −1) = 1 − NORM.S.DIST(−1)

P(Z > −1) = 1 − 0.1587

P(X > 152) = **0.8413**

### c) P(144 < X < 152)

**Step 1: Apply the given in the formula**

z₁ = (144 − 160) / 8

z₂ = (152 − 160) / 8

**Step 2: Continue solving**

z₁ = −16 / 8 = −2

z₂ = −8 / 8 = −1

P(−2 < Z < −1) = NORM.S.DIST(−1) − NORM.S.DIST(−2)

P(−2 < Z < −1) = 0.1587 − 0.0228

P(144 < X < 152) = **0.1359**

---

## Exercise 11 – Confidence Intervals

**Given:**

σ = 3: known population standard deviation (minutes)

x̄ = 12: sample mean (minutes)

n = 225 (first case) or n = 100 (second case): sample size

z = 1.96: critical value for 95% confidence

z = 1.645: critical value for 90% confidence

**Formula:**

CI = x̄ ± z × (σ / √n)

### Sample size 225

**Step 1: Standard error**

SE = 3 / √225 = 3 / 15 = 0.2

**95% confidence**

Step 1: Apply the given in the formula

CI = 12 ± 1.96 × 0.2

Step 2: Continue solving

CI = 12 ± 0.392

CI = **(11.61, 12.39)**

**90% confidence**

Step 1: Apply the given in the formula

CI = 12 ± 1.645 × 0.2

Step 2: Continue solving

CI = 12 ± 0.329

CI = **(11.67, 12.33)**

### Sample size 100

**Step 1: Standard error**

SE = 3 / √100 = 3 / 10 = 0.3

**95% confidence**

Step 1: Apply the given in the formula

CI = 12 ± 1.96 × 0.3

Step 2: Continue solving

CI = 12 ± 0.588

CI = **(11.41, 12.59)**

**90% confidence**

Step 1: Apply the given in the formula

CI = 12 ± 1.645 × 0.3

Step 2: Continue solving

CI = 12 ± 0.494

CI = **(11.51, 12.49)**

A smaller sample gives a wider interval, and a higher confidence level gives a wider interval.

---

## Exercise 12 – Hypothesis Test of Average A/R Balance

**Given:**

H0: μ = 755: claimed average A/R balance (null hypothesis)

Ha: μ ≠ 755: the average is different from the claim

n = 49: number of accounts sampled

x̄ = 730: sample mean

s = 58: sample standard deviation (used to estimate σ, since n ≥ 30)

IC = 1.96: interval coefficient for 95% confidence (5% significance level)

IC = 2.58: interval coefficient for 99% confidence (1% significance level)

**Formula:**

SE = s / √n

Critical values = μ ± IC × SE

Reject H0 if x̄ falls outside the critical values.

**Step 1: Standard error**

SE = 58 / √49

SE = 58 / 7

SE = 8.286

### a) 5% significance level

**Step 1: Apply the given in the formula**

Critical values = 755 ± 1.96 × 8.286

**Step 2: Continue solving**

Critical values = 755 ± 16.24

WC1 = 738.76 and WC2 = 771.24

x̄ = 730 is outside the interval (738.76, 771.24)

**Answer: Reject** the claim at the 5% level.

### b) 1% significance level

**Step 1: Apply the given in the formula**

Critical values = 755 ± 2.58 × 8.286

**Step 2: Continue solving**

Critical values = 755 ± 21.38

WC1 = 733.62 and WC2 = 776.38

x̄ = 730 is outside the interval (733.62, 776.38)

**Answer: Reject** the claim at the 1% level.

**Conclusion:** The auditor's claim that the average A/R balance is $755 should be rejected at both the 5% and the 1% significance levels.
