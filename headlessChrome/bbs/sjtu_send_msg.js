// puppeteer v0.13.0
// 发信息

// 1. 填写用户名密码
var userName = 'wingjay';
var password = 'yinjie123123';

const lineByLine = require('./utils/readlines.js');

const puppeteer = require('puppeteer');
const fs = require('fs');

const userIdFilter = new Set();
const targetUserId = new Set();

const loginUrl = 'https://bbs.sjtu.edu.cn';
const sendMsgUrl = 'https://bbs.sjtu.edu.cn/bbspstmail?userid='

const title = '【上交校友兼职求职群】欢迎企业入群';
const content = '，你好。\n\n我们是“上交校友兼职求职微信群”的管理者，主要以微信群的方式，向交大的校友及同学们发布招聘、兼职、项目合作等信息，未来还会有上海各大高校校友群。\n\n如有需要的话可加微信 iam_wingjay 入群，须备注 “饮水思源+企业名”。\n\n谢谢，打扰。'

var browser;
// 打开页面
var page;

(async() => {
	if (userName == '' || password == '') {
		console.log('Error:请填写用户名密码')
		return
	}

	await prepare();
	browser = await puppeteer.launch({
        // 关闭无头模式，方便我们看到这个无头浏览器执行的过程
        headless: false,
    });
    page = await browser.newPage();	
	// login
	await login(loginUrl)

	var count = 20;
	for(var item of targetUserId) {
		if (count <= 0) {
			break;
		}
		count--;
		await send(item);
	}

	browser.close()
})();

async function prepare() {
	// read data
	const liner = new lineByLine('used_list.txt');
	let line;
	while (line = liner.next()) {
	    userIdFilter.add(line.toString('utf-8'));
	}
	console.log('userIdFilter', userIdFilter.size)

	const liner2 = new lineByLine('target_list.txt')
	let line2;
	while (line2 = liner2.next()) {
	    targetUserId.add(line2.toString('utf-8'));
	}
	console.log('targetUserId', targetUserId.size)

	for (var item of targetUserId) {
		if (userIdFilter.has(item)) {
			console.log('delete ', item);
			targetUserId.delete(item);
		}
	}
	console.log(targetUserId.size)
}

async function send(userId) {
	console.log('Send to ', userId)
	var url = sendMsgUrl + userId
	await page.goto(url, {
	    waitUntil: 'networkidle2', // 等待网络状态为空闲的时候才继续执行
	});
	await page.type('input[name=title]', title, {delay: 10});
	await page.type('textarea[name=text]', userId + content, {delay: 10});

	fs.appendFileSync('used_list.txt', userId + '\n');
	await page.click('input[type=submit]')
	await sleep(800)
}

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

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}
