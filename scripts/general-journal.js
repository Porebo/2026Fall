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

  function appendLine(body, entryNumber, date, description, account, debitCents, creditCents) {
    var row = document.createElement("tr");
    row.appendChild(makeCell(entryNumber));
    row.appendChild(makeCell(date));
    row.appendChild(makeCell(description));
    row.appendChild(makeCell(account));
    row.appendChild(makeCell(debitCents ? money(debitCents) : "", "amount"));
    row.appendChild(makeCell(creditCents ? money(creditCents) : "", "amount"));
    body.appendChild(row);
  }

  fetch("../data/accounts.json").then(function (response) {
    if (!response.ok) {
      throw new Error("Could not load journal data.");
    }
    return response.json();
  }).then(function (data) {
    var body = document.getElementById("journal-rows");
    var error = document.getElementById("journal-error");
    var accountsByCode = {};
    var totalDebits = 0;
    var totalCredits = 0;
    data.chartOfAccounts.forEach(function (account) {
      accountsByCode[account.code] = account;
    });
    body.innerHTML = "";
    (data.checkingLedgerTransactions || []).forEach(function (transaction, index) {
      var amountCents = Math.abs(transaction.amountCents);
      var mappedAccount = accountsByCode[transaction.code];
      var counterpart = mappedAccount
        ? mappedAccount.code + " " + mappedAccount.name
        : "Unclassified bank activity";
      var cashAccount = "1000 Bank of America checking account";
      var entryNumber = "JE-" + String(index + 1).padStart(4, "0");
      if (transaction.amountCents < 0) {
        appendLine(body, entryNumber, transaction.date, transaction.description, counterpart, amountCents, 0);
        appendLine(body, "", "", "", cashAccount, 0, amountCents);
      } else {
        appendLine(body, entryNumber, transaction.date, transaction.description, cashAccount, amountCents, 0);
        appendLine(body, "", "", "", counterpart, 0, amountCents);
      }
      totalDebits += amountCents;
      totalCredits += amountCents;
    });
    document.getElementById("journal-total-debits").textContent = money(totalDebits);
    document.getElementById("journal-total-credits").textContent = money(totalCredits);
    if (totalDebits !== totalCredits) {
      error.hidden = false;
      error.textContent = "Journal totals are not balanced.";
    }
  }).catch(function (exception) {
    var error = document.getElementById("journal-error");
    error.hidden = false;
    error.textContent = exception.message;
  });
}());