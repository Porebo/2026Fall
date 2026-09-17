Lester Carcamo  
Principles of Information Quality  
HW03 - Define Data Quality Requirements and Remediation Plan  
September 16, 2026

# HW03: Define Data Quality Requirements and Remediation Plan

## About Writing the Data Requirements

The data requirements were created based on my observations of the data sample. I identified the areas where requirements were needed to prevent data-quality errors and support the remediation of existing errors. I used AI to help write the atomic rules that I can later implement in a PowerShell script and to organize this document into a cohesive Markdown structure. I reviewed the resulting requirements to ensure that they accurately reflect the observed data problems and the needs of the final report.

I used a customer-centered perspective to design the data requirements. I read the business case and determined which data was important for producing the final report and which data was unnecessary. Based on this analysis, I decided that EMAIL was not needed for the customer's information product and should be excluded. Thinking from the customer's perspective gave me a different appreciation of the data because I was designing a product to meet the customer's needs rather than treating data quality itself as the product. This perspective helped me distinguish between data that is useful for the report and data that is merely available in the source file.

This document expresses the specification requirements for the data input file and the data output report in separate sections. The Data Input Requirements section defines the information and quality conditions that the source file must satisfy. The Data Output Requirements section defines the structure and values that the final report must produce.

For this specification, I elected to present the data requirements in a user-centered format that is easy to read and understand. I defined each requirement as an atomic condition that can be evaluated independently. This keeps the specification clear while allowing me to test the data against each condition separately. Structuring the requirements this way is especially beneficial for automated testing, as I can translate each requirement into an individual validation rule that yields a clear pass or fail result, streamlining data-quality troubleshooting and remediation.

# Data Input Requirements

## Human-Readable Data Requirements

### File Structure

The source file must be a CSV file encoded using UTF-8. It must contain one header row followed by student records. The file should use a consistent tabular structure so that each record can be read and evaluated reliably.

### Header Structure

The header should use clear, consistent column names. Column names must be uppercase, use underscores between words, and avoid spaces, numbers, special characters, and invisible characters. Each column name must be between 5 and 30 characters. The header must identify the student ID, first name, last name, program code, course code, midterm score, final score, and attendance. The header should contain only columns required for the report or for calculating report values. The EMAIL column and other unrelated columns are excluded because they are not needed for the report.

### Row Structure

Each row must represent one student enrolled in one course and one program.

#### Student ID

Each student ID must begin with the uppercase letter S followed by exactly three digits.

#### Program Code

Each PROGRAM_CODE must consist of the two uppercase letters IQ, representing Information Quality, followed by three numeric digits. Therefore, every program code must contain exactly five characters.

#### First Name

The FIRST_NAME field must contain only the student's given name, written in uppercase, without titles, honorifics, suffixes, or surname particles such as MR., MRS., MS., DR., SR., JR., VON, VAN, VOM, or ZU. For example, MR. HANS must be represented as HANS, and HANS VON GOETHE must use HANS as FIRST_NAME. Surname particles must remain with LAST_NAME when they are part of the family name.

#### Assessment Scores

The MIDTERM, FINAL, and ATTENDANCE columns must contain numeric scores with a maximum value of 100 and a resolution of one decimal place. When a score is unavailable, the field must remain null. Missing scores must not be represented by NA, N/A, unknown, or other characters.

#### Record Uniqueness

The same student-course combination must not appear more than once in the file.

# Data Output Requirements

The data output report reuses the previously defined file, header, and row-structure requirements. The output must preserve the applicable structure and data-quality rules established for the input data. In addition, the output report must include two derived columns: COURSE_AVERAGE and FINAL_LETTER_GRADE.

## Data Output/Reporting Columns

#### COURSE_AVERAGE

The COURSE_AVERAGE column must show the student's final course average. The average is calculated by giving 45% weight to the midterm score, 45% weight to the final score, and 10% weight to the attendance score. The calculated result must be rounded to the nearest whole number.

#### FINAL_LETTER_GRADE

The FINAL_LETTER_GRADE column must show the letter grade assigned to the rounded COURSE_AVERAGE. Averages from 90 to 100 receive an A, 80 to 89 receive a B, 70 to 79 receive a C, 60 to 69 receive a D, and 0 to 59 receive an F.

# Assessment of Data Input File

When developing the specification, I also defined atomic requirements so that each condition could be tested independently. I use these atomic requirements in a PowerShell script to evaluate the input file and produce clear pass, fail, or not-applicable results. I elected to use PowerShell instead of Python for two reasons. First, PowerShell is already installed and available in most Windows-based corporate environments and can use built-in Windows components to run scripts without requiring an additional programming-language installation. Second, using Python may introduce additional governance risks in corporate environments, including the need to review and comply with the commercial licenses of external libraries and the possibility of introducing external software and supply-chain vulnerabilities when importing those libraries.

