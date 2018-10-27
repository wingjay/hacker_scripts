// puppeteer v0.13.0
// 收集企业方userId

// 1. 填写用户名密码
var userName = '';
var password = '';


const puppeteer = require('puppeteer');
const fs = require('fs');

const frameUrlDemo = 'https://bbs.sjtu.edu.cn/bbsdoc,board,CS.html'

const loginUrl = 'https://bbs.sjtu.edu.cn';
const boardsUrl = new Map([
	['勤工助学', 'https://bbs.sjtu.edu.cn/bbstdoc,board,PartTime.html'],
	['求职交流', 'https://bbs.sjtu.edu.cn/bbstdoc,board,JobForum.html'],
	['就业信息', 'https://bbs.sjtu.edu.cn/bbstdoc,board,JobInfo.html']
]);

const numberFilter = new Set(["[板规]", "[置底]", "序号"])
const lastPageText = "上一页"

const resultUserIds = new Set();

const title = '【上交校友兼职求职群】欢迎企业入群';
const content = '你好，如果需要发布招聘、项目合作等信息的朋友可加入 上交兼职求职微信群，我们会第一时间转发到上交校友群，未来还会有上海各大高校校友群，以帮助快速对接。\n可加微信 iam_wingjay 入群，须备注 “饮水思源+企业”，谢谢，打扰。'

var browser;
// 打开页面
var page;

(async() => {
	browser = await puppeteer.launch({
        // 关闭无头模式，方便我们看到这个无头浏览器执行的过程
        headless: false,
    });
    page = await browser.newPage();	
	// login
	for(var item of boardsUrl.entries()) {
		console.log('open: ', item[0])
		await page.goto(item[1], {
		    waitUntil: 'networkidle2', // 等待网络状态为空闲的时候才继续执行
		});
		var totalPages = 20;
		if (item[0] == '求职交流') {
			totalPages = 20;
		} else if (item[0] == '勤工助学') {
			totalPages = 70;
		} else if (item[0] == '就业信息') {
			totalPages = 250;
		}
		for(var pages = totalPages; pages >0; pages--) {
			await collectUserIds();
			// 点击上一页
			const links = await page.$$('center a');
			for(var item of links) {
				var value = await page.evaluate(el => el.textContent, item)
				if (lastPageText === value) {
					var lastPage = await page.evaluate(el => el.href, item)
					console.log('goto lastPage:', lastPage)
					await page.goto(lastPage, {
						waitUntil: 'networkidle2', // 等待网络状态为空闲的时候才继续执行
					})
					break;
				}
			}
			sleep(100);
		}
	}
	console.log('result: ', resultUserIds)
	saveToFile()
	browser.close()
})();

async function saveToFile() {
	var resultContent = "";
	resultUserIds.forEach(function(value, key) {
		resultContent += value + "\n";
	})
	fs.writeFile('target_list.txt', resultContent, function(err) {
		if (err) {
			return console.log(err);
		}
		console.log('saved!');
	})
}

async function collectUserIds(name, url) {
	const results = await page.$$('table tbody tr')
	for(var item of results) {
		const tds = await item.$$('td')
		const number = await page.evaluate(el => el.textContent, tds[0])
		if (numberFilter.has(number)) {
			// console.log(number, ' was filtered')
			continue;
		}
		const userId = await page.evaluate(el => el.textContent, tds[2])
		console.log(number, ':', userId);
		resultUserIds.add(userId)
	}
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}
