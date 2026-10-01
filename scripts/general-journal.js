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

  function makeSourceCell(sourceDocuments) {
    var cell = document.createElement("td");
    var documents = Array.isArray(sourceDocuments) ? sourceDocuments : sourceDocuments ? [sourceDocuments] : [];
    if (documents.length === 0) {
      return cell;
    }
    documents.forEach(function (sourceDocument, index) {
      if (index > 0) {
        cell.appendChild(document.createTextNode(", "));
      }
      if (/\.pdf$/i.test(sourceDocument)) {
        var link = document.createElement("a");
        link.href = sourceDocument;
        link.textContent = sourceDocument;
        cell.appendChild(link);
        return;
      }
      cell.appendChild(document.createTextNode(sourceDocument));
    });
    return cell;
  }

  function appendLine(body, entryNumber, sourceDocument, post, date, account, debitCents, creditCents, creditAccount) {
    var row = document.createElement("tr");
    if (entryNumber) {
      row.id = entryNumber;
    }
    row.appendChild(makeCell(entryNumber));
    row.appendChild(makeSourceCell(sourceDocument));
    row.appendChild(makeCell(post));
    row.appendChild(makeCell(date));
    row.appendChild(makeCell(account, creditAccount ? "journal-credit-account" : ""));
    row.appendChild(makeCell(debitCents ? money(debitCents) : "", "amount"));
    row.appendChild(makeCell(creditCents ? money(creditCents) : "", "amount"));
    body.appendChild(row);
  }

  function appendDescription(body, description) {
    var row = document.createElement("tr");
    row.className = "journal-description-row";
    row.appendChild(makeCell(""));
    row.appendChild(makeCell(""));
    row.appendChild(makeCell(""));
    row.appendChild(makeCell(""));
    row.appendChild(makeCell(description));
    row.appendChild(makeCell(""));
    row.appendChild(makeCell(""));
    body.appendChild(row);
  }

  function journalDescription(transaction) {
    if (transaction.id.indexOf("payroll") !== -1) {
      var dayOfMonth = Number(transaction.date.slice(-2));
      return "CRC payroll - " + (dayOfMonth <= 15 ? "1st" : "2nd") + " of the month";
    }
    return transaction.description;
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
    var accountsById = {};
    var totalDebits = 0;
    var totalCredits = 0;
    data.chartOfAccounts.forEach(function (account) {
      accountsByCode[account.code] = account;
      accountsById[account.id] = account;
    });
    body.innerHTML = "";
    (data.checkingLedgerTransactions || []).forEach(function (transaction, index) {
      var amountCents = Math.abs(transaction.amountCents);
      var mappedAccount = accountsByCode[transaction.code];
      var counterpart = mappedAccount
        ? mappedAccount.name
        : "Unclassified bank activity";
      var counterpartPost = mappedAccount ? mappedAccount.code : "";
      var cashAccount = "Bank of America checking account";
      var entryNumber = "GJ-" + String(index + 1).padStart(4, "0");
      if (transaction.amountCents < 0) {
        appendLine(body, entryNumber, ["BofA-2026-09-7632.pdf"], counterpartPost, transaction.date, counterpart, amountCents, 0, false);
        appendLine(body, "", ["BofA-2026-09-7632.pdf"], "1000", "", cashAccount, 0, amountCents, true);
      } else {
        appendLine(body, entryNumber, ["BofA-2026-09-7632.pdf"], "1000", transaction.date, cashAccount, amountCents, 0, false);
        appendLine(body, "", ["BofA-2026-09-7632.pdf"], counterpartPost, "", counterpart, 0, amountCents, true);
      }
      appendDescription(body, journalDescription(transaction));
      totalDebits += amountCents;
      totalCredits += amountCents;
    });
    (data.supplementalJournalEntries || []).forEach(function (entry) {
      entry.lines.forEach(function (line, index) {
        var account = accountsById[line.accountId];
        appendLine(
          body,
          index === 0 ? entry.number : "",
          line.sourceDocuments || (entry.sourceDocument ? [entry.sourceDocument] : []),
          account ? account.code : "",
          index === 0 ? entry.date : "",
          account ? account.name : line.accountId,
          line.debitCents,
          line.creditCents,
          line.creditCents > 0
        );
        totalDebits += line.debitCents;
        totalCredits += line.creditCents;
      });
      appendDescription(body, entry.description);
    });
    document.getElementById("journal-total-debits").textContent = money(totalDebits);
    document.getElementById("journal-total-credits").textContent = money(totalCredits);
    if (totalDebits !== totalCredits) {
      error.hidden = false;
      error.textContent = "Journal totals are not balanced.";
    }
    var target = window.location.hash
      ? document.getElementById(window.location.hash.slice(1))
      : null;
    if (target) {
      target.scrollIntoView();
    }
  }).catch(function (exception) {
    var error = document.getElementById("journal-error");
    error.hidden = false;
    error.textContent = exception.message;
  });
}());