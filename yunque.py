# coding=utf-8
# python yunque.py username password
import sys
import requests

url = 'https://lark.alipay.com/api/v2'
headers = {"Content-Type": "application/x-www-form-urlencoded"}

xiamiMobileGroupId = 'xiami-mobile'
xiamiIndexRepo = xiamiMobileGroupId + '/index'

androidTitleFilter = ('android', u'安卓')
iosTitleFilter = ('ios')

f = open('index.md', 'w')

def main(userName, password):
	print('go to login')
	login(userName, password)
	repos = getReposFromGroup(xiamiMobileGroupId)

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
	f.write('- [Android]()\n')
	printRepoDocs(androidRepos)
	f.write('- [iOS]()\n')
	printRepoDocs(iosRepos)
	f.write('- [其他]()\n')
	printRepoDocs(bothRepos)
	f.close()
	print('generated index in index.md')
	file = open('index.md', 'r')
	updateRepoIndex(file.read())


def printRepoDocs(repos):
	for repo in repos:
		docs = requests.get(url + '/repos/' + str(repo['id']) + '/docs', headers=headers)
		docs = docs.json()['data']
		if len(docs) <= 0:
			continue
		str1 = '	- [' + repo['name'] + ']()\n'
		f.write(str1.encode("UTF-8"))
		for doc in docs:
			str2 = '		- [' + doc['title'] + '](' + repo['slug'] + '/' + doc['slug'] + ')\n'
			f.write(str2.encode("UTF-8"))


def getReposFromGroup(groupId):
	rawRepos = requests.get(url + '/groups/' + str(groupId) + '/repos', headers=headers)
	return rawRepos.json()['data']


def getDocsFromRepo(repoId):
	docs = requests.get(url + '/repos/' + str(repoId) + '/docs', headers=headers)
	docs = docs.json()['data']
	return docs


def updateRepoIndex(toc):
	print 'go to update index toc.'
	result = requests.put(url + '/repos/' + xiamiIndexRepo, headers=headers, data={'toc': toc})
	print str(result.json()['data']['toc'].encode('UTF-8'))


def login(userName, password):
	print('username: ' + userName + ", password: " + password)
	payload = {'username': userName, 'password': password}
	response = requests.post(url+'/authorize', data=payload, headers=headers)
	jsonData = response.json()
	token = jsonData['data']['private_token']
	if not token:
		print('token empty, login fail')
		exit()
	headers.update({'X-Auth-Token': token})


if __name__ == '__main__':
	main(str(sys.argv[1]), str(sys.argv[2]))