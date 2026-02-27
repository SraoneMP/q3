const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const urls = [
    'https://sanand0.github.io/tdsdata/js_table/?seed=63',
    'https://sanand0.github.io/tdsdata/js_table/?seed=64',
    'https://sanand0.github.io/tdsdata/js_table/?seed=65',
    'https://sanand0.github.io/tdsdata/js_table/?seed=66',
    'https://sanand0.github.io/tdsdata/js_table/?seed=67',
    'https://sanand0.github.io/tdsdata/js_table/?seed=68',
    'https://sanand0.github.io/tdsdata/js_table/?seed=69',
    'https://sanand0.github.io/tdsdata/js_table/?seed=70',
    'https://sanand0.github.io/tdsdata/js_table/?seed=71',
    'https://sanand0.github.io/tdsdata/js_table/?seed=72'
  ];

  let grandTotal = 0;

  for (const url of urls) {
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForSelector('table', { timeout: 5000 });

    const cells = await page.locator('table td').allTextContents();
    
    let pageTotal = 0;
    for (const rawText of cells) {
      const text = rawText.trim();
      if (!text) continue;
      const cleaned = text.replace(/[,₹$€£%]/g, '');
      const num = Number(cleaned);
      if (!isNaN(num)) {
        pageTotal += num;
      }
    }
    console.log(`${url} -> ${pageTotal}`);
    grandTotal += pageTotal;
  }

  await browser.close();
  console.log(`GRAND_TOTAL_RAW=${grandTotal}`);
})();
