# coding=utf-8
# auto generated xiami docs index and update remote.
# python yunque.py username password
import sys
import requests

from common import url, headers
from common import login, getReposFromGroup, updateRepoIndex, getDocString


xiamiMobileGroupId = 'xiami-mobile'
xiamiIndexRepo = 'xiami-mobile/index'

androidTitleFilter = ('android', u'安卓')
iosTitleFilter = ('ios')

fileName = 'xiamiIndex.md'
f = open(fileName, 'w')


def main(user_name, password):
    print('go to login')
    login(user_name, password)
    repos = getReposFromGroup(xiamiMobileGroupId)

    android_repos = []
    ios_repos = []
    both_repos = []
    for repo in repos:
        repo_name = repo['name'].lower()
        if any(_filter in repo_name for _filter in androidTitleFilter):
            android_repos.append(repo)
        elif any(_filter in repo_name for _filter in iosTitleFilter):
            ios_repos.append(repo)
        else:
            both_repos.append(repo)

    f.write('- [Android]()\n')
    printRepoDocs(android_repos)
    f.write('- [iOS]()\n')
    printRepoDocs(ios_repos)
    f.write('- [其他]()\n')
    printRepoDocs(both_repos)
    f.close()
    print('generated index in' + fileName)

    _file = open(fileName, 'r')
    updateRepoIndex(xiamiIndexRepo, _file.read())


def printRepoDocs(repos):
    for repo in repos:
        docs = requests.get(url + '/repos/' + str(repo['id']) + '/docs', headers=headers)
        docs = docs.json()['data']
        if len(docs) <= 0:
            continue
        docs = sorted(docs, key=lambda d: d['updated_at'], reverse=True)
        str1 = '\t- [' + repo['name'] + ']()\n'
        f.write(str1.encode("UTF-8"))
        for doc in docs:
            f.write('\t\t' + getDocString(repo['slug'], doc))


if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]))
