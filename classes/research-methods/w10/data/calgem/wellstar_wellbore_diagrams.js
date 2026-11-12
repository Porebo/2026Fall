// Find and download wellbore diagrams from the WellSTAR public portal.
//
// This is the browser code used on November 10, 2026 (PROVENANCE.md, section 7),
// combined into one file. It was run through the Playwright MCP server from Claude Code
// ("browser_run_code"), which calls the exported function with a Playwright `page`.
// It can also be run with plain Playwright (see the bottom of this file).
//
// Before running: open https://wellstar-public.conservation.ca.gov/ in the same browser
// and accept the data disclosure by hand. The code does not accept it for you.
//
// Steps per well, the same as the manual steps in PROVENANCE.md, section 7.4:
//   1. Search the 10-digit API in the global search box.
//   2. Open the Well Detail page, switch the view from "Summary" to "Documents".
//   3. Collect rows whose Type is "Wellbore Diagram" (Document ID in column 7).
//   4. For each Document ID, search Explore Data > Documents and click the file link.
//      (The Well Detail grid has no working public download link.)

const SITE = 'https://wellstar-public.conservation.ca.gov';

// List the wellbore diagram documents for one well (10-digit API).
async function listWellboreDiagrams(page, api) {
  await page.goto(SITE + '/Well/Well/Index');
  const box = page.getByRole('textbox', { name: 'Global Search value to be sought' });
  await box.fill(api);
  await box.press('Enter');
  const link = page.getByRole('link', { name: api, exact: true }).first();
  await link.waitFor({ timeout: 30000 });
  const detail = await link.getAttribute('href');
  await page.goto(SITE + detail);
  await page.getByRole('button', { name: 'Summary' }).click();
  await page.getByRole('link', { name: 'Documents', exact: true }).first().click();
  await page.waitForTimeout(4000);
  const rows = await page.$$eval('[role=row], tr', rs =>
    rs.map(r => Array.from(r.querySelectorAll('[role=gridcell], td')).map(c => c.innerText.trim()))
      .filter(c => c.length >= 7));
  // Columns: Upload Date, Relevant Date, Category, Type, Description, Filename, Document ID, ...
  const docs = rows.filter(r => r[3] === 'Wellbore Diagram').map(r => ({
    uploadDate: r[0], relevantDate: r[1], description: r[4], filename: r[5], documentId: r[6],
  }));
  return { api, detail, docs };
}

// Download one document by its WellSTAR Document ID. Returns the suggested file name.
// The browser saves the file to its download folder (for the Playwright MCP server:
// the .playwright-mcp folder of the workspace).
async function downloadDocument(page, documentId, saveDir) {
  await page.goto(SITE + '/General/DocumentSearch/Index');
  await page.getByRole('textbox', { name: 'Document ID' }).fill(documentId);
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  const row = page.locator('[role=row]')
    .filter({ has: page.getByRole('gridcell', { name: documentId, exact: true }) }).first();
  await row.waitFor({ timeout: 30000 });
  const a = row.locator('a[href*="DownloadDocument"]').first();
  const href = await a.getAttribute('href');
  // Some files open in a new tab instead of downloading when clicked; forcing a
  // download attribute on a fresh link avoids that (needed for Doc ID 243866).
  const [download] = await Promise.all([
    page.waitForEvent('download', { timeout: 60000 }),
    page.evaluate(h => {
      const x = document.createElement('a');
      x.href = h; x.download = '';
      document.body.appendChild(x); x.click();
    }, href),
  ]);
  if (saveDir) {
    await download.saveAs(require('path').join(saveDir, download.suggestedFilename()));
  } else {
    await download.path();
  }
  return { documentId, href, file: download.suggestedFilename() };
}

// The run of November 10, 2026: the 10 wells of the final sample (PROVENANCE.md, 7.2).
const FINAL_APIS = [
  '0411105027', '0411121560', '0411105257', '0411122017', '0411104888',
  '0411103998', '0411104441', '0411121506', '0411104246', '0411104595',
];

async function run(page, apis = FINAL_APIS, saveDir) {
  const log = [];
  for (const api of apis) {
    const found = await listWellboreDiagrams(page, api);
    for (const d of found.docs) {
      log.push({ api, ...d, ...(await downloadDocument(page, d.documentId, saveDir)) });
    }
    if (!found.docs.length) log.push({ api, note: 'no wellbore diagram' });
  }
  return log;
}

module.exports = { listWellboreDiagrams, downloadDocument, run, FINAL_APIS };

// Plain Playwright (npm install playwright): node wellstar_wellbore_diagrams.js
// Files are saved to a "downloads" folder next to this script, under WellSTAR's names.
if (require.main === module) {
  (async () => {
    const saveDir = require('path').join(__dirname, 'downloads');
    require('fs').mkdirSync(saveDir, { recursive: true });
    const { chromium } = require('playwright');
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    await page.goto(SITE);
    console.log('Accept the data disclosure in the browser window, then press Enter here.');
    await new Promise(r => process.stdin.once('data', r));
    console.log(JSON.stringify(await run(page, FINAL_APIS, saveDir), null, 1));
    await browser.close();
  })();
}
