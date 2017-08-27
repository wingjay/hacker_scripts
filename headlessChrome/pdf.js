const puppeteer = require('puppeteer');

(async() => {

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://news.ycombinator.com', {waitUntil: 'networkidle'});
// page.pdf() is currently supported only in headless mode.
// @see https://bugs.chromium.org/p/chromium/issues/detail?id=753118
await page.pdf({
  path: 'hn.pdf',
  format: 'letter'
});

browser.close();

})();