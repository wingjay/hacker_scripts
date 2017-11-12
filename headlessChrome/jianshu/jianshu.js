// node jianshu.js ## ##
// puppeteer version:0.10.1

const puppeteer = require('puppeteer');

const message = '读者好，我是wingjay，Android工程师，目前就职阿里巴巴。 为了能更好与简书读者交流技术成长和职业发展，我决定尝试创建自己的《阿里求职付费微信群》：iam_wingjay。 群内提供以下服务： 1. 和大家分享在阿里的经验积累和前沿技术； 2. 分享专门针对阿里巴巴Android岗位的面试经验； 3. 定时推送大厂内部最新的内推信息。 《关于阿里求职付费群》详情见：http://www.jianshu.com/p/655af849aaf6 打扰。 关于作者： Android工程师，就职阿里巴巴，之前在原Google创业团队工作，所开发的 Android App 曾获得过全美 Play Store Best of 2016 奖项。';

(async() => {
	fs = require('fs')
	follower_list = fs.readFileSync('followers.txt', 'utf-8').split(/[\n\r]/);

	weibo_account = process.argv[2]
	weibo_pwd = process.argv[3]
	console.log(weibo_account, '\n', weibo_pwd)
	const google = 'https://google.com'
	// const url = 'http://www.jianshu.com/notifications#/chats/new?mail_to=4840388'
	const login_url = 'https://www.jianshu.com/users/auth/weibo'

	// 启动浏览器
	const browser = await puppeteer.launch({
	        // 关闭无头模式，方便我们看到这个无头浏览器执行的过程
	        headless: false,
	        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
	    });

	// 打开页面
	const page = await browser.newPage();
	// 设置浏览器视窗
	page.setViewport({
	    width: 1376,
	    height: 768,
	});
	// 地址栏输入网页地址
	await page.goto(login_url, {
	    waitUntil: 'networkidle', // 等待网络状态为空闲的时候才继续执行
	});
	// await page.click('.weibo');
	await page.click('#userId');
	await page.focus('#userId');
	await page.type(weibo_account);
	await page.click('#passwd');
	await page.focus('#passwd');
	await page.type(weibo_pwd, {
		delay: 100
	});
	await page.click('.WB_btn_login', {
		button: 'right',
	});
	await page.press('Enter');
	// 登陆成功
	await page.waitForSelector('.logo');

	// 打开消息页面
	for(var i=0; i<follower_list.length; i++) {
		var url = follower_list[i];
		console.log(url)
		await page.goto(url, {
		    waitUntil: 'networkidle', // 等待网络状态为空闲的时候才继续执行
		});
		await page.focus('.form-control');
		await page.type(message);
		await page.click('.btn-send');
	}

	// 不关闭浏览器，看看效果
	// await browser.close();

})();