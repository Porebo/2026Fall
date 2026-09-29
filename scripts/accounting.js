(function () {
  var dataUrl = window.ACCOUNTING_CONFIG && window.ACCOUNTING_CONFIG.dataUrl || "data/accounts.json";
  var currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
  var sortDirections = { accounts: "asc", transactions: "desc", journal: "desc" };
  var github = window.ACCOUNTING_CONFIG && window.ACCOUNTING_CONFIG.github;
  var tokenKey = "accounting.githubToken";
  var token = readToken();
  var savedPosted = {};
  var pendingPosted = {};

  function compareDates(a, b, direction) {
    return direction === "asc" ? a.localeCompare(b) : b.localeCompare(a);
  }

  function parseDate(value) {
    var parts = value.split("-");
    return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  }

  function formatDate(value) {
    var month = String(value.getMonth() + 1).padStart(2, "0");
    var day = String(value.getDate()).padStart(2, "0");
    return value.getFullYear() + "-" + month + "-" + day;
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

  function moneyOrDash(cents) {
    return cents == null ? "-" : money(cents);
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

  function makeBalanceCell(cents) {
    var cell = makeCell(moneyOrDash(cents), "amount");
    if (cents != null && cents < 0) {
      cell.classList.add("amount--negative");
    }
    return cell;
  }

  function remainingMinimumDue(account) {
    if (account.minimumDueCents == null) {
      return null;
    }
    return Math.max(0, account.minimumDueCents - account.completedPaymentCents);
  }

  function remainingPlannedPayment(account) {
    var plannedPayment = account.plannedPaymentCents === undefined ? account.minimumDueCents : account.plannedPaymentCents;
    if (plannedPayment == null) {
      return null;
    }
    return Math.max(0, plannedPayment - account.completedPaymentCents);
  }

  function plannedObligationCents(account, data) {
    var chartAccount = getChartAccount(data, account.id);
    var chartCode = chartAccount ? Number(chartAccount.code) : 0;
    var isCreditCard = chartCode >= 2100 && chartCode < 2200;
    var amountDue = account.plannedPaymentCents !== undefined
      ? account.plannedPaymentCents
      : isCreditCard ? account.statementBalanceCents : account.minimumDueCents;

    return amountDue == null ? null : Math.max(0, amountDue - (account.completedPaymentCents || 0));
  }

  function expenseClass(account) {
    return account && account.recurrence && account.recurrence.frequency === "monthly" ? "R" : account ? "F" : "-";
  }

  function getProjectedPaymentEvents(data, startDate, endDate) {
    var events = [];

    data.accounts.forEach(function (account) {
      if (account.recurrence && account.recurrence.frequency === "monthly") {
        var occurrence = parseDate(account.dueDate);
        if (account.status === "paid") {
          occurrence.setMonth(occurrence.getMonth() + 1);
        }

        while (formatDate(occurrence) <= endDate) {
          var occurrenceDate = formatDate(occurrence);
          if (occurrenceDate > startDate) {
            var amountCents = occurrenceDate === account.dueDate
              ? plannedObligationCents(account, data)
              : account.recurrence.amountCents;
            events.push({ type: "payment", date: occurrenceDate, account: account, amountCents: amountCents });
          }
          occurrence.setMonth(occurrence.getMonth() + 1);
        }
      } else if (account.status !== "paid" && account.dueDate > startDate && account.dueDate <= endDate) {
        events.push({ type: "payment", date: account.dueDate, account: account, amountCents: plannedObligationCents(account, data) });
      }
    });

    return events;
  }

  function renderPaycheckSchedule(data) {
    var target = document.getElementById("paycheck-schedule");
    if (!target) {
      return;
    }

    target.innerHTML = "";
    (data.paycheckSchedule || []).forEach(function (paycheck) {
      var item = document.createElement("li");
      var amount = paycheck.amountCents == null ? "" : " - " + money(paycheck.amountCents);
      item.textContent = date(paycheck.date) + " - Paycheck from " + paycheck.employer + amount;
      target.appendChild(item);
    });
  }

  function renderCashRunway(data) {
    var target = document.getElementById("cash-runway");
    var snapshot = data.cashBalanceSnapshot;
    if (!target || !snapshot) {
      return;
    }

    var paymentsSinceSnapshotCents = data.transactions.filter(function (transaction) {
      return transaction.type === "payment" && (!transaction.paidFromAccountId || transaction.paidFromAccountId === snapshot.accountId) && transaction.date > snapshot.asOf && transaction.date < snapshot.nextPaydayDate;
    }).reduce(function (total, transaction) {
      return total + transaction.amountCents;
    }, 0);
    var transfersIntoCheckingCents = data.transactions.filter(function (transaction) {
      return transaction.type === "transfer" && transaction.direction === "in" && transaction.accountId === snapshot.accountId && transaction.date > snapshot.asOf && transaction.date < snapshot.nextPaydayDate;
    }).reduce(function (total, transaction) {
      return total + transaction.amountCents;
    }, 0);
    var plannedTransfersIntoCheckingCents = (data.cashForecastEntries || []).filter(function (entry) {
      return entry.type === "transfer" && entry.direction === "in" && entry.accountId === snapshot.accountId && entry.date > snapshot.asOf && entry.date < snapshot.nextPaydayDate;
    }).reduce(function (total, entry) {
      return total + entry.amountCents;
    }, 0);
    var upcoming = data.accounts.filter(function (account) {
      return account.status !== "paid" && account.dueDate > snapshot.asOf && account.dueDate < snapshot.nextPaydayDate;
    });
    var knownUpcomingCents = 0;
    var unknownUpcoming = [];

    upcoming.forEach(function (account) {
      var amountDue = plannedObligationCents(account, data);
      if (amountDue == null) {
        unknownUpcoming.push(account.name);
        return;
      }
      knownUpcomingCents += amountDue;
    });

    var afterRecordedActivityCents = snapshot.balanceCents - paymentsSinceSnapshotCents + transfersIntoCheckingCents;
    var projectedBalanceCents = afterRecordedActivityCents - knownUpcomingCents + plannedTransfersIntoCheckingCents;
    var projectedAfterPaydayCents = projectedBalanceCents + (snapshot.nextPaydayAmountCents || 0);
    target.replaceChildren();

    [
      snapshot.bank + " balance on " + snapshot.asOf + ": " + money(snapshot.balanceCents),
      "Payments recorded since snapshot: " + money(paymentsSinceSnapshotCents),
      "Transfers into checking since snapshot: " + money(transfersIntoCheckingCents),
      "Remaining before unpaid bills: " + money(afterRecordedActivityCents),
      "Known bills due before " + snapshot.nextPaydayDate + ": " + money(knownUpcomingCents),
      "Planned transfers into checking: " + money(plannedTransfersIntoCheckingCents),
      "Projected balance before next deposit: " + money(projectedBalanceCents),
      "Planned paycheck on " + snapshot.nextPaydayDate + ": " + money(snapshot.nextPaydayAmountCents || 0),
      "Projected balance after next deposit: " + money(projectedAfterPaydayCents)
    ].forEach(function (text) {
      var line = document.createElement("p");
      line.textContent = text;
      target.appendChild(line);
    });

    if (unknownUpcoming.length > 0) {
      var note = document.createElement("p");
      note.textContent = "Not included because the amount is unknown: " + unknownUpcoming.join(", ") + ".";
      target.appendChild(note);
    }
  }

  function renderCheckingLedger(data) {
    var body = document.getElementById("checking-ledger-rows");
    var snapshot = data.cashBalanceSnapshot;
    if (!body || !snapshot) {
      return;
    }

    body.innerHTML = "";
    var balanceCents = snapshot.balanceCents;
    var openingRow = document.createElement("tr");
    openingRow.appendChild(makeCell(date(snapshot.asOf)));
    openingRow.appendChild(makeCell("1"));
    openingRow.appendChild(makeCell("-"));
    openingRow.appendChild(makeCell("-"));
    openingRow.appendChild(makeCell("Beginning balance - " + snapshot.bank));
    openingRow.appendChild(makeBalanceCell(balanceCents));
    openingRow.appendChild(makeCell("-", "amount"));
    openingRow.appendChild(makeBalanceCell(balanceCents));
    body.appendChild(openingRow);

    var referenceNumber = 2;
    data.transactions.filter(function (transaction) {
      var isCheckingPayment = transaction.type === "payment" && (!transaction.paidFromAccountId || transaction.paidFromAccountId === snapshot.accountId);
      var isCheckingDeposit = transaction.type === "transfer" && transaction.direction === "in" && transaction.accountId === snapshot.accountId;
      return (isCheckingPayment || isCheckingDeposit) && transaction.date > snapshot.asOf && transaction.date < snapshot.nextPaydayDate;
    }).sort(function (a, b) {
      return compareDates(a.date, b.date, "asc") || a.id.localeCompare(b.id);
    }).forEach(function (transaction) {
      var isCredit = transaction.type === "payment" || transaction.direction === "out";
      balanceCents += isCredit ? -transaction.amountCents : transaction.amountCents;
      var account = data.accounts.find(function (item) {
        return item.id === transaction.accountId;
      });
      var chartAccount = getChartAccount(data, transaction.accountId);
      var row = document.createElement("tr");
      row.appendChild(makeCell(date(transaction.date)));
      row.appendChild(makeCell(String(referenceNumber)));
      referenceNumber += 1;
      row.appendChild(makeCell(transaction.type === "payment" ? expenseClass(account) : "-"));
      row.appendChild(makeCell("C"));
      row.appendChild(makeCell((account ? account.name : chartAccount ? chartAccount.name : transaction.accountId) + " - " + transaction.description));
      row.appendChild(makeCell(isCredit ? "-" : money(transaction.amountCents), "amount"));
      row.appendChild(makeCell(isCredit ? money(transaction.amountCents) : "-", "amount"));
      row.appendChild(makeBalanceCell(balanceCents));
      body.appendChild(row);
    });

    var paycheckSchedule = data.paycheckSchedule || [];
    var endDate = paycheckSchedule.length ? paycheckSchedule[paycheckSchedule.length - 1].date : snapshot.nextPaydayDate;

    var forecastEvents = getProjectedPaymentEvents(data, snapshot.asOf, endDate);
    (data.cashForecastEntries || []).filter(function (entry) {
      return entry.type === "transfer" && entry.direction === "in" && entry.accountId === snapshot.accountId;
    }).forEach(function (entry) {
      var occurrence = parseDate(entry.date);
      while (formatDate(occurrence) <= endDate) {
        var occurrenceDate = formatDate(occurrence);
        if (occurrenceDate > snapshot.asOf) {
          forecastEvents.push({ type: "transfer", date: occurrenceDate, entry: entry, amountCents: entry.amountCents });
        }
        if (!entry.recurrence || entry.recurrence.frequency !== "monthly") {
          break;
        }
        occurrence.setMonth(occurrence.getMonth() + 1);
      }
    });
    paycheckSchedule.filter(function (paycheck) {
      return paycheck.date > snapshot.asOf;
    }).forEach(function (paycheck) {
      forecastEvents.push({ type: "paycheck", date: paycheck.date, paycheck: paycheck, amountCents: paycheck.amountCents });
    });
    forecastEvents.sort(function (a, b) {
      var dateOrder = compareDates(a.date, b.date, "asc");
      if (dateOrder !== 0) {
        return dateOrder;
      }
      var eventOrder = { payment: 0, transfer: 1, paycheck: 2 };
      return eventOrder[a.type] - eventOrder[b.type];
    }).forEach(function (event) {
      var row = document.createElement("tr");
      row.className = "ledger-row--projected";
      if (event.type === "payment" && event.account.id === "church-tithing") {
        row.classList.add("ledger-row--tithing");
      }
      row.appendChild(makeCell(date(event.date)));
      row.appendChild(makeCell(String(referenceNumber)));
      referenceNumber += 1;
      row.appendChild(makeCell(event.type === "payment" ? expenseClass(event.account) : "-"));
      row.appendChild(makeCell("S"));
      if (event.type === "payment") {
        row.appendChild(makeCell(event.account.name + (event.amountCents == null ? " (amount unknown)" : "")));
        row.appendChild(makeCell("-", "amount"));
        row.appendChild(makeCell(moneyOrDash(event.amountCents), "amount"));
        if (event.amountCents != null) {
          if (balanceCents != null) {
            balanceCents -= event.amountCents;
          }
        } else {
          balanceCents = null;
        }
      } else if (event.type === "transfer") {
        row.appendChild(makeCell(event.entry.description));
        row.appendChild(makeCell(money(event.amountCents), "amount"));
        row.appendChild(makeCell("-", "amount"));
        if (balanceCents != null) {
          balanceCents += event.amountCents;
        }
      } else {
        row.appendChild(makeCell("Paycheck from " + event.paycheck.employer + (event.amountCents == null ? " (amount unknown)" : "")));
        row.appendChild(makeCell(moneyOrDash(event.amountCents), "amount"));
        row.appendChild(makeCell("-", "amount"));
        if (event.amountCents == null || balanceCents == null) {
          balanceCents = null;
        } else {
          balanceCents += event.amountCents;
        }
      }
      row.appendChild(makeBalanceCell(balanceCents));
      body.appendChild(row);
    });
  }

  function renderAccounts(data) {
    var body = document.getElementById("account-rows");
    body.innerHTML = "";
    var accounts = data.accounts.filter(function (account) {
      return account.balanceCents !== 0;
    }).sort(function (a, b) {
      return compareDates(a.dueDate, b.dueDate, sortDirections.accounts);
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
      row.appendChild(makeCell(moneyOrDash(remainingPlannedPayment(account)), "amount"));
      row.appendChild(makeCell(moneyOrDash(account.balanceCents), "amount"));
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
      return compareDates(a.date, b.date, sortDirections.transactions);
    }).forEach(function (transaction) {
      var account = accounts[transaction.accountId];
      var chartAccount = getChartAccount(data, transaction.accountId);
      var row = document.createElement("tr");
      row.appendChild(makeCell(date(transaction.date)));
      row.appendChild(makeCell(account ? accountLabel(account) : chartAccount ? chartAccount.name : transaction.accountId));
      row.appendChild(makeCell(transaction.description));
      row.appendChild(makeCell(money(transaction.amountCents), "amount"));
      row.appendChild(makeCell(transaction.balanceAfterCents == null ? "-" : money(transaction.balanceAfterCents), "amount"));
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

    data.journalEntries.filter(function (entry) {
      return entry.posted;
    }).forEach(function (entry) {
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

  function makePostedCell(data, entry) {
    var cell = document.createElement("td");
    var label = document.createElement("label");
    var box = document.createElement("input");
    var text = document.createElement("span");
    label.className = "posted-toggle";
    box.type = "checkbox";
    box.checked = Boolean(entry.posted);
    box.setAttribute("aria-label", "Posted " + entry.number);

    function showState() {
      text.textContent = entry.posted ? "Yes" : "No";
      text.className = entry.posted ? "status status--paid" : "status status--open";
    }

    box.addEventListener("change", function () {
      entry.posted = box.checked;
      if (savedPosted[entry.id] === entry.posted) {
        delete pendingPosted[entry.id];
      } else {
        pendingPosted[entry.id] = entry.posted;
      }
      showState();
      renderLedger(data);
      renderTrialBalance(data);
      updateSaveControls();
    });

    showState();
    label.appendChild(box);
    label.appendChild(text);
    cell.appendChild(label);
    return cell;
  }

  function renderJournal(data) {
    var body = document.getElementById("journal-rows");
    body.innerHTML = "";
    data.journalEntries.slice().sort(function (a, b) {
      return compareDates(a.date + a.number, b.date + b.number, sortDirections.journal);
    }).forEach(function (entry) {
      entry.lines.forEach(function (line, index) {
        var account = getChartAccount(data, line.accountId);
        var first = index === 0;
        var row = document.createElement("tr");
        row.appendChild(makeCell(first ? entry.number : ""));
        row.appendChild(first ? makePostedCell(data, entry) : makeCell(""));
        row.appendChild(makeCell(first ? date(entry.date) : ""));
        row.appendChild(makeCell(first ? entry.description : ""));
        row.appendChild(makeCell(account ? account.name : line.accountId, line.creditCents > 0 ? "journal-credit" : ""));
        row.appendChild(makeCell(line.debitCents ? money(line.debitCents) : "", "amount"));
        row.appendChild(makeCell(line.creditCents ? money(line.creditCents) : "", "amount"));
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
      var plannedPayment = remainingPlannedPayment(account);
      result.plannedPaymentCents += plannedPayment == null ? 0 : plannedPayment;
      result.balanceCents += account.balanceCents == null ? 0 : account.balanceCents;
      return result;
    }, { plannedPaymentCents: 0, balanceCents: 0, paidCents: 0 });
    totals.paidCents = data.transactions.reduce(function (total, transaction) {
      return total + (transaction.type === "payment" ? transaction.amountCents : 0);
    }, 0);

    setText("as-of", data.asOf);
    setText("minimum-due-total", money(totals.plannedPaymentCents));
    setText("balance-total", money(totals.balanceCents));
    setText("paid-total", money(totals.paidCents));
    setText("account-count", String(data.accounts.length));
    renderPaycheckSchedule(data);
    renderCashRunway(data);
    renderCheckingLedger(data);
    renderAccounts(data);
    renderTransactions(data);
    renderJournal(data);
    renderLedger(data);
    renderTrialBalance(data);
    setupSorting(data);
  }

  function readToken() {
    try {
      return localStorage.getItem(tokenKey) || "";
    } catch (error) {
      return "";
    }
  }

  function writeToken(value) {
    try {
      if (value) {
        localStorage.setItem(tokenKey, value);
      } else {
        localStorage.removeItem(tokenKey);
      }
    } catch (error) {
      // Storage blocked: the token lasts until the page is closed.
    }
  }

  function setSaveStatus(text) {
    setText("journal-save-status", text);
  }

  function updateSaveControls() {
    var saveButton = document.getElementById("journal-save");
    var tokenButton = document.getElementById("journal-token");
    var pendingCount = Object.keys(pendingPosted).length;
    if (!saveButton || !tokenButton) {
      return;
    }
    saveButton.disabled = !github || !token || pendingCount === 0;
    saveButton.textContent = pendingCount ? "Save to GitHub (" + pendingCount + ")" : "Save to GitHub";
    tokenButton.textContent = token ? "Disconnect GitHub" : "Connect GitHub";
  }

  function githubRequest(method, body) {
    var url = "https://api.github.com/repos/" + github.owner + "/" + github.repo + "/contents/" + github.path;
    if (method === "GET") {
      url += "?ref=" + encodeURIComponent(github.branch);
    }
    return fetch(url, {
      method: method,
      cache: "no-store",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28"
      },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (response) {
      if (response.ok) {
        return response.json();
      }
      var error = new Error("GitHub returned " + response.status + ".");
      error.status = response.status;
      throw error;
    });
  }

  function githubErrorMessage(error) {
    if (error.status === 401) {
      return "GitHub rejected the token. It may have expired; disconnect and connect again with a new one.";
    }
    if (error.status === 403 || error.status === 404) {
      return "The token cannot write to " + github.owner + "/" + github.repo + ". Check it has Contents: Read and write on this repository.";
    }
    if (error.status === 409) {
      return "The file changed on GitHub while saving. Click Save again.";
    }
    return "Could not reach GitHub: " + error.message;
  }

  function decodeBase64(value) {
    var binary = atob(value.replace(/\n/g, ""));
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i += 1) {
      bytes[i] = binary.charCodeAt(i);
    }
    return new TextDecoder().decode(bytes);
  }

  function encodeBase64(value) {
    var bytes = new TextEncoder().encode(value);
    var binary = "";
    for (var i = 0; i < bytes.length; i += 1) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  function loadFromGitHub() {
    return githubRequest("GET").then(function (file) {
      return JSON.parse(decodeBase64(file.content));
    });
  }

  function saveToGitHub() {
    var changes = pendingPosted;
    setSaveStatus("Saving...");
    document.getElementById("journal-save").disabled = true;

    // Apply only the posted changes onto the latest file, so edits made on another computer are kept.
    githubRequest("GET").then(function (file) {
      var latest = JSON.parse(decodeBase64(file.content));
      latest.journalEntries.forEach(function (entry) {
        if (Object.prototype.hasOwnProperty.call(changes, entry.id)) {
          entry.posted = changes[entry.id];
        }
      });
      return githubRequest("PUT", {
        message: "Update posted status in general journal",
        content: encodeBase64(JSON.stringify(latest, null, 2) + "\n"),
        sha: file.sha,
        branch: github.branch
      });
    }).then(function () {
      Object.keys(changes).forEach(function (id) {
        savedPosted[id] = changes[id];
      });
      pendingPosted = {};
      setSaveStatus("Saved to GitHub at " + new Date().toLocaleTimeString() + ".");
      updateSaveControls();
    }).catch(function (error) {
      setSaveStatus(githubErrorMessage(error));
      updateSaveControls();
    });
  }

  function toggleConnection() {
    if (token) {
      if (!window.confirm("Remove the GitHub token from this browser?")) {
        return;
      }
      token = "";
      writeToken("");
      setSaveStatus("Disconnected. Changes can no longer be saved from this browser.");
      updateSaveControls();
      return;
    }

    var entered = window.prompt("Paste a GitHub fine-grained token with Contents: Read and write on " + github.owner + "/" + github.repo + ". It is stored only in this browser.");
    if (!entered || !entered.trim()) {
      return;
    }
    token = entered.trim();
    setSaveStatus("Checking token...");
    githubRequest("GET").then(function () {
      writeToken(token);
      setSaveStatus("Connected to GitHub.");
      updateSaveControls();
    }).catch(function (error) {
      token = "";
      setSaveStatus(githubErrorMessage(error));
      updateSaveControls();
    });
  }

  function setupSaving() {
    var saveButton = document.getElementById("journal-save");
    var tokenButton = document.getElementById("journal-token");
    if (!saveButton || !tokenButton) {
      return;
    }
    if (!github) {
      tokenButton.hidden = true;
      saveButton.hidden = true;
      return;
    }
    saveButton.addEventListener("click", saveToGitHub);
    tokenButton.addEventListener("click", toggleConnection);
    window.addEventListener("beforeunload", function (event) {
      if (Object.keys(pendingPosted).length) {
        event.preventDefault();
        event.returnValue = "";
      }
    });
    updateSaveControls();
  }

  function loadFromSite() {
    return fetch(dataUrl).then(function (response) {
      if (!response.ok) {
        throw new Error("Could not load accounting data.");
      }
      return response.json();
    });
  }

  function loadData() {
    if (!github || !token) {
      return loadFromSite();
    }
    // The published site can lag a minute behind GitHub, so read the repository directly when connected.
    return loadFromGitHub().then(function (data) {
      setSaveStatus("Connected. Showing the latest data from GitHub.");
      return data;
    }).catch(function (error) {
      setSaveStatus(githubErrorMessage(error));
      return loadFromSite();
    });
  }

  setupSaving();
  loadData()
    .then(function (data) {
      data.journalEntries.forEach(function (entry) {
        savedPosted[entry.id] = Boolean(entry.posted);
      });
      render(data);
    })
    .catch(function (error) {
      var message = document.getElementById("accounting-error");
      message.hidden = false;
      message.textContent = error.message;
    });
}());
