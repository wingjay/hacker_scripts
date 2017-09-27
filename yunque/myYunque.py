# coding=utf-8
# auto generated my fav-repos docs index and update remote.
# python myYunque.py username password

import sys
import requests

from common import official_url, url, headers
from common import login, getDocsFromRepo, updateRepoIndex, getRepoToc

wingjayGroupId = 'wingjay'
wingjayIndexRepo = 'wingjay/index'

favRepoList = [
    ('yksq/yo9016', '优酷大社区客户端文档', True),
    ('liuke.hf/nwny81', '伙伴Android开发者', False),
    ('youku_android_arch/atlas', '优酷架构团队／Atlas', False),
    ('wdk-wireless/wphh88', '盒马鲜生Android团队', True),
    ('aone488674/androidnewcomers', '支付宝 Android 新人引导', False),
    ('userexperience-arch-of-tmall-mobile/bvs3k9', '天猫Android架构优化&稳定性', False),
    ('userexperience-arch-of-tmall-mobile/app_on_diet_android', '天猫Android包瘦身文档', True),
]

blackDocIdList = ['wdk-wireless/wphh88/hvgd84']

fileName = 'wingjayIndex.md'
f = open(fileName, 'w')


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


def main(user_name, password):
    print('go to login')
    login(user_name, password)

    for repo, name, has_toc in favRepoList:
        if has_toc:
            f.write('- [' + name + ']()\n')
            toc = '\t' + getRepoToc(repo)
            toc = toc.replace('](https://lark.alipay.com/*)', '](')
            toc = toc.replace('](', '](' + official_url + repo + '/').replace('](' + official_url + repo + '/)', ']()')
            toc = replace_last(toc, '\n\n', '').strip(' ')
            toc = toc.replace('\n', '\n\t').rstrip('\t')
            f.write(toc)
            continue
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
