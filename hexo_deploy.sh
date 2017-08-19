#!/bin/sh
# 1. input must contains: title + date + permalink
# 2. create a new issue, including article title and link
# 3. deploy hexo
if [ "$#" -ne 3 ]; then
	echo "must input arguments: title date(2017-08-06) permalink"
	exit 1
fi

# TODO: fetch title/date/permalink from .md file
title=$1
createDate=`echo $2 | tr '-' '/'`
permalink=$3

# generate article link
link='文章地址：http://wingjay.com/'$createDate'/'$permalink
echo $link

data='{"title":"《'$1'》评论","body":"'$link'"}'

# create a issue with title + link
commentId=$(curl --silent -H "Content-Type: application/json" -u wingjay:5871be02a817be2afd733ffbdbd6f5f8b1cb1289 -X POST -d $data https://api.github.com/repos/wingjay/hellojava/issues | jq -r '.number')
echo $commentId

# replace commentId

# deploy

cd ~/Documents/wingjay.github.io
hexo generate
cp -R public/ .deploy/wingjay.github.io
cd .deploy/wingjay.github.io
git add .
git commit -m "update"
git push origin master
cd -
git add .
git commit -m "source code"
git push origin code
