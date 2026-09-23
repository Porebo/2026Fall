(function () {
  var dataUrl = window.ACCOUNTING_CONFIG && window.ACCOUNTING_CONFIG.dataUrl || "data/accounts.json";
  var currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
  var sortDirections = { accounts: "asc", transactions: "desc", journal: "desc" };

  function compareDates(a, b, direction) {
    return direction === "asc" ? a.localeCompare(b) : b.localeCompare(a);
  }

  function updateSortHeaders() {
    Object.keys(sortDirections).forEach(function (table) {
      var header = document.querySelector('[data-sort-header="' + table + '"]');
      if (!header) {
        return;
      }
      var ascending = sortDirections[table] === "asc";
      header.setAttribute("aria-sort", ascending ? "ascending" : "descending");
      header.querySelector(".sort-arrow").textContent = ascending ? "▲" : "▼";
    });
  }

  function setupSorting(data) {
    var renderers = { accounts: renderAccounts, transactions: renderTransactions, journal: renderJournal };
    document.querySelectorAll("[data-sort]").forEach(function (button) {
      button.addEventListener("click", function () {
        var table = button.getAttribute("data-sort");
        sortDirections[table] = sortDirections[table] === "asc" ? "desc" : "asc";
        renderers[table](data);
        updateSortHeaders();
      });
    });
    updateSortHeaders();
  }

  function money(cents) {
    return currency.format(cents / 100);
  }

  function date(value) {
    if (!value) {
      return "-";
    }
    return value;
  }

  function accountLabel(account) {
    return account.name + (account.lastFour ? " ending in " + account.lastFour : "");
  }

  function setText(id, value) {
    var element = document.getElementById(id);
    if (element) {
      element.textContent = value;
    }
  }

  function makeCell(text, className) {
    var cell = document.createElement("td");
    cell.textContent = text;
    if (className) {
      cell.className = className;
    }
    return cell;
  }

  function remainingMinimumDue(account) {
    return Math.max(0, account.minimumDueCents - account.completedPaymentCents);
  }

  function renderAccounts(data) {
    var body = document.getElementById("account-rows");
    body.innerHTML = "";
    var accounts = data.accounts.filter(function (account) {
      return account.balanceCents !== 0;
    }).sort(function (a, b) {
      return a.dueDate.localeCompare(b.dueDate);
    });

    if (accounts.length === 0) {
      var emptyRow = document.createElement("tr");
      var emptyCell = makeCell("No upcoming obligations.");
      emptyCell.colSpan = 7;
      emptyRow.appendChild(emptyCell);
      body.appendChild(emptyRow);
      return;
    }

    accounts.forEach(function (account) {
      var row = document.createElement("tr");
      var status = account.status === "paid" ? "Paid" : "Open";
      var statusClass = account.status === "paid" ? "status status--paid" : "status status--open";

      row.appendChild(makeCell(account.bank));
      row.appendChild(makeCell(accountLabel(account)));
      row.appendChild(makeCell(date(account.dueDate)));
      row.appendChild(makeCell(money(remainingMinimumDue(account)), "amount"));
      row.appendChild(makeCell(money(account.balanceCents), "amount"));
      row.appendChild(makeCell(date(account.completedPaymentDate)));
      row.appendChild(makeCell(status, statusClass));
      body.appendChild(row);
    });
  }

  function renderTransactions(data) {
    var body = document.getElementById("transaction-rows");
    body.innerHTML = "";
    var accounts = {};
    data.accounts.forEach(function (account) {
      accounts[account.id] = account;
    });

    data.transactions.slice().sort(function (a, b) {
      return b.date.localeCompare(a.date);
    }).forEach(function (transaction) {
      var account = accounts[transaction.accountId];
      var row = document.createElement("tr");
      row.appendChild(makeCell(date(transaction.date)));
      row.appendChild(makeCell(account ? accountLabel(account) : transaction.accountId));
      row.appendChild(makeCell(transaction.description));
      row.appendChild(makeCell(money(transaction.amountCents), "amount"));
      row.appendChild(makeCell(money(transaction.balanceAfterCents), "amount"));
      body.appendChild(row);
    });
  }

  function getChartAccount(data, accountId) {
    return data.chartOfAccounts.find(function (account) {
      return account.id === accountId;
    });
  }

  function buildActivity(data) {
    var activity = {};
    data.chartOfAccounts.forEach(function (account) {
      activity[account.id] = { debitCents: 0, creditCents: 0 };
    });

    data.journalEntries.forEach(function (entry) {
      entry.lines.forEach(function (line) {
        if (!activity[line.accountId]) {
          activity[line.accountId] = { debitCents: 0, creditCents: 0 };
        }
        activity[line.accountId].debitCents += line.debitCents;
        activity[line.accountId].creditCents += line.creditCents;
      });
    });

    return activity;
  }

  function signedMoney(cents) {
    return cents < 0 ? "-" + money(Math.abs(cents)) : money(cents);
  }

  function renderJournal(data) {
    var body = document.getElementById("journal-rows");
    body.innerHTML = "";
    data.journalEntries.slice().sort(function (a, b) {
      return b.date.localeCompare(a.date);
    }).forEach(function (entry) {
      entry.lines.forEach(function (line) {
        var account = getChartAccount(data, line.accountId);
        var row = document.createElement("tr");
        row.appendChild(makeCell(date(entry.date)));
        row.appendChild(makeCell(entry.description));
        row.appendChild(makeCell(account ? account.name : line.accountId));
        row.appendChild(makeCell(money(line.debitCents), "amount"));
        row.appendChild(makeCell(money(line.creditCents), "amount"));
        body.appendChild(row);
      });
    });
  }

  function renderLedger(data) {
    var body = document.getElementById("ledger-rows");
    var activity = buildActivity(data);
    body.innerHTML = "";

    data.chartOfAccounts.forEach(function (account) {
      var accountActivity = activity[account.id];
      var row = document.createElement("tr");
      row.appendChild(makeCell(account.code));
      row.appendChild(makeCell(account.name));
      row.appendChild(makeCell(account.type));
      row.appendChild(makeCell(money(accountActivity.debitCents), "amount"));
      row.appendChild(makeCell(money(accountActivity.creditCents), "amount"));
      row.appendChild(makeCell(signedMoney(accountActivity.debitCents - accountActivity.creditCents), "amount"));
      body.appendChild(row);
    });
  }

  function renderTrialBalance(data) {
    var body = document.getElementById("trial-balance-rows");
    var activity = buildActivity(data);
    var totalDebits = 0;
    var totalCredits = 0;
    body.innerHTML = "";

    data.chartOfAccounts.forEach(function (account) {
      var accountActivity = activity[account.id];
      var netActivity = accountActivity.debitCents - accountActivity.creditCents;
      if (netActivity === 0) {
        return;
      }

      var debitBalance = netActivity > 0 ? netActivity : 0;
      var creditBalance = netActivity < 0 ? Math.abs(netActivity) : 0;
      totalDebits += debitBalance;
      totalCredits += creditBalance;
      var row = document.createElement("tr");
      row.appendChild(makeCell(account.code));
      row.appendChild(makeCell(account.name));
      row.appendChild(makeCell(money(debitBalance), "amount"));
      row.appendChild(makeCell(money(creditBalance), "amount"));
      body.appendChild(row);
    });

    setText("trial-balance-debits", money(totalDebits));
    setText("trial-balance-credits", money(totalCredits));
    setText("trial-balance-status", totalDebits === totalCredits ? "Balanced" : "Out of balance");
  }

  function render(data) {
    var totals = data.accounts.reduce(function (result, account) {
      result.minimumDueCents += remainingMinimumDue(account);
      result.balanceCents += account.balanceCents;
      result.paidCents += account.completedPaymentCents;
      return result;
    }, { minimumDueCents: 0, balanceCents: 0, paidCents: 0 });

    setText("as-of", data.asOf);
    setText("minimum-due-total", money(totals.minimumDueCents));
    setText("balance-total", money(totals.balanceCents));
    setText("paid-total", money(totals.paidCents));
    setText("account-count", String(data.accounts.length));
    renderAccounts(data);
    renderTransactions(data);
    renderJournal(data);
    renderLedger(data);
    renderTrialBalance(data);
  }

  fetch(dataUrl)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Could not load accounting data.");
      }
      return response.json();
    })
    .then(render)
    .catch(function (error) {
      var message = document.getElementById("accounting-error");
      message.hidden = false;
      message.textContent = error.message;
    });
}());
