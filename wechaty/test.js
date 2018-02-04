// const QrcodeTerminal  = require('qrcode-terminal')

const { config, Wechaty }  = require('Wechaty')//import { config, Wechaty } from 'wechaty'

const bot = Wechaty.instance({ profile: config.default.DEFAULT_PROFILE })

bot
.on('scan', (url, code) => {
	// if (!/201|200/.test(String(code))) {
	// 	const loginUrl = url.replace(/\/qrcode\//, '/l/')
	// 	QrcodeTerminal.generate(loginUrl)
	// }
	console.log(`Scan QR Code to login: ${code}\n${url}`)
})
.on('login',       user => {
	console.log(`User ${user} logined`)
	bot.say('Wechaty login').catch(console.error)
})
.on('message',  async message => {
	try {
	    const room = m.room()
	    console.log(
	      (room ? `${room}` : '')
	      + `${m.from()}:${m}`,
	    )

	    if (/^(ding|ping|bing|code)$/i.test(m.content()) && !m.self()) {
	      m.say('dong')
	      log.info('Bot', 'REPLY: dong')

	      const joinWechaty =  `Join Wechaty Developers' Community\n\n` +
	                            `Wechaty is used in many ChatBot projects by hundreds of developers.\n\n` +
	                            `If you want to talk with other developers, just scan the following QR Code in WeChat with secret code: wechaty,\n\n` +
	                            `you can join our Wechaty Developers' Home at once`
	      await m.say(joinWechaty)
	      await m.say(new MediaMessage(BOT_QR_CODE_IMAGE_FILE))
	      await m.say('Scan now, because other Wechaty developers want to talk with you too!\n\n(secret code: wechaty)')
	      log.info('Bot', 'REPLY: Image')
	    }
	  } catch (e) {
	    log.error('Bot', 'on(message) exception: %s' , e)
	  }
})
.start()
