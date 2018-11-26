// puppeteer v0.13.0
// 发帖

// 1. 填写用户名密码
var userName = '';
var password = '';


const puppeteer = require('puppeteer');

const frameUrlDemo = 'https://bbs.sjtu.edu.cn/bbsdoc,board,CS.html'

const loginUrl = 'https://bbs.sjtu.edu.cn';
const boardsUrl = new Map([
	['求职交流', 'https://bbs.sjtu.edu.cn/bbspst?board=JobForum'],
	['就业信息', 'https://bbs.sjtu.edu.cn/bbspst?board=JobInfo'],
	// ['IT职场', 'https://bbs.sjtu.edu.cn/bbspst?board=ITCareer'],
	['交大快讯', 'https://bbs.sjtu.edu.cn/bbspst?board=SJTUNews'],
	['勤工助学', 'https://bbs.sjtu.edu.cn/bbspst?board=PartTime'],
	// ['移动开发者', 'https://bbs.sjtu.edu.cn/bbspst?board=MobileDev'],
	// ['人工智能', 'https://bbs.sjtu.edu.cn/bbspst?board=AI'],
	// ['研究之家', 'https://bbs.sjtu.edu.cn/bbspst?board=Graduate'],
	// ['计算机系', 'https://bbs.sjtu.edu.cn/bbspst?board=CS']
]);

const title = '【上交校友兼职求职群】欢迎校友及企业入群';
const content = '各位同学及校友好，如想关注兼职、求职信息的校友可加入 上交校友群，目前已经不少同学加了，需提供班号认证哦；\n\n想发布招聘、项目合作等信息的朋友可加入 上交企业方微信群，需提供企业名。\n\n我们会对求职、兼职群内的信息进行过滤并第一时间转发到校友群，以保证高效率对接。\n\n有相关需求的校友或企业朋友可加微信 iam_wingjay 入群，须备注 “饮水思源+上述认证信息”，否则不加，非诚勿扰，谢谢。'

var browser;
// 打开页面
var page;

(async() => {
	if (userName == '' || password == '') {
		console.log('Error:请填写用户名密码')
		return
	}
	browser = await puppeteer.launch({
        // 关闭无头模式，方便我们看到这个无头浏览器执行的过程
        headless: false,
    });
    page = await browser.newPage();	
	// login
	await login(loginUrl)

	for(var item of boardsUrl.entries()) {
		await publish(item[0], item[1]);
	}

	browser.close()
})();

async function login(url) {
	// 设置浏览器视窗
	page.setViewport({
	    width: 1376,
	    height: 768,
	});
	// 地址栏输入网页地址
	await page.goto(url, {
	    waitUntil: 'networkidle2', // 等待网络状态为空闲的时候才继续执行
	});
	await page.type('#Text1', userName, {
		delay: 10
	});
	await page.type('#Password1', password, {
		delay: 10
	});	
	await page.click('#button_style li a');
	await page.mainFrame().waitForSelector('#rframe');
}

async function publish(name, url) {
	console.log('name: ' + name)
	await page.goto(url, {
	    waitUntil: 'networkidle2', // 等待网络状态为空闲的时候才继续执行
	});
	await page.type('#inputCH', title, {delay: 10});
	await page.type('#text', content, {delay: 20});
	const submit = await page.$('input[type=submit]');
	await submit.click()
	await page.mainFrame().waitForSelector('.title');
	await sleep(2000)
	console.log('finish')
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}
