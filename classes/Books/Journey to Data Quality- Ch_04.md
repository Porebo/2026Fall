# Journey to Data Quality — Ch. 04

Notes from *Assessing Data Quality, Part II* (printed pp. 53–66).

## Codd's Five Integrity Constraints

Source: chapter's presentation of Codd (1970), printed p. 53.

### 1. Entity integrity
No primary key field value in a table may be null. Codd also requires the key be
unique; the chapter's metric counts only nulls.

    Degree of adherence = 1 − (null primary keys / total rows)

Example — `RPLC_LEGO.WELL`, primary key `FAC_ID`:

```sql
SELECT COUNT(*)                                            AS total_rows,
       COUNT(*) - COUNT(fac_id)                            AS null_pk,
       COUNT(DISTINCT fac_id)                              AS distinct_pk,
       ROUND(1 - (COUNT(*) - COUNT(fac_id)) / COUNT(*), 6) AS entity_integrity
FROM   RPLC_LEGO.WELL;
```

Result:

| TOTAL_ROWS | NULL_PK | DISTINCT_PK | ENTITY_INTEGRITY |
|---|---|---|---|
| 103,886 | 0 | 103,886 | 1 |

`COUNT(col)` skips nulls while `COUNT(*)` does not, so their difference is the
null count. `distinct_pk` equal to `total_rows` means no duplicates — the
uniqueness half of the rule, which the chapter's formula omits.

Tautological here: `WELL_WELL_PK` is ENABLED, so the database rejects nulls at
entry and the metric cannot return anything but 1.

**Worked examples**

| Object | Type | Key | Result |
|---|---|---|---|
| `RPLC_LEGO.WELL` | table | `FAC_ID`, PK `WELL_WELL_PK` ENABLED VALIDATED | 103,886 rows, 0 nulls, 103,886 distinct → 1.000 (tautological) |
| `EDMADMIN.CD_WELL_SOURCE` | view over `RPLC_EDMADMIN.CD_WELL_SOURCE` | `WELL_ID`, no declaration reachable | 113,507 rows, 0 nulls, 113,507 distinct → 1.000 (a real finding) |

Generic form of the measuring query:

```sql
SELECT COUNT(*)                  AS total_rows,
       COUNT(*) - COUNT(key_col) AS null_keys,
       COUNT(DISTINCT key_col)   AS distinct_keys
FROM   owner.object;
```

### 2. Referential integrity
The value of a foreign key must match a primary key value in the designated
related table, or the foreign key must be null.

    Degree of adherence = 1 − (nonmatching values excluding nulls / rows in dependent table)

Note: the constraint spans two tables, but the metric is scoped to the dependent
one. A table whose foreign keys are all null scores 1.0 while being fully
disconnected.

A violation is a **non-null** foreign key value with no matching parent — an
orphan. Nulls are excluded by design: a null foreign key means "no relationship,"
not "broken relationship."

Example — `RPLC_LEGO.WELL`. The schema has **no declared foreign keys at all**
(replication carried the primary keys but not the FKs), so every relationship is
convention only and must be measured:

```sql
SELECT COUNT(*)                   AS total_rows,
       COUNT(c.fk_col)            AS non_null_fk,
       COUNT(*) - COUNT(c.fk_col) AS null_fk,
       SUM(CASE WHEN c.fk_col IS NOT NULL
                 AND NOT EXISTS (SELECT 1 FROM parent_owner.parent_tbl p
                                 WHERE  p.pk_col = c.fk_col)
                THEN 1 ELSE 0 END) AS orphans
FROM   child_owner.child_tbl c;
```

The `IS NOT NULL` guard is Codd's "excluding nulls" clause expressed in SQL.

Results, five undeclared foreign keys on `RPLC_LEGO.WELL` (103,886 rows):

| FK column | Parent | Non-null FK | Orphans | Rating |
|---|---|---|---|---|
| `FAC_ID` | `FAC` | 103,886 | 0 | 1.000 |
| `REPL_WELL_FAC_ID` | `WELL` (self) | 7,034 | 0 | 1.000 |
| `WELL_DATUM_TYPE_ID` | `WELL_DATUM_TYPE` | 68,628 | 0 | 1.000 |
| `UIC_CLASS_TYPE_ID` | `UIC_CLASS_TYPE` | 1,574 | 0 | 1.000 |
| `WELL_INIT_DRLG_RSN_TYPE_ID` | `WELL_INIT_DRLG_RSN_TYPE` | 54,076 | 0 | 1.000 |

A real finding, not a tautology: nothing enforces these, and integrity held anyway
— evidence the replication is faithful and the source system enforced them.

Also shows the null asymmetry. `UIC_CLASS_TYPE_ID` scores 1.000 on only 1,574
actual references out of 103,886 rows — 98.5% null. The rating would look
identical if the column were entirely empty, which is why the non-null count
belongs beside it.

To list the offending rows rather than count them (the Integrity Analyzer's
"Improve" step):

```sql
SELECT c.*
FROM   child_owner.child_tbl c
WHERE  c.fk_col IS NOT NULL
AND    NOT EXISTS (SELECT 1 FROM parent_owner.parent_tbl p
                   WHERE p.pk_col = c.fk_col);
```

