# AI Prompt to Maintain Financial Data

## Mission

Maintain this workspace as an evidence-backed personal accounting system. The system starts with bank and credit-card statements, converts verified activity into balanced General Journal entries, posts the activity to individual account ledgers, projects future cash activity in the Bank of America budget, and summarizes posted activity in a Trial Balance.

Preserve the audit trail at every step. Do not guess an account, transaction source, or payment amount when the document does not support it. Use the suspense account and the `Pending source document` label until the missing evidence is available.

This guide is intentionally operational. Follow it before changing financial data.

## Workspace Map

The financial system lives primarily in these files:

| Path | Responsibility |
| --- | --- |
| `data/accounts.json` | Source of truth for chart of accounts, account details, statement transactions, recurring forecast items, explicit account ledgers, and supplemental GJ entries. |
| `scripts/accounting.js` | Renders the Bank of America budget/forecast page and contains reusable sort/filter controls. |
| `scripts/account-ledger.js` | Renders all numbered account ledger pages from `accounts.json`. |
| `scripts/general-journal.js` | Generates the General Journal from BofA statement activity plus supplemental GJ entries. |
| `scripts/trial-balance.js` | Builds the activity Trial Balance from posted journal activity. |
| `ledger/0000.html` | Ledger Index / chart-of-accounts entry point. |
| `ledger/1000.html`, `ledger/1001.html`, etc. | Individual account ledger pages. The filename is the chart-account code. |
| `ledger/BUDGET_BofA_7632.html` | Bank of America checking budget and future transaction forecast. |
| `ledger/General Journal.html` | General Journal view. |
| `ledger/Trial Balance.html` | Activity Trial Balance view. |
| `ledger/account-ledger.css` | Shared compact ledger and table-control styling. |
| `ledger/*.pdf` | Source statements. Keep them with the ledger when the user wants cross-computer availability. |

All page paths are relative to the repository root. A static server can be started with:

```powershell
python -m http.server 8080 --directory .
```

Then open a page such as:

```text
http://localhost:8080/ledger/General%20Journal.html
```

## Core Accounting Rules

1. Every posted General Journal entry must balance: total debits equal total credits.
2. A ledger `Ref.` is the **General Journal entry number**, not a displayed-row number.
3. Opening balances are not journal entries. Display `-` in their Ref. column unless an actual opening-entry journal is later created.
4. Scheduled future budget rows are not posted journal entries. Display `-` in their Ref. column and `S` in Status.
5. Completed, evidence-backed activity displays `C` with a check mark.
6. Do not post an unverified card or bank assignment to a real account. Use `2999 Unclassified activity (suspense)` and a source value of `Pending source document`.
7. Do not double count activity. A transaction already represented by an explicit statement ledger must not also be injected from a generic transaction list into that same account ledger.
8. Use only account suffixes in page names and display labels. Do not put full account numbers into hand-authored pages or documentation.

## Statement-to-Accounting Workflow

Use this process for every new statement.

### 1. Preserve the source document

Place the original PDF in `ledger/` using a stable, descriptive filename. Existing naming examples:

- `BofA-2026-09-7632.pdf`
- `Barclays-2026-08-0741.pdf`
- `Barclays-2026-08-2946.pdf`
- `WellsFargo-2026-08_0805.pdf`
- `WellsFargo-2026-09_0009.pdf`
- `WellsFargo-2026-09_9110.pdf`
- `Chase_2026-08-5236-.pdf`
- `Chase_2026-09-5236-.pdf`
- `Chase-2026-08-3254-.pdf`
- `Chase_2026-09-3254-.pdf`
- `Affirm Loan.pdf`

If the user works from multiple computers, add the PDF to Git along with the derived data. Do not leave source evidence untracked unless the user explicitly wants it local-only.

### 2. Reconcile the statement itself

Extract and verify:

- Statement period start and end dates.
- Opening balance.
- Every deposit, charge, payment, transfer, fee, and interest posting.
- Closing balance.
- Account ending digits, bank, due date, minimum due, scheduled AutoPay, and source-document filename.

The local reconciliation equation is:

$$
\text{Opening balance} + \sum \text{debits} - \sum \text{credits} = \text{Closing balance}
$$

The sign convention in an account ledger is account-specific. For example:

- Asset ledger: deposits are debit-side increases; withdrawals are credit-side decreases.
- Liability ledger: purchases/interest increase the credit side; payments decrease the liability on the debit side.
- Expense ledger: charges are debit-side increases; a payment or reversal may be displayed as a credit-side reduction.