The evaluation found deficiencies wherever the input file failed an atomic requirement. Rules 2.2, 2.3, and 2.5 failed because the header contains lowercase letters, numbers, and special characters. Rules 2.9.1 through 2.9.6 and 2.9.8 failed because the required STUDENT_ID, FIRST_NAME, LAST_NAME, PROGRAM_CODE, COURSE_CODE, MIDTERM, and ATTENDANCE columns are missing or incorrectly named. Rules 3.1.3 and 3.1.4 failed because one student ID, S1000, contains four digits after S and has five characters instead of the required three digits and four characters. Rules 3.2.1 through 3.2.4 failed because PROGRAM_CODE is absent from all 1,000 records. Rules 3.3.1 through 3.3.7 failed because the file contains a combined NAME field instead of separate FIRST_NAME and LAST_NAME fields. Assessment rules 3.4.3, 3.4.4, 3.4.5, 3.4.7, 3.4.8, 3.4.12, and 3.4.13 failed because the file contains nonnumeric attendance values, scores above 100, values with more than one decimal place, and text placeholders such as unknown, N/A, and seventy-five. Finally, rule 3.5.1 failed because duplicate STUDENT_ID and COURSE_CODE combinations were found. The output rules were correctly marked NA because the output report has not yet been created.

# Plan for Remediation of Each Deficiency

To resolve data-quality errors, I will execute targeted remediation across the dataset. First, I will fix header issues by renaming columns to approved uppercase formats with underscores, creating PROGRAM_CODE, splitting NAME into FIRST_NAME and LAST_NAME, and aligning the remaining fields. Next, I will resolve identifier errors by correcting invalid IDs and removing duplicate STUDENT_ID and COURSE_CODE pairings. For name fields, I will strip titles and suffixes, preserve surname particles in LAST_NAME, convert text to uppercase, and enforce a 60-character limit. Finally, I will standardize score data by fixing nonnumeric entries, correcting values above 100, trimming excessive decimals, and replacing text placeholders such as unknown and N/A with null.

The remaining errors concern requirements that cannot currently be confirmed from the input file alone. Rules 3.2.1 through 3.2.4 cannot currently be satisfied because PROGRAM_CODE is missing, requiring me to obtain authoritative program information before validating its format. Similarly, rules 3.3.1 through 3.3.7 cannot currently be evaluated because the source file uses a combined NAME field rather than separate FIRST_NAME and LAST_NAME columns; I must split and verify these names before testing capitalization, titles, suffixes, surname particles, and length. Finally, output rules 4.1 through 4.15 are marked NA because the final report does not yet exist.

<div style="page-break-before: always;"></div>

# Appendix A: Atomic Validation Requirements

### 1. File Structure

1. The file must have a .csv filename extension.
2. The file must be parseable as comma-separated values.
3. The file must use UTF-8 encoding.

### 2. Header Structure

1. The file must contain one header row.
2. Each column name must contain no lowercase letters.
3. Each column name must contain no numbers.
4. Each column name must contain no spaces.
5. Each column name must contain no special characters; underscores are the only permitted non-alphabetic character.
6. Each column name must contain no invisible or non-printing characters.
7. Each column name must contain at least 5 characters.
8. Each column name must contain no more than 30 characters.
9. The header must contain the required columns:
   1. The header must contain a STUDENT_ID column.
   2. The header must contain a FIRST_NAME column.
   3. The header must contain a LAST_NAME column.
   4. The header must contain a PROGRAM_CODE column.
   5. The header must contain a COURSE_CODE column.
   6. The header must contain a MIDTERM column.
   7. The header must contain a FINAL column.
   8. The header must contain an ATTENDANCE column.
10. The header must not contain an EMAIL column.
11. Every column in the header must support a reporting or calculation requirement.

### 3. Row Structure

#### 3.1 Student ID

1. Each data row must contain one STUDENT_ID value.
2. Each STUDENT_ID must begin with the uppercase letter S.
3. Each STUDENT_ID must contain exactly three digits after the letter S.
4. Each STUDENT_ID must contain exactly four characters.

#### 3.2 Program Code

1. Each data row must contain one PROGRAM_CODE value.
2. Each PROGRAM_CODE must begin with the uppercase letters IQ.
3. Each PROGRAM_CODE must contain exactly three digits after IQ.
4. Each PROGRAM_CODE must contain exactly five characters.

#### 3.3 First Name

