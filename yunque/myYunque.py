# coding=utf-8
# auto generated my fav-repos docs index and update remote.
# python myYunque.py username password

import sys
import requests

from common import official_url, url, headers
from common import login, getDocsFromRepo, updateRepoIndex

wingjayGroupId = 'wingjay'
wingjayIndexRepo = 'wingjay/index'

favRepoList = ['liuke.hf/nwny81', 'youku_android_arch/atlas', 'wdk-wireless/wphh88']
favRepoNameList = ['伙伴Android开发者', '优酷架构团队／Atlas', '盒马鲜生Android团队']

blackDocIdList = ['wdk-wireless/wphh88/hvgd84']

fileName = 'wingjayIndex.md'
f = open(fileName, 'w')


def main(user_name, password):
    print('go to login')
    login(user_name, password)

    for repo, name in zip(favRepoList, favRepoNameList):
        docs = getDocsFromRepo(repo)
        f.write('- [' + name + ']()\n')
        for doc in docs:
            if _filterDoc(repo, doc):
                line = ('\t- [' + doc['title'] + '](' + official_url + repo + '/' + doc['slug'] + ')\n').encode("UTF-8")
                f.write(line)
    f.close()

    _file = open(fileName, 'r')
    updateRepoIndex(wingjayIndexRepo, _file.read())


def _filterDoc(repo_namespace, doc):
    return repo_namespace + '/' + doc['slug'] not in blackDocIdList

if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]))