### 3. Create or update the chart account

Add a chart account under `chartOfAccounts` in `data/accounts.json` only when it represents a distinct account or classification.

Example:

```json
{
  "id": "wells-fargo-way2save-0805",
  "code": "1005",
  "name": "Wells Fargo Way2Save Savings ending in 0805",
  "type": "asset",
  "normalBalance": "debit"
}
```

Code ranges currently follow this convention:

| Range | Purpose |
| --- | --- |
| `1000` - `1999` | Assets: checking and savings accounts. |
| `2100` - `2499` | Liabilities: credit cards, loans, utilities carried as payable accounts. |
| `2999` | Unclassified activity suspense account. |
| `4000` - `4999` | Income. |
| `5000` - `5999` | Expenses. |

Do not reuse a code for two different accounts. New current examples include:

- `1001` Wells Fargo Everyday Checking ending in `0009`
- `1006` Chase Total Checking ending in `5236`
- `2108` Chase Freedom Flex ending in `3254`
- `2113` Affirm Monitor (masked suffix `XXXX`)
- `1005` Wells Fargo Way2Save Savings ending in `0805`
- `2104` GM Rewards Mastercard ending in `2946`
- `2107` Wells Fargo Active Cash ending in `9110`
- `2112` Barclays Rewards World Mastercard ending in `0741`
- `4001` Bank interest income
- `5005` San Joaquin Pest Control
- `5006` AT&T mobility
- `5007` Bank fees
- `5008` Vehicle wash expense
- `5009` Personal-use monitor expense

### 4. Add account detail and explicit statement ledger entries

The `accounts` array stores display details, current statement status, recurring payments, and optional exact statement-ledger records.

Use `openingBalanceDate`, `openingBalanceCents`, and `ledgerEntries` when a statement has enough information to reconstruct the account ledger exactly.

Example pattern for a liability statement:

```json
{
  "id": "example-card",
  "bank": "Example Bank",
  "name": "Example Card",
  "lastFour": "1234",
  "dueDate": "2026-10-18",
  "minimumDueCents": 2500,
  "plannedPaymentCents": 2500,
  "statementBalanceCents": 15000,
  "balanceCents": 15000,
  "status": "open",
  "openingBalanceDate": "2026-08-25",
  "openingBalanceCents": 0,
  "ledgerEntries": [
    {
      "date": "2026-08-29",
      "amountCents": 15718,
      "description": "Verified card charge",
      "balanceAfterCents": 15718,
      "isDebit": false,
      "journalEntry": "GJ-0052"
    },
    {
      "date": "2026-09-23",
      "amountCents": 718,
      "description": "Verified payment",
      "balanceAfterCents": 15000,
      "isDebit": true,
      "journalEntry": "GJ-0058"
    }
  ]
}
```

Interpretation of important fields:

| Field | Meaning |
| --- | --- |
| `amountCents` | Always a positive absolute amount in an explicit account ledger. |
| `isDebit` | `true` renders the amount in Debit; `false` renders it in Credit. Required when the normal sign cannot safely be inferred. |
| `balanceAfterCents` | Reconciled balance after that exact line. |
| `journalEntry` | Source General Journal entry, such as `GJ-0058`; use `-` or omit for opening balance. |
| `ledgerEntries` | Overrides generic transaction rendering for that account; do not duplicate those entries elsewhere in the same account ledger. |

### 5. Create a balanced General Journal entry

Supplemental entries live in `supplementalJournalEntries`.

Each entry needs:

- `number`: next available `GJ-####` value.
- `date`: posting date.
- `description`: human-readable explanation shown in the gray comment row.
- Optional entry-level `sourceDocument`: fallback only.
- `lines`: each debit or credit posting.

Each line needs its own `sourceDocuments` list when its evidence differs from the other side of the journal entry.

Example: one document supports the Active Cash payment, another supports the cash withdrawal:

```json
{
  "number": "GJ-0058",
  "date": "2026-09-23",
  "description": "Wells Fargo Everyday Checking payment to Active Cash Visa",
  "lines": [
    {
      "accountId": "wells-fargo-active-cash-9110",
      "debitCents": 718,
      "creditCents": 0,
      "sourceDocuments": ["WellsFargo-2026-09_9110.pdf"]
    },
    {
      "accountId": "wells-fargo-checking",
      "debitCents": 0,
      "creditCents": 718,
      "sourceDocuments": ["WellsFargo-2026-09_0009.pdf"]
    }
  ]
}
```

