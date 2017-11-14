// puppeteer v0.13.0

const puppeteer = require('puppeteer');

(async() => {
	const url = 'https://job.alibaba.com/zhaopin/positionList.htm'
	// 启动浏览器
	const browser = await puppeteer.launch({
	        // 关闭无头模式，方便我们看到这个无头浏览器执行的过程
	        headless: true,
	    });
	// 打开页面
	const page = await browser.newPage();
	// 地址栏输入网页地址
	await page.goto(url, {
	    waitUntil: 'networkidle2', // 等待网络状态为空闲的时候才继续执行
	});

	await page.click('[rel^="技术类"]')
	await page.click('[rel^="杭州"]')
	await page.click('[rel^="上海"]')
	await page.click('[rel^="北京"]')
	await page.click('[rel^="深圳"]')
	await page.type('#keyword', 'android', {
		delay: 100
	});
	await page.click('.search-btn');

	for (var i = 0; i <= 2; i++) {
		await page.waitForSelector('.table-list tr td');

		const moreIconList = await page.$$('.more-icon');
		await Promise.all(moreIconList.map(icon => {
			page.evaluate(i => i.click(), icon)
		}));

		const elementHandle = await page.$('.table-list');
      	const box = await elementHandle.boundingBox();
      	console.log("print page: " + i + ". height: " + box.height)
		await page.screenshot({
			path: 'screenshots/sc_' + i + '.jpeg',
			quality: 100,
			type: "jpeg",
			clip: {
				x: 0,
				y: 450,
				width: box.width,
				height: box.height
			}
		});
		await page.click('li[data-index="next"] a')
	}

	browser.close()
})();
