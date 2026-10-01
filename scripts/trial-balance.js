(function () {
  var currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });

  function money(cents) {
    return currency.format(cents / 100);
  }

  function makeCell(text, className) {
    var cell = document.createElement("td");
    cell.textContent = text;
    if (className) {
      cell.className = className;
    }
    return cell;
  }

  fetch("../data/accounts.json").then(function (response) {
    if (!response.ok) {
      throw new Error("Could not load trial balance data.");
    }
    return response.json();
  }).then(function (data) {
    var body = document.getElementById("trial-balance-rows");
    var accountsByCode = {};
    var accountsById = {};
    var activity = {};
    var currentBalancesById = {};
    var suspense = { id: "unclassified-bank-activity", code: "2999", name: "Unclassified bank activity (suspense)" };

    data.chartOfAccounts.forEach(function (account) {
      accountsByCode[account.code] = account;
      accountsById[account.id] = account;
      activity[account.id] = { account: account, debitCents: 0, creditCents: 0 };
    });
    (data.accounts || []).forEach(function (account) {
      currentBalancesById[account.id] = account.balanceCents;
    });
    if (data.cashBalanceSnapshot) {
      currentBalancesById[data.cashBalanceSnapshot.accountId] = data.cashBalanceSnapshot.balanceCents;
    }
    suspense = accountsByCode["2999"] || suspense;

    function post(account, debitCents, creditCents) {
      if (!activity[account.id]) {
        activity[account.id] = { account: account, debitCents: 0, creditCents: 0 };
      }
      activity[account.id].debitCents += debitCents;
      activity[account.id].creditCents += creditCents;
    }

    (data.checkingLedgerTransactions || []).forEach(function (transaction) {
      var amountCents = Math.abs(transaction.amountCents);
      var counterpart = accountsByCode[transaction.code] || suspense;
      var cash = accountsById["cash-checking"];
      if (transaction.amountCents < 0) {
        post(counterpart, amountCents, 0);
        post(cash, 0, amountCents);
      } else {
        post(cash, amountCents, 0);
        post(counterpart, 0, amountCents);
      }
    });

    (data.supplementalJournalEntries || []).forEach(function (entry) {
      entry.lines.forEach(function (line) {
        post(accountsById[line.accountId], line.debitCents, line.creditCents);
      });
    });

    var totalDebits = 0;
    var totalCredits = 0;
    body.innerHTML = "";
    Object.keys(activity).map(function (accountId) {
      return activity[accountId];
    }).sort(function (first, second) {
      return Number(first.account.code) - Number(second.account.code);
    }).forEach(function (entry) {
      var isBalanceSheetAccount = entry.account.type === "asset" || entry.account.type === "liability";
      var currentBalanceCents = isBalanceSheetAccount ? currentBalancesById[entry.account.id] : null;
      var row = document.createElement("tr");
      var codeCell = document.createElement("td");
      var accountLink = document.createElement("a");
      accountLink.href = entry.account.code + ".html";
      accountLink.textContent = entry.account.code;
      codeCell.appendChild(accountLink);
      row.appendChild(codeCell);
      row.appendChild(makeCell(entry.account.name));
      row.appendChild(makeCell(currentBalanceCents == null ? "-" : money(currentBalanceCents), "amount"));
      body.appendChild(row);
      totalDebits += entry.debitCents;
      totalCredits += entry.creditCents;
    });

    if (totalDebits !== totalCredits) {
      throw new Error("Trial balance totals do not match.");
    }
  }).catch(function (exception) {
    var error = document.getElementById("trial-balance-error");
    error.hidden = false;
    error.textContent = exception.message;
  });
}());