For unknown source evidence:

```json
"sourceDocuments": ["Pending source document"]
```

The General Journal renders this order:

```text
Entry | Source | Post | Date | Description | Debit | Credit
```

The debit account prints on the first posting line. The credit account prints on the second line with indentation. A full-width gray italic row below them contains the entry description.

### 6. Link source documents line by line

`scripts/general-journal.js` uses `line.sourceDocuments` first, then falls back to `entry.sourceDocument` for older entries. PDF names render as links in the Source column. Plain text values such as `Pending source document` render as text.

This is important for auditability:

- Debit and credit lines may be supported by different bank statements.
- A merchant receipt may support an expense line while a card statement supports the liability line.
- A payment may be known from a checking statement even before the receiving-card statement arrives.

Never claim a source document supports a side it does not show.

## Current Journal Numbering

The first 43 BofA statement transactions are generated as:

```text
GJ-0001 through GJ-0043
```

Supplemental evidence-backed entries currently continue from:

```text
GJ-0044 onward; the Affirm loan and payment history continues through GJ-0089
```

Before adding an entry, inspect `supplementalJournalEntries` and select the next unused number. Do not renumber old GJ references, because account ledgers use those values in their Ref. column.

## Bank of America Budget

`ledger/BUDGET_BofA_7632.html` is a budget and forecast, not the historical BofA account ledger.

It combines:

1. Reconciled BofA statement activity from `checkingLedgerTransactions`.
2. Future recurring obligations from the `accounts` array.
3. Future transfers from `cashForecastEntries`.
4. Future payroll from `paycheckSchedule`.

The page has:

- `C` for completed statement activity.
- `S` for scheduled future budget activity.
- `GJ-####` references for completed BofA rows.
- `-` in Ref. for opening balance and scheduled forecast rows.

For a recurring account, use:

```json
"recurrence": {
  "frequency": "monthly",
  "dayOfMonth": 18,
  "amountCents": 2500
}
```

For a known final installment, `recurrence.endDate` stops projection and optional `recurrence.finalAmountCents` overrides the regular amount on that date. `paymentSourceLabel` identifies the funding account in the budget forecast without posting a future journal entry.

Use `plannedPaymentCents` when a known AutoPay amount differs from the statement balance. Example: GM Rewards statement balance was `$680.58`, but the verified AutoPay was `$30.00`; therefore `plannedPaymentCents` must be `3000`, not `68058`.

Do not create a budget forecast just because a charge appears once. Add recurrence only when the statement, user, or documented billing arrangement supports it.

## Individual Ledger Pages

Every chart account should have a code-named page in `ledger/`, for example:

```text
1001.html
1005.html
2107.html
2999.html
4001.html
5006.html
```

The page is intentionally minimal. It identifies its account with:

```html
<body data-account-id="wells-fargo-way2save-0805">
  <script src="../scripts/account-ledger.js"></script>
</body>
```

`scripts/account-ledger.js` supplies the shared breadcrumb, account metadata, eight-column ledger, sort buttons, and Excel-like filter controls.

The individual ledger columns are:

```text
Date | Ref. | Code | Status | Description | Debit | Credit | Balance
```

Rules:

- Opening balance has Ref. `-`.
- Explicit statement ledger entries use their `journalEntry` reference.
- Generic BofA statement transactions receive generated GJ references.
- Use `isDebit` for explicit line direction where needed.
- An explicit account ledger does not ingest generic `data.transactions` for the same account; this prevents double counting.

## General Journal and Trial Balance Relationship

`ledger/General Journal.html` is the journal-level audit view. It renders:

1. Every `checkingLedgerTransactions` record as a two-line GJ entry.
2. Every `supplementalJournalEntries` record as the specified posting lines.

`ledger/Trial Balance.html` is an **activity trial balance**. It:

- Excludes opening balances.
- Posts BofA statement transactions using the same debit/credit logic as the General Journal.
- Posts all supplemental GJ lines.
- Displays debit or credit balances by account.
- Must have equal totals.

`2999 Unclassified activity (suspense)` is a real chart account and must appear only once in the Trial Balance. Its purpose is to hold activity that is known to exist but cannot yet be assigned to a final account.

When a missing statement arrives:

1. Identify the correct account.
2. Replace the suspense line in the related GJ entry with that real account.
3. Update the source document list on the correct line.
4. Update the account ledger `journalEntry` references as needed.
5. Verify Trial Balance still balances.

