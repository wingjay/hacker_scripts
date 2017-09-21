# coding=utf-8
# python yunque.py username password
import sys
import requests

url = 'https://lark.alipay.com/api/v2'
headers = {"Content-Type": "application/x-www-form-urlencoded"}

xiamiRepoId = '35201'
xiamiMobileGroupId = '24208'

androidTitleFilter = ('android', u'安卓')
iosTitleFilter = ('ios')

def main(userName, password):
	token = ''
	print('go to login')
	token = login(userName, password)

	if not token:
		print('token empty, login fail')
		exit()

	headers.update({'X-Auth-Token': token})
	rawRepos = requests.get(url + '/groups/' + xiamiMobileGroupId + '/repos')
	repos = rawRepos.json()['data'] # repos of XiamiMobile group

	androidRepos = []
	iosRepos = []
	bothRepos = []
	for repo in repos:
		repoName = repo['name'].lower()
		if any(filter in repoName for filter in androidTitleFilter):
			androidRepos.append(repo)
		elif any(filter in repoName for filter in iosTitleFilter):
			iosRepos.append(repo)
		else:
			bothRepos.append(repo)
	print('- [Android]()')
	printRepoDocs(androidRepos)
	print('- [iOS]()')
	printRepoDocs(iosRepos)
	print('- [其他]()')
	printRepoDocs(bothRepos)


def printRepoDocs(repos):
	for repo in repos:
		docs = requests.get(url + '/repos/' + str(repo['id']) + '/docs', headers=headers)
		docs = docs.json()['data']
		if len(docs) <= 0:
			continue
		print('	- [' + repo['name'] + ']()')
		for doc in docs:
			print('		- [' + doc['title'] + '](' + repo['slug'] + '/' + doc['slug'] + ')')



def login(userName, password):
	print('username: ' + userName + ", password: " + password)
	payload = {'username': userName, 'password': password}
	response = requests.post(url+'/authorize', data=payload, headers=headers)
	jsonData = response.json()
	return jsonData['data']['private_token']


if __name__ == '__main__':
	main(str(sys.argv[1]), str(sys.argv[2]))