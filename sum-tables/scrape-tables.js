const { chromium } = require('playwright');

const urls = [
    'https://sanand0.github.io/tdsdata/js_table/?seed=57',
    'https://sanand0.github.io/tdsdata/js_table/?seed=58',
    'https://sanand0.github.io/tdsdata/js_table/?seed=59',
    'https://sanand0.github.io/tdsdata/js_table/?seed=60',
    'https://sanand0.github.io/tdsdata/js_table/?seed=61',
    'https://sanand0.github.io/tdsdata/js_table/?seed=62',
    'https://sanand0.github.io/tdsdata/js_table/?seed=63',
    'https://sanand0.github.io/tdsdata/js_table/?seed=64',
    'https://sanand0.github.io/tdsdata/js_table/?seed=65',
    'https://sanand0.github.io/tdsdata/js_table/?seed=66'
];

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    let grandTotal = 0;
    
    for (const url of urls) {
        console.log(`\nScraping: ${url}`);
        await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
        
        // Wait for table to appear
        await page.waitForSelector('table', { timeout: 10000 });
        
        const numbers = await page.evaluate(() => {
            const cells = Array.from(document.querySelectorAll('table td, table th'));
            return cells.map(cell => {
                const text = cell.textContent.trim();
                const num = parseFloat(text);
                return isNaN(num) ? 0 : num;
            }).filter(n => n !== 0);
        });
        
        const pageSum = numbers.reduce((a, b) => a + b, 0);
        console.log(`  Found ${numbers.length} numbers, sum: ${pageSum}`);
        grandTotal += pageSum;
    }
    
    await browser.close();
    
    console.log('\n' + '='.repeat(60));
    console.log(`TOTAL SUM FROM ALL PAGES: ${grandTotal}`);
    console.log('='.repeat(60));
    console.log(`\nFinal Answer: ${grandTotal}`);
})();