## Wells Fargo Example

The September 2026 Wells documents established this evidence chain:

| Activity | Debit | Credit | Source evidence |
| --- | --- | --- | --- |
| Everyday Checking payroll | `1001 Wells Fargo Everyday Checking` | `4000 CRC Services payroll income` | `WellsFargo-2026-09_0009.pdf` |
| Way2Save interest | `1005 Way2Save Savings` | `4001 Bank interest income` | `WellsFargo-2026-08_0805.pdf` |
| AT&T charge | `5006 AT&T mobility` | `2107 Active Cash` | `WellsFargo-2026-09_9110.pdf` |
| Active Cash payment | `2107 Active Cash` | `1001 Everyday Checking` | Each side cites its own Wells statement PDF |

The checking statement also documents two ATM withdrawals. They are posted to `2999` until the user classifies them.

## GM Rewards Example

GM Rewards `2104` was reconciled from the Barclays statement:

```text
Opening balance        $700.00 credit
09/01 payment           $30.00 debit
09/08 interest          $10.58 credit
Closing balance        $680.58 credit
```

The September 1 payment is backed by the BofA statement and uses `GJ-0012`. The September 8 interest charge is `GJ-0046`, debiting `5001 Credit card interest expense` and crediting `2104`.

Post-statement activity that could not be confirmed against the GM statement was moved to suspense. Do not reassign it to GM until a supporting statement confirms it.

## Front-End Behavior

### Table controls

`scripts/accounting.js` exports `window.setupLedgerTableControls(table, body)`.

It provides:

- Sort icons: first click ascending, second click descending.
- Excel-like filter dropdowns: searchable unique values, Select All, Clear, Apply.
- Filter menus are fixed and clamped to the viewport, so they remain visible while scrolling.

Do not hand-copy another sort/filter implementation into a new ledger page. Use the shared account-ledger pattern.

### Styling

`ledger/account-ledger.css` is shared by numbered account pages and common table structures.

The General Journal adds local rules for:

- White debit/credit posting rows, without zebra bands.
- Indented credit account names.
- Gray italic description/comment rows.

Keep the compact accounting tables readable. Do not increase font size or add permanent text filter inputs without discussing the change; the current dropdown behavior was deliberately chosen to resemble Excel.

## Validation Checklist

Run this after any meaningful accounting change.

### Data validation

1. Use editor diagnostics on `data/accounts.json` and every edited script/page.
2. Confirm JSON parses:

```powershell
Get-Content -Raw data/accounts.json | ConvertFrom-Json | Out-Null
```

3. Confirm every supplemental journal entry balances:

```powershell
$data = Get-Content -Raw data/accounts.json | ConvertFrom-Json
$data.supplementalJournalEntries | ForEach-Object {
  $debits = ($_.lines | Measure-Object debitCents -Sum).Sum
  $credits = ($_.lines | Measure-Object creditCents -Sum).Sum
  [pscustomobject]@{ Entry = $_.number; Balanced = ($debits -eq $credits) }
}
```

### Browser validation

Use the local server and browser tools to verify:

1. The account ledger opening, transaction sequence, and closing balance agree with the source statement.
2. The General Journal displays the correct `GJ-####`, source document(s), postings, and description row.
3. The Trial Balance debit and credit totals are equal with no visible error.
4. Budget recurrence appears on the correct future dates and amount.
5. Sort and filter controls still work after renderer changes.

### Git validation

Before committing:

```powershell
git diff --check
git status --short
```

Do not commit source PDFs without user approval when they were just added locally. When the user wants cross-computer access, stage the source PDFs with the related data changes and push the branch.

## Decision Rules for Future AI Work

1. Prefer source evidence over inference.
2. Ask one focused question only when evidence cannot distinguish between real account classifications.
3. Use suspense, not an invented account, for unresolved activity.
4. Add a new chart account only for a distinct asset, liability, income, expense, or documented counterparty that needs its own ledger.
5. Preserve GJ references. They are the link between the General Journal and account ledgers.
6. Preserve source-document provenance at the posting-line level.
7. Keep statement-reconciled historical ledgers separate from projected budget activity.
8. Do not put a projected payment into the General Journal or Trial Balance until it is completed and supported by evidence.
9. Keep source filenames stable. Renaming a PDF requires updating every GJ line that cites it.
10. Validate in a live browser whenever a rendered accounting page or its interaction changes.