1. Each data row must contain one FIRST_NAME value.
2. Each FIRST_NAME value must represent the student's given name.
3. Each FIRST_NAME value must use uppercase letters.
4. Each FIRST_NAME value must not contain a title or honorific.
5. Each FIRST_NAME value must not contain a suffix.
6. Each FIRST_NAME value must not contain a surname particle.
7. Each FIRST_NAME value must contain no more than 60 characters.

#### 3.4 Assessment Scores

1. Each MIDTERM value must be numeric.
2. Each FINAL value must be numeric.
3. Each ATTENDANCE value must be numeric.
4. Each MIDTERM value must not exceed 100.
5. Each FINAL value must not exceed 100.
6. Each ATTENDANCE value must not exceed 100.
7. Each MIDTERM value must use no more than one decimal place.
8. Each FINAL value must use no more than one decimal place.
9. Each ATTENDANCE value must use no more than one decimal place.
10. A missing MIDTERM value must be represented as null.
11. A missing FINAL value must be represented as null.
12. A missing ATTENDANCE value must be represented as null.
13. A missing score must not be represented by NA, N/A, unknown, or another text value.

#### 3.5 Record Uniqueness

1. Each STUDENT_ID and COURSE_CODE combination must be unique.

### Atomic Output Requirements

#### COURSE_AVERAGE

1. The output must contain a COURSE_AVERAGE column.
2. COURSE_AVERAGE must be calculated using the MIDTERM value.
3. COURSE_AVERAGE must be calculated using the FINAL value.
4. COURSE_AVERAGE must be calculated using the ATTENDANCE value.
5. The MIDTERM value must contribute 45% to COURSE_AVERAGE.
6. The FINAL value must contribute 45% to COURSE_AVERAGE.
7. The ATTENDANCE value must contribute 10% to COURSE_AVERAGE.
8. The calculated COURSE_AVERAGE must be rounded to the nearest whole number.

Formal calculation:

$$
COURSE\_AVERAGE = ROUND((0.45 \times MIDTERM) + (0.45 \times FINAL) + (0.10 \times ATTENDANCE), 0)
$$

#### FINAL_LETTER_GRADE

1. The output must contain a FINAL_LETTER_GRADE column.
2. FINAL_LETTER_GRADE must be based on COURSE_AVERAGE.
3. COURSE_AVERAGE values from 90 through 100 must produce A.
4. COURSE_AVERAGE values from 80 through 89 must produce B.
5. COURSE_AVERAGE values from 70 through 79 must produce C.
6. COURSE_AVERAGE values from 60 through 69 must produce D.
7. COURSE_AVERAGE values from 0 through 59 must produce F.

<div style="page-break-before: always;"></div>

# Appendix B: Errors detection output from PowerShell custom application

The following table reproduces the deficiency catalog generated by the PowerShell application. Passing rules are omitted because this appendix records errors and rules that are not yet applicable.

| RULE_ID | STATUS | REQUIREMENT | EVIDENCE | REMEDIATION |
| --- | --- | --- | --- | --- |
| 2.2 | FAIL | Column names contain no lowercase letters. | 0 of 7 column names meet this condition. | Rename the columns using uppercase letters. |
| 2.3 | FAIL | Column names contain no numbers. | 6 of 7 column names meet this condition. | Remove numbers from column names. |
| 2.5 | FAIL | Column names contain no special characters. | 2 of 7 column names meet this condition. | Replace special characters with approved underscores. |
| 2.9.1 | FAIL | Required column STUDENT_ID. | The column is missing. | Rename the source ID column to STUDENT_ID. |
| 2.9.2 | FAIL | Required column FIRST_NAME. | The column is missing. | Split NAME and create FIRST_NAME. |
| 2.9.3 | FAIL | Required column LAST_NAME. | The column is missing. | Split NAME and create LAST_NAME. |
| 2.9.4 | FAIL | Required column PROGRAM_CODE. | The column is missing. | Add authoritative program codes. |
| 2.9.5 | FAIL | Required column COURSE_CODE. | The column is missing. | Rename the source course column to COURSE_CODE. |
| 2.9.6 | FAIL | Required column MIDTERM. | The column is missing. | Rename the source midterm column to MIDTERM. |
| 2.9.8 | FAIL | Required column ATTENDANCE. | The column is missing. | Rename the source attendance column to ATTENDANCE. |
| 3.1.3 | FAIL | Each STUDENT_ID contains three digits after S. | S1000 appears in source row 1001. | Correct S1000 to the authoritative four-character ID. |
| 3.1.4 | FAIL | Each STUDENT_ID contains four characters. | S1000 appears in source row 1001. | Correct the student ID length. |
| 3.2.1 | FAIL | Each data row contains one PROGRAM_CODE value. | PROGRAM_CODE is missing in all 1,000 records. | Obtain and add authoritative program codes. |
| 3.2.2 | FAIL | Each PROGRAM_CODE begins with IQ. | PROGRAM_CODE cannot be checked because the column is missing. | Add codes beginning with IQ. |
| 3.2.3 | FAIL | Each PROGRAM_CODE contains three digits after IQ. | PROGRAM_CODE cannot be checked because the column is missing. | Add codes with three digits after IQ. |
| 3.2.4 | FAIL | Each PROGRAM_CODE contains five characters. | PROGRAM_CODE cannot be checked because the column is missing. | Add five-character program codes. |
| 3.3.1 | FAIL | Each data row contains one FIRST_NAME value. | FIRST_NAME is missing; NAME is combined in all 1,000 records. | Split NAME into FIRST_NAME and LAST_NAME. |
| 3.3.2 | FAIL | Each FIRST_NAME represents the student's given name. | The given name cannot be evaluated because FIRST_NAME is missing. | Create FIRST_NAME from authoritative records. |
| 3.3.3 | FAIL | Each FIRST_NAME uses uppercase letters. | FIRST_NAME capitalization cannot be evaluated because FIRST_NAME is missing. | Convert FIRST_NAME values to uppercase. |
| 3.3.4 | FAIL | Each FIRST_NAME contains no title or honorific. | Titles cannot be separated because FIRST_NAME is missing. | Remove titles and honorifics from FIRST_NAME. |
| 3.3.5 | FAIL | Each FIRST_NAME contains no suffix. | Suffixes cannot be evaluated because FIRST_NAME is missing. | Remove suffixes from FIRST_NAME. |
| 3.3.6 | FAIL | Each FIRST_NAME contains no surname particle. | Surname particles cannot be evaluated because FIRST_NAME is missing. | Keep surname particles with LAST_NAME. |
| 3.3.7 | FAIL | Each FIRST_NAME contains no more than 60 characters. | FIRST_NAME length cannot be evaluated because FIRST_NAME is missing. | Create FIRST_NAME and enforce the length limit. |
| 3.4.3 | FAIL | Each ATTENDANCE value is numeric. | 37 attendance values are nonnumeric, including unknown, N/A, 100%, and seventy-five. | Convert valid values and replace unconfirmed values with null. |
| 3.4.4 | FAIL | Each MIDTERM value does not exceed 100. | 56 midterm values exceed 100. | Correct the affected midterm values. |
| 3.4.5 | FAIL | Each FINAL value does not exceed 100. | 80 final values exceed 100. | Correct the affected final values. |
| 3.4.7 | FAIL | Each MIDTERM value uses no more than one decimal place. | 42 midterm values contain excessive decimal precision. | Round or correct midterm values to one decimal place. |
| 3.4.8 | FAIL | Each FINAL value uses no more than one decimal place. | 69 final values contain excessive decimal precision. | Round or correct final values to one decimal place. |
| 3.4.12 | FAIL | A missing ATTENDANCE value is represented as null. | 29 attendance values use text instead of null. | Replace missing-value text with null. |
| 3.4.13 | FAIL | A missing score is not represented by text. | Text placeholders include unknown, N/A, and seventy-five. | Replace text placeholders with null. |
| 3.5.1 | FAIL | Each STUDENT_ID and COURSE_CODE combination is unique. | 18 records belong to duplicate student-course combinations. | Investigate duplicates and retain one authoritative record per pair. |
| 4.1 | NA | The output contains a COURSE_AVERAGE column. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.2 | NA | COURSE_AVERAGE uses MIDTERM. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.3 | NA | COURSE_AVERAGE uses FINAL. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.4 | NA | COURSE_AVERAGE uses ATTENDANCE. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.5 | NA | MIDTERM contributes 45 percent. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.6 | NA | FINAL contributes 45 percent. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.7 | NA | ATTENDANCE contributes 10 percent. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.8 | NA | COURSE_AVERAGE is rounded to a whole number. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.9 | NA | The output contains a FINAL_LETTER_GRADE column. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.10 | NA | FINAL_LETTER_GRADE is based on COURSE_AVERAGE. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.11 | NA | Averages 90 through 100 produce A. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.12 | NA | Averages 80 through 89 produce B. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.13 | NA | Averages 70 through 79 produce C. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.14 | NA | Averages 60 through 69 produce D. | The output report has not been created. | Create the output report and rerun the evaluation. |
| 4.15 | NA | Averages 0 through 59 produce F. | The output report has not been created. | Create the output report and rerun the evaluation. |


