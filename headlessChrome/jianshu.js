// node jianshu.js ## ##

const puppeteer = require('puppeteer');

var lineReader = require('readline').createInterface({
  input: require('fs').createReadStream('jianshu.js')
});

lineReader.on('line', function (line) {
  console.log('Line from file:', line);
});

// (async() => {
// 	weibo_account = process.argv[2]
// 	weibo_pwd = process.argv[3]
// 	console.log(weibo_account, '\n', weibo_pwd)
// 	const google = 'https://google.com'
// 	const url = 'http://www.jianshu.com/notifications#/chats/new?mail_to=4840388'
// 	const login_url = 'https://www.jianshu.com/users/auth/weibo'

// 	// 启动浏览器
// 	const browser = await puppeteer.launch({
// 	        // 关闭无头模式，方便我们看到这个无头浏览器执行的过程
// 	        headless: false,
// 	        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
// 	    });

// 	// 打开页面
// 	const page = await browser.newPage();
// 	// 设置浏览器视窗
// 	page.setViewport({
// 	    width: 1376,
// 	    height: 768,
// 	});
// 	// 地址栏输入网页地址
// 	await page.goto(login_url, {
// 	    waitUntil: 'networkidle', // 等待网络状态为空闲的时候才继续执行
// 	});
// 	// await page.click('.weibo');
// 	await page.click('#userId');
// 	await page.focus('#userId');
// 	await page.type(weibo_account);
// 	await page.click('#passwd');
// 	await page.focus('#passwd');
// 	await page.type(weibo_pwd, {
// 		delay: 100
// 	});
// 	await page.click('.WB_btn_login', {
// 		button: 'right',
// 	});
// 	await page.press('Enter');
// 	// 登陆成功
// 	await page.waitForSelector('.logo');

// 	// 打开消息页面
// 	await page.goto(url, {
// 	    waitUntil: 'networkidle', // 等待网络状态为空闲的时候才继续执行
// 	});
// 	await page.focus('.form-control');
// 	await page.type('test script');
// 	await page.click('.btn-send');

// 	// 不关闭浏览器，看看效果
// 	// await browser.close();

// })();