const { chromium } = require('playwright');

const urls = [
    'https://tds-playwright-scrapers.netlify.app/57',
    'https://tds-playwright-scrapers.netlify.app/58',
    'https://tds-playwright-scrapers.netlify.app/59',
    'https://tds-playwright-scrapers.netlify.app/60',
    'https://tds-playwright-scrapers.netlify.app/61',
    'https://tds-playwright-scrapers.netlify.app/62',
    'https://tds-playwright-scrapers.netlify.app/63',
    'https://tds-playwright-scrapers.netlify.app/64',
    'https://tds-playwright-scrapers.netlify.app/65',
    'https://tds-playwright-scrapers.netlify.app/66'
];

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    let grandTotal = 0;
    
    for (const url of urls) {
        console.log(`\nScraping: ${url}`);
        await page.goto(url, { waitUntil: 'networkidle' });
        
        const numbers = await page.$$eval('table td, table th', cells => {
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
