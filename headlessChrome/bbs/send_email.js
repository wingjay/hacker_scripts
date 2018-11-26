
const nodemailer = require('nodemailer');
const fs = require('fs');
const lineByLine = require('./utils/readlines.js');

const emailFilter = new Set();
const targetEmail = new Set();

var user = 'sh_xianshi_a@126.com';
var password = '6896226yjlrn';

var email_html = "";

(async() => {
	if (user == '' || password == '') {
		console.log('Enter user & password')
		return;
	}

	await prepare();

	const liner = new lineByLine('email.html');
	let line;
	while (line = liner.next()) {
	    email_html += line.toString('utf-8');
	}

	var count = 10;
	for(var item of targetEmail) {
		if (count < 0) {
			break;
		}
		count--;
		if (item == '') {
			continue;
		}
		await send(item);
	}
})();

async function send(mail) {
	const transporter = nodemailer.createTransport({
	    host: 'smtp.126.com',
	    port: 465, // SMTP 端口
	    auth: {
	        user: user,//发送者邮箱
	        pass: password //授权码,在准备工作中开启服务时候的授权码
	    }
	});
	const mailOptions = {
	    from: user, // 发送者
	    to: mail, // 接受者,可以同时发送多个,以逗号隔开
	    subject: 'BAT招聘认证群邀请', // 标题
	    html: email_html
	};
	await transporter.sendMail(mailOptions, function (err, info) {
	   if (err) {
	       console.log(err, "mail: " + mail);
	       return;
	   }
	   console.log(`发送成功：${info.accepted}`);
	   fs.appendFileSync('used_email.txt', mail + '\n');
	});
}

async function prepare() {
	// read data
	const liner = new lineByLine('used_email.txt');
	let line;
	while (line = liner.next()) {
	    emailFilter.add(line.toString('utf-8'));
	}
	console.log('emailFilter: ', emailFilter.size)

	const liner2 = new lineByLine('email_list.txt')
	let line2;
	while (line2 = liner2.next()) {
	    targetEmail.add(line2.toString('utf-8'));
	}
	console.log('targetEmail', targetEmail.size)

	for (var item of targetEmail) {
		if (emailFilter.has(item)) {
			console.log('delete ', item);
			targetEmail.delete(item);
		}
	}
	console.log(targetEmail.size)
}
