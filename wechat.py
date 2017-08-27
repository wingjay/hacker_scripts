# python3 virtual-environment
# sdk: https://github.com/justdoit0823/pywxclient
import sys

from pywxclient.core import Session, SyncClient, TextMessage
from pywxclient.core.exception import (
    WaitScanQRCode, RequestError, APIResponseError, SessionExpiredError,
    AuthorizeTimeout, UnsupportedMessage)


def sendTextTo(client, remarkName, textContext):
	me=client.user['UserName']
	contacts=client.get_contact(); 
	
	to_user=''
	for c in contacts:
		if(c['RemarkName']==remarkName):
			to_user=c['UserName']
			break
	if not to_user:
		print('cannot find user for ', remarkName)
		return

	print('ready to send message to ', remarkName)
	textMsg=TextMessage(me, to_user, textContext)
	client.send_message(textMsg)
	print('finish send text message')


def login():
	session = Session();
	client = SyncClient(session);
	authorize_url = client.get_authorize_url()
	print('Go to authorize: ', authorize_url)
	while True:
		try:
			authorize_result = client.authorize()
		except WaitScanQRCode:
			continue
		except AuthorizeTimeout:
			print('Authorize timeout')
			sys.exit(0)

		if authorize_result:
				break	

	print('start login')			
	client.login()
	print('login success')	
	return client


def main():
	client = login()
	sendTextTo(client, 'xx', '测试文本')


if __name__ == '__main__':
	main()
