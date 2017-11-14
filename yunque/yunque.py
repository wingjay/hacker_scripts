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
    f.write('- [客户端公共]()\n')
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
        docs = sorted(docs, key=lambda d: d['title'], reverse=False)
        str1 = '\t- [' + repo['name'] + ']()\n'
        f.write(str1.encode("UTF-8"))
        for doc in docs:
            f.write('\t\t' + getDocString(repo['slug'], doc))


if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]))

"""
doc:
{u'content_updated_at': u'2017-10-15T10:21:40.000Z',
  u'created_at': u'2017-10-10T05:28:39.000Z',
  u'format': u'asl',
  u'id': 373919,
  u'public': 1,
  u'slug': u'tkzgge',
  u'status': 0,
  u'title': u'OnLineMonitor\uff1a\u754c\u9762\u9996\u5f00\u7684\u4e00\u6b21\u4f18\u5316',
  u'updated_at': u'2017-10-16T01:48:14.000Z'}

repo:
{u'created_at': u'2017-09-21T12:20:16.000Z',
 u'description': u'\u867e\u7c73\u5ba2\u6237\u7aef\u5168\u90e8\u6587\u7ae0\u7d22\u5f15[\u811a\u672c\u81ea\u52a8\u751f\u6210\uff0c\u8bf7\u52ff\u624b\u52a8
\u4fee\u6539\uff0c\u6709\u95ee\u9898\u6216\u610f\u89c1\u8bf7\u8054\u7cfb \u51b2\u7075]',
 u'id': 51041,
 u'name': u'\u76ee\u5f55\u7d22\u5f15',
 u'namespace': u'xiami-mobile/index',
 u'public': 1,
 u'slug': u'index',
 u'type': u'Book',
 u'updated_at': u'2017-10-25T06:16:11.000Z',
 u'user': {u'avatar_url': u'https://zos.alipayobjects.com/skylark/1e7e516e-d6af-4a0f-afea-1414d39b2184/avatar/c97aa44455310a2a/globalbtnsharexiami3x.png
',
  u'created_at': u'2017-02-27T04:53:09.000Z',
  u'email': None,
  u'id': 24208,
  u'login': u'xiami-mobile',
  u'name': u'\u867e\u7c73\u5ba2\u6237\u7aef',
  u'updated_at': u'2017-10-23T05:44:09.000Z',
  u'work_id': None},
 u'user_id': 24208}  
"""
