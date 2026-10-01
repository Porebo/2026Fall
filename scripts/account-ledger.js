(function () {
  var currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
  var page = document.body;

  function money(cents) {
    return currency.format(Math.abs(cents) / 100);
  }

  function balanceMoney(cents) {
    return currency.format(cents / 100);
  }

  function institution(account, detail) {
    if (detail && detail.bank) {
      return detail.bank;
    }
    var names = {
      "cash-checking": "Bank of America",
      "wells-fargo-checking": "Wells Fargo",
      "capital-one-checking": "Capital One",
      "other-funding-account": "Unspecified",
      "bofa-savings-3435": "Bank of America",
      "crc-payroll-income": "CRC Services",
      "gm-marketplace-expense": "GM Marketplace",
      "credit-card-interest-expense": "Various institutions",
      "spouse-support-irene": "Personal",
      "gardening-expense": "Personal",
      "church-tithing": "Church of Jesus Christ"
    };
    return names[account.id] || account.name;
  }

  function accountPath(account) {
    return account.code + ".html";
  }

  function makeCell(text, className) {
    var cell = document.createElement("td");
    cell.textContent = text;
    if (className) {
      cell.className = className;
    }
    return cell;
  }

  function makeJournalReference(number) {
    var cell = document.createElement("td");
    if (!number || number === "-") {
      cell.textContent = "-";
      return cell;
    }
    var link = document.createElement("a");
    link.href = "General Journal.html#" + encodeURIComponent(number);
    link.textContent = number;
    cell.appendChild(link);
    return cell;
  }

  function renderIndex(data) {
    var body = document.getElementById("ledger-index-rows");
    if (!body) {
      return;
    }
    var details = {};
    data.accounts.forEach(function (account) {
      details[account.id] = account;
    });
    body.innerHTML = "";
    data.chartOfAccounts.slice().sort(function (a, b) {
      return Number(a.code) - Number(b.code);
    }).forEach(function (account) {
      var row = document.createElement("tr");
      var codeCell = makeCell(account.code, "amount");
      var nameCell = document.createElement("td");
      var link = document.createElement("a");
      link.href = accountPath(account);
      link.textContent = account.name;
      nameCell.appendChild(link);
      row.appendChild(codeCell);
      row.appendChild(nameCell);
      row.appendChild(makeCell(institution(account, details[account.id])));
      row.appendChild(makeCell(account.type));
      body.appendChild(row);
    });
  }

  function ensureAccountLayout() {
    if (!document.getElementById("account-ledger-styles")) {
      var styles = document.createElement("link");
      styles.id = "account-ledger-styles";
      styles.rel = "stylesheet";
      styles.href = "account-ledger.css";
      document.head.appendChild(styles);
    }
    page.innerHTML = "<main class=\"page accounting-page\"><nav class=\"breadcrumb\"><a href=\"../index.html\">Home</a> / <a href=\"0000.html\">Ledger Index</a></nav><header class=\"hero\"><p class=\"eyebrow\">Account Ledger</p><h1 id=\"account-name\">Loading...</h1><p class=\"lede\">Account <strong id=\"account-code\">-</strong> &middot; <span id=\"account-institution\">-</span></p></header><div id=\"ledger-error\" class=\"accounting-error\" hidden></div><section class=\"card accounting-section\"><p class=\"accounting-meta\">Type: <span id=\"account-type\">-</span> &middot; Normal balance: <span id=\"account-normal-balance\">-</span></p><div class=\"accounting-table-wrap\"><table class=\"accounting-table accounting-table--compact\"><thead><tr><th><span class=\"ledger-header\">Date <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"0\" aria-label=\"Sort date\" title=\"Sort date\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"0\" aria-label=\"Filter date\" title=\"Filter date\">&#9662;</button></span></th><th><span class=\"ledger-header\">Ref. <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"1\" aria-label=\"Sort reference\" title=\"Sort reference\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"1\" aria-label=\"Filter reference\" title=\"Filter reference\">&#9662;</button></span></th><th><span class=\"ledger-header\">Code <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"2\" aria-label=\"Sort code\" title=\"Sort code\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"2\" aria-label=\"Filter code\" title=\"Filter code\">&#9662;</button></span></th><th><span class=\"ledger-header\">Status <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"3\" aria-label=\"Sort status\" title=\"Sort status\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"3\" aria-label=\"Filter status\" title=\"Filter status\">&#9662;</button></span></th><th><span class=\"ledger-header\">Description <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"4\" aria-label=\"Sort description\" title=\"Sort description\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"4\" aria-label=\"Filter description\" title=\"Filter description\">&#9662;</button></span></th><th><span class=\"ledger-header\">Debit (Dr) <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"5\" aria-label=\"Sort debit\" title=\"Sort debit\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"5\" aria-label=\"Filter debit\" title=\"Filter debit\">&#9662;</button></span></th><th><span class=\"ledger-header\">Credit (Cr) <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"6\" aria-label=\"Sort credit\" title=\"Sort credit\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"6\" aria-label=\"Filter credit\" title=\"Filter credit\">&#9662;</button></span></th><th><span class=\"ledger-header\">Balance <button type=\"button\" class=\"ledger-sort-button\" data-ledger-sort=\"7\" aria-label=\"Sort balance\" title=\"Sort balance\">&#8597;</button><button type=\"button\" class=\"ledger-filter-button\" data-ledger-filter-button=\"7\" aria-label=\"Filter balance\" title=\"Filter balance\">&#9662;</button></span></th></tr></thead><tbody id=\"account-ledger-rows\"></tbody></table></div></section></main>";
  }

  function renderAccount(data, accountId) {
    var account = data.chartOfAccounts.find(function (item) {
      return item.id === accountId;
    });
    if (!account) {
      return;
    }
    ensureAccountLayout();
    var breadcrumb = document.querySelector(".breadcrumb");
    var trialBalanceLink = document.createElement("a");
    trialBalanceLink.href = "Trial%20Balance.html";
    trialBalanceLink.textContent = "Trial Balance";
    breadcrumb.appendChild(document.createTextNode(" / "));
    breadcrumb.appendChild(trialBalanceLink);
    var detail = data.accounts.find(function (item) {
      return item.id === accountId;
    });
    document.title = account.code + " Ledger";
    document.getElementById("account-code").textContent = account.code;
    document.getElementById("account-name").textContent = account.name;
    document.getElementById("account-institution").textContent = institution(account, detail);
    document.getElementById("account-type").textContent = account.type;
    document.getElementById("account-normal-balance").textContent = account.normalBalance;

    var hasExplicitLedgerEntries = detail && detail.ledgerEntries;
    var entries = hasExplicitLedgerEntries ? detail.ledgerEntries.map(function (entry, index) {
      return { date: entry.date, code: account.code, description: entry.description, amountCents: entry.amountCents, balanceAfterCents: entry.balanceAfterCents, isDebit: entry.isDebit, journalEntry: entry.journalEntry || "-", sequence: index };
    }) : (data.checkingLedgerTransactions || []).filter(function (entry) {
      return accountId === "cash-checking" || entry.code === account.code;
    }).map(function (entry, index) {
      return { date: entry.date, code: entry.code || account.code, description: entry.description, amountCents: entry.amountCents, balanceAfterCents: null, journalEntry: "GJ-" + String(index + 1).padStart(4, "0"), sequence: index };
    });
    if (!hasExplicitLedgerEntries) {
      (data.transactions || []).filter(function (entry) {
        return accountId !== "cash-checking" && entry.accountId === accountId;
      }).forEach(function (entry, index) {
        entries.push({ date: entry.date, code: account.code, description: entry.description, amountCents: entry.amountCents, balanceAfterCents: entry.balanceAfterCents, journalEntry: entry.journalEntry || "-", sequence: 100000 + index });
      });
    }
    var representedJournalEntries = {};
    entries.forEach(function (entry) {
      if (entry.journalEntry && entry.journalEntry !== "-") {
        representedJournalEntries[entry.journalEntry] = true;
      }
    });
    (data.supplementalJournalEntries || []).forEach(function (journalEntry, entryIndex) {
      journalEntry.lines.forEach(function (line, lineIndex) {
        if (line.accountId !== accountId || representedJournalEntries[journalEntry.number]) {
          return;
        }
        entries.push({
          date: journalEntry.date,
          code: account.code,
          description: journalEntry.description,
          amountCents: line.debitCents || line.creditCents,
          balanceAfterCents: null,
          isDebit: line.debitCents > 0,
          journalEntry: journalEntry.number,
          sequence: 200000 + entryIndex * 2 + lineIndex
        });
      });
    });
    entries.sort(function (a, b) {
      return a.date.localeCompare(b.date) || (a.isOpeningBalance ? -1 : 0) || a.sequence - b.sequence;
    });
    var openingBalanceCents = accountId === "cash-checking" && data.cashBalanceSnapshot
      ? data.cashBalanceSnapshot.balanceCents
      : detail && detail.openingBalanceCents;
    var openingBalanceDate = accountId === "cash-checking" && data.cashBalanceSnapshot
      ? data.cashBalanceSnapshot.asOf
      : detail && detail.openingBalanceDate;
    if (openingBalanceCents != null && openingBalanceDate) {
      var runningBalanceCents = openingBalanceCents;
      var openingEntry = {
        date: openingBalanceDate,
        code: "-",
        description: "Beginning balance - " + institution(account, detail),
        amountCents: openingBalanceCents,
        balanceAfterCents: runningBalanceCents,
        journalEntry: "-",
        isOpeningBalance: true,
        sequence: -1
      };
      entries.push(openingEntry);
      entries.sort(function (a, b) {
        return a.date.localeCompare(b.date) || (a.isOpeningBalance ? -1 : 0) || a.sequence - b.sequence;
      });
      if (accountId === "cash-checking") {
        var openingBalanceReached = false;
        entries.forEach(function (entry) {
          if (entry.isOpeningBalance) {
            openingBalanceReached = true;
            return;
          }
          if (!openingBalanceReached) {
            entry.balanceAfterCents = null;
            return;
          }
          runningBalanceCents += entry.isDebit === undefined
            ? entry.amountCents
            : entry.isDebit ? entry.amountCents : -entry.amountCents;
          entry.balanceAfterCents = runningBalanceCents;
        });
      }
    }

    var body = document.getElementById("account-ledger-rows");
    body.innerHTML = "";
    if (entries.length === 0) {
      var empty = makeCell("No recorded activity is available for this account.");
      empty.colSpan = 8;
      body.appendChild(document.createElement("tr")).appendChild(empty);
      return;
    }
    entries.forEach(function (entry, index) {
      var row = document.createElement("tr");
      row.appendChild(makeCell(entry.date));
      row.appendChild(makeJournalReference(entry.journalEntry || "-"));
      row.appendChild(makeCell(entry.code));
      row.appendChild(makeCell(entry.isOpeningBalance ? "-" : "C " + String.fromCharCode(10003)));
      row.appendChild(makeCell(entry.description));
      var debitEntry = entry.isDebit === undefined
        ? (entry.isOpeningBalance ? account.normalBalance !== "credit" : entry.amountCents < 0)
        : entry.isDebit;
      row.appendChild(makeCell(debitEntry ? money(entry.amountCents) : "-", entry.amountCents < 0 ? "amount amount--negative" : "amount"));
      row.appendChild(makeCell(!debitEntry ? money(entry.amountCents) : "-", "amount"));
      row.appendChild(makeCell(entry.balanceAfterCents == null ? "-" : balanceMoney(entry.balanceAfterCents), "amount"));
      body.appendChild(row);
    });
    window.setupLedgerTableControls(document.querySelector(".accounting-table--compact"), body);
  }

  function loadLedgerData() {
    fetch("../data/accounts.json").then(function (response) {
    if (!response.ok) {
      throw new Error("Could not load ledger data.");
    }
    return response.json();
    }).then(function (data) {
    if (page.dataset.ledgerIndex === "true") {
      renderIndex(data);
      return;
    }
    renderAccount(data, page.dataset.accountId);
    }).catch(function (error) {
    var target = document.getElementById("ledger-error");
    if (target) {
      target.hidden = false;
      target.textContent = error.message;
    }
    });
  }

  if (page.dataset.ledgerIndex === "true") {
    loadLedgerData();
    return;
  }

  page.dataset.accountingView = "account-ledger";
  window.ACCOUNTING_CONFIG = { dataUrl: "../data/accounts.json" };
  if (window.setupLedgerTableControls) {
    loadLedgerData();
  } else {
    var controlsScript = document.createElement("script");
    controlsScript.src = "../scripts/accounting.js";
    controlsScript.addEventListener("load", loadLedgerData);
    document.head.appendChild(controlsScript);
  }
}());