**Where measurement is worth doing.** `EDS` has 562 declared foreign keys:

| State | Count | What the metric tells you |
|---|---|---|
| `ENABLED, VALIDATED` | 535 | Nothing — 1.000 guaranteed |
| `ENABLED, NOT VALIDATED` | 17 | New rows checked; pre-existing never were |
| `DISABLED, NOT VALIDATED` | 10 | Nothing is enforced at all |

Only 27 of 562 are worth measuring. `ENABLE NOVALIDATE` is the state to watch:
enforcement starts at a point in time and says nothing about the data before it.

### 3. Domain integrity
The set of permissible values for a column — the type definition itself. Named in
the chapter but given no metric, since a domain is a property of the schema rather
than something counted row by row. Violations surface as column integrity (rule 4).

**Declared domain vs. real domain.** The declaration sets an outer bound that is
usually far wider than the actual permissible set. `VARCHAR2(8)` permits any eight
characters; the real domain may be four status codes. Three levels:

| Level | Declared? | Enforced? |
|---|---|---|
| Datatype, length, precision, NOT NULL | yes | always |
| Check constraint | yes | if ENABLED |
| Lookup table | as data, not as declaration | only if an FK points at it |

The third is the common case here. `UIC_CLASS_TYPE_ID`'s permissible values live as
rows in `UIC_CLASS_TYPE` — a domain expressed as data. With no FK declared, the
orphan check under rule 2 *is* the domain check.

**Why there is no metric.** The permissible set has to come from outside the data
— a dictionary, a spec, a domain expert. It cannot be derived from the column,
because what is there may already be wrong. Profiling gets you candidates; only a
human confirms the boundary. Rule 3 sits closer to rule 5 than its numbering
suggests.

Profiling is still structurally useful before any spec arrives. The *shape* of the
distribution is informative: 4 distinct values in 100k rows is a code column; one
distinct value per row is an identifier; two values at 40k each plus six appearing
once makes those six suspicious whatever the spec says.

Example — `DWRPTG.CMPL_DMN.INIT_PROD_DTE`:

```sql
SELECT COUNT(*)                        AS total_rows,
       COUNT(init_prod_dte)            AS non_null,
       COUNT(*) - COUNT(init_prod_dte) AS nulls,
       TO_CHAR(MIN(init_prod_dte),'YYYY-MM-DD') AS min_date,
       TO_CHAR(MAX(init_prod_dte),'YYYY-MM-DD') AS max_date,
       SUM(CASE WHEN init_prod_dte > SYSDATE THEN 1 ELSE 0 END) AS future_dates
FROM   DWRPTG.CMPL_DMN;
```

Result:

| TOTAL_ROWS | NON_NULL | NULLS | MIN_DATE | MAX_DATE | FUTURE_DATES |
|---|---|---|---|---|---|
| 290,253 | 175,085 | 115,168 | 1800-01-01 | 2026-09-21 | 0 |

Max is yesterday and no future dates — sensible. But the minimum is **1800**,
predating the oil industry. The datatype permits it, so nothing objected.

Distribution by year to locate the boundary:

```sql
SELECT TO_CHAR(init_prod_dte,'YYYY') AS yr, COUNT(*) AS cnt
FROM   DWRPTG.CMPL_DMN
WHERE  init_prod_dte < DATE '1950-01-01'
GROUP  BY TO_CHAR(init_prod_dte,'YYYY')
ORDER  BY yr;
```

| Range | Count | Verdict |
|---|---|---|
| 1800 | 106 | Sentinel — violation |
| 1900 | 12 | Possible sentinel — needs a human |
| 1901–1949 | ~10,000 | Legitimate |

All 106 sit at exactly `1800-01-01` with no scatter, confirming a deliberate
placeholder for "unknown" rather than data entry noise. The 1901–1949 values climb
smoothly and track real history — a bump at 1915–1917, growth through the 1920s, a
dip in the early 1940s, a jump at 1945 — so they are real production dates, not
violations.

Taking "plausible production date" as the permissible set:

    Rating = 1 − (106 / 175,085) = 0.99939

The denominator caveat in action: 0.9994 reads as fine while 106 rows carry a date
off by 150 years. Anything averaging or trending this column silently includes them.

### 4. Column integrity
Values in a column must be drawn from the set of permissible values. This is where
rule 3's domain gets measured.

    Degree of adherence = 1 − (invalid column values / rows in table)

The chapter also notes that where a column represents a required property, this
doubles as a check of **column completeness**.

Profiling query — distinct values with counts:

```sql
SELECT NVL(col,'(null)') AS val,
       COUNT(*)          AS cnt,
       MAX(LENGTH(col))  AS len
FROM   owner.tbl
GROUP  BY col
ORDER  BY cnt DESC;
```

Where a lookup table holds the domain, the measurable version — same form as the
orphan check under rule 2:

