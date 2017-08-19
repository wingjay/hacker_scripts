#!/bin/sh
# 1. input article file path
# 2. create a new issue, including article title and link
# 3. deploy hexo
if [ "$#" -ne 1 ]; then
	echo "必须输入文章路径"
	exit 1
fi

# Fetch title/date/permalink from .md file
argument_count=0
title=''
date=''
permalink=''
while IFS='' read -r line || [[ -n "$line" ]]; do
    if [[ $line == title:*  ]]; then 
        title=$(echo $line|cut -d" " -f2)
        argument_count=$(($argument_count+1))
    elif [[ $line == date:* ]]; then
    	date=$(echo $line|cut -d" " -f2)
    	argument_count=$(($argument_count+1))
    elif [[ $line == permalink:* ]]; then
    	permalink=$(echo $line|cut -d" " -f2)
    	argument_count=$(($argument_count+1))
    fi
    if [[ $argument_count == 3 ]]; then
    	break
    fi  
done < "$1"

date=`echo $date | tr '-' '/'`

# generate article link
link='文章地址：http://wingjay.com/'$date'/'$permalink
data='{"title":"《'$title'》评论","body":"'$link'"}'
echo data: $data

# create a issue with title + link
commentId=$(curl --silent -H "Content-Type: application/json" -u wingjay:9d2ee1a50153311040db7f6d6ea8e46865d8b3d1 -X POST -d $data https://api.github.com/repos/wingjay/hellojava/issues | jq -r '.number')
echo commentId: $commentId

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
