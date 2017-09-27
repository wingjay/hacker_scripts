# coding=utf-8
import requests

official_url = 'https://lark.alipay.com/'
url = 'https://lark.alipay.com/api/v2'
headers = {"Content-Type": "application/x-www-form-urlencoded"}


def login(user_name, password):
    print('username: ' + user_name + ", password: " + password)
    payload = {'username': user_name, 'password': password}
    response = requests.post(url+'/authorize', data=payload, headers=headers)
    json_data = response.json()
    token = json_data['data']['private_token']
    if not token:
        print('token empty, login fail')
        exit()
    headers.update({'X-Auth-Token': token})


def getReposFromGroup(group_id):
    raw_repos = requests.get(url + '/groups/' + str(group_id) + '/repos', headers=headers)
    return raw_repos.json()['data']


def getDocsFromRepo(repo_id):
    docs = requests.get(url + '/repos/' + str(repo_id) + '/docs', headers=headers)
    docs = docs.json()['data']
    return docs


def updateRepoIndex(repo_name_space, toc):
    print 'go to update index toc. for', repo_name_space
    result = requests.put(url + '/repos/' + repo_name_space, headers=headers, data={'toc': toc})
    print str(result.json()['data']['toc'].encode('UTF-8'))


def getDocString(repo_namespace, doc):
    return ('- [' + doc['title'] + '](' + repo_namespace + '/' + doc['slug'] + ')\n').encode("UTF-8")