```sql
SELECT COUNT(*) AS total_rows,
       SUM(CASE WHEN c.col IS NOT NULL
                 AND NOT EXISTS (SELECT 1 FROM owner.lookup_tbl l
                                 WHERE l.code = c.col)
                THEN 1 ELSE 0 END) AS invalid_values
FROM   owner.tbl c;
```

**Example 1 — `DWRPTG.CMPL_DMN.CMPL_STATE_TYPE_CDE`**, declared `VARCHAR2(50)`:

| Value | Count | Length |
|---|---|---|
| `OPNL` | 171,196 | 4 |
| `ABND` | 61,499 | 4 |
| `TA` | 28,585 | 2 |
| `PRPO` | 22,028 | 4 |
| `FUTR` | 3,792 | 4 |
| (null) | 1,915 | |
| `CANCD` | 1,229 | 5 |
| `INPRGS` | **9** | 6 |

Declared domain is 50 characters; the real domain is 7 values, max length 6.

The shape is a closed set with one straggler: `INPRGS` at 9 rows against a
next-smallest of 1,229 — three orders of magnitude apart. Structurally the thing to
ask about, though its form (uppercase abbreviation, consistent with the rest)
suggests a deprecated or rare state rather than a typo. Confirming that needs a
domain expert.

If `INPRGS` is deemed invalid:

    Rating = 1 − (9 / 288,338) = 0.99997

The denominator problem at its most extreme — a value worth investigating, scoring
as indistinguishable from perfect.

**Example 2 — the `_INDC` columns**, all declared `VARCHAR2(1)` or `CHAR(1)`:

| Column | Values | Rating |
|---|---|---|
| `ACTV_INDC` | N 179,842 / Y 110,411 | 1.000 |
| `IN_SVC_INDC` | null 142,637 / Y 101,956 / N 45,660 | 1.000 |
| `PMTD_TO_CYCL_INDC` | null 266,004 / N 17,396 / Y 6,853 | 1.000 |
| `LOW_USE_CYC_INDC` | null 290,253 | 1.000 |

Every non-null value is `Y` or `N` — no stray `y`, `1`, `T` or blanks. Column
integrity holds throughout.

But the profile surfaces what the rating cannot: **`LOW_USE_CYC_INDC` is 100%
null** across all 290,253 rows. Perfect column integrity on an empty column. The
same blind spot as an all-null foreign key under rule 2 — caught by the
completeness dimension, not by integrity.

### 5. Business rules
Codd's all-purpose category for integrity rules specific to an organization.
Cannot be task-independent by definition.

## Task-independent vs. context-dependent

The first four constraints yield **task-independent** metrics: they reflect the
state of the data without contextual knowledge of the application, and apply to
any dataset regardless of task.

The fifth cannot. It is where expectations that live outside the schema belong —
e.g. "this view column should behave like a primary key."

## Canonical form

All four metrics above are instances of one ratio:

    Rating = 1 − (number of undesirable outcomes / total outcomes)

1 is most desirable, 0 least. Exceptions are counted because they are fewer and
easier to tabulate, then inverted so the reported figure expresses adherence.

## Enforcement vs. diagnosis

Commercial RDBMS check Codd's constraints **at entry** — violations never land
(printed p. 61). Measuring adherence on an enforced key can only return 1.0, so
the result is a tautology rather than a finding.

The metrics earn their keep where enforcement is absent or weaker:

- views (no key to enforce; a stored query, not stored rows)
- replicated copies, where constraints may not have shipped
- legacy systems, imports, staging tables


### Checking the declaration

```sql
SELECT c.constraint_name, c.constraint_type, c.status, c.validated,
       cc.column_name, cc.position
FROM   all_constraints c
JOIN   all_cons_columns cc
       ON cc.owner = c.owner AND cc.constraint_name = c.constraint_name
WHERE  c.owner = '<OWNER>' AND c.table_name = '<TABLE>'
AND    c.constraint_type IN ('P','U','R')
ORDER  BY c.constraint_type, c.constraint_name, cc.position;
```

Types: `P` primary key, `R` referential, `U` unique, `C` check (includes NOT NULL).

### On views specifically

A view has no room for an enforced key — the data materializes at query time.
Oracle permits a declared PK on a view only as `DISABLE NOVALIDATE`, as metadata
for query rewrite; it enforces nothing.

So for a view, entity integrity is **measured, never guaranteed**. Views also break
key properties in non-obvious ways: joins fan out rows and destroy uniqueness,
outer joins introduce nulls in columns that were non-null at the base, unions
collide keys from separate sources.

Uniqueness is the more important half to test on a view. Nulls tend to get
noticed; duplicates silently fan out downstream joins and inflate counts.

## Caveats

- **Denominator sensitivity.** The metric is a rate, not a count. Five bad rows
  score 0.95 in a 100-row table and 0.999995 in a million-row table. Report the
  raw violation count alongside the rating.
- **Per-table scope.** Each metric is scoped to one table, so scores across tables
  are not commensurable and should not be pooled. Aggregate with `min` if a
  database-level figure is needed.
- **Naming.** "Codd's fifth" here means the fifth *integrity constraint* in this
  book's framing — not Codd's 12 Rules for relational DBMS, a different list.
