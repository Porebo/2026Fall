# Principles of IQ - HW02: MovieDataset Data Assessment

## Characteristics of the Data

This is a cohesive dataset that describes, in each row, a set of characteristics about a show. Its focus is consistent: it does not combine unrelated topics, such as horse betting or child births, with the show information.

 The `show_id` field is not unique: only the values `s1` through `s50` appear, and each occurs 17 or 18 times. Many titles also recur frequently; for example, `The Crown` appears 57 times and `The Irishman` 56 times. Since the rows represent individual shows, these repeated identifiers and titles are characteristics that should be investigated. If `show_id` is intended to uniquely identify a show, its repeated values would prevent it from serving as a unique identifier. The repeated titles may represent distinct shows with the same name, or they may indicate duplicate records. Neither observation can be called a data-quality error without an explicit uniqueness requirement, but both would matter when the dataset is used to count or identify individual shows.

## Dataset Overview

The dataset contains 860 rows and 13 columns: `show_id`, `type`, `title`, `director`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`, `user_rating_score`, and `number_of_reviews`. The facet steps below describe how to reproduce these observations in OpenRefine.

The records describe movies and television-related content. The `type` field has four values: Movie (302 rows), tv show (272), Stand-Up (148), and Documentary (138). This shows that the catalog includes several types of media content.

## Completeness

I used text facets to identify blank cells. Six fields contain blank values:

| Column | Blank rows | Percent of 860 rows |
| --- | ---: | ---: |
| `number_of_reviews` | 381 | 44.3% |
| `user_rating_score` | 344 | 40.0% |
| `duration` | 276 | 32.1% |
| `date_added` | 225 | 26.2% |
| `director` | 145 | 16.9% |
| `rating` | 85 | 9.9% |
| `country` | 51 | 5.9% |

The other six columns have values in every row. Whether a blank is a problem depends on the intended use. For example, a director may not apply to every content type, while missing review and score values would limit an analysis of audience reception.

## Numerical and Date Characteristics

All 860 `release_year` values are numeric. They range from 2000 to 2022, with an average of 2010.9 and a median of 2010.

There are 516 populated `user_rating_score` values. These range from 5.2 to 9.0, have an average of 7.25, and a median of 7.6. The 479 populated `number_of_reviews` values range from 67 to 996, with an average of 509.8 and a median of 547. The remaining entries in each of those fields are blank rather than non-numeric text.

`date_added` has 635 populated values. No nonblank values failed a date conversion check. The missing dates should be considered if the dataset is meant to support an analysis of additions over time.

## Categorical and Format Characteristics

The `rating` facet includes 85 blank values and several value formats. Its most common values are `tv-ma` (223), `TV-14` (173), `pg13` (172), `PG-13` (139), and `TV-PG` (68). The visible capitalization and punctuation variation in `tv-ma`/`TV-14` and especially `pg13`/`PG-13` may split otherwise comparable categories. Standardizing them would be appropriate only if a rating taxonomy is required for the analysis.

`duration` uses two populated formats: 499 entries in a `number min` form and 85 entries in a `number Season(s)` form; 276 values are blank. These are different units, so they should not be aggregated as one numeric duration without first defining how seasons are to be handled. The two duration formats occur across each value of `type`, so the type field does not by itself determine the duration unit.

`country` and `listed_in` can contain multi-valued text, so a text facet counts entire combinations rather than individual countries or genres. A split multi-valued-cell operation would be needed before calculating frequencies for individual countries or genres.

## Potential Anomalies and Questions for Requirements

Similarly, the rating-format differences and blank cells are not confirmed errors without business rules. They are potential issues when requirements call for complete reporting, normalized ratings, record-level uniqueness, or comparable numeric durations.

## OpenRefine Workflow to Reproduce the Assessment

1. Create a project from the CSV and confirm the 860-row import.
2. Used text facets on `type`, `rating`, and `duration` to inspect distinct values and counts.
3. Used blank/nonblank facets on each column to count missing values.
4. Used numeric facets or statistics for `release_year`, `user_rating_score`, and `number_of_reviews`.
5. Examined `date_added` for date parseability and reviewed duplicate groups for `show_id` and `title`.

No transformations are required to make these observations. Any cleaning step should follow explicit requirements for identifiers, accepted rating labels, required fields, and the meaning of each row.

