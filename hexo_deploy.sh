#!/bin/sh
# 1. input article file path
# 2. create a new issue, including article title and link
# 3. deploy hexo

# Fetch title/date/permalink from .md file

articlePath=$1
title=''
date=''
permalink=''
commentIssueId=''

ACCESS_TOKEN='1b50ce9a7fc027fa619276c86c4b4831c0a86b02'

deployAll() {
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
}

readFromMdFile() {
	argument_count=0
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
	    elif [[ $line == commentIssueId:* ]]; then
	    	commentIssueId=$(echo $line|cut -d" " -f2)
	    	argument_count=$(($argument_count+1))
	    fi
	    if [[ $argument_count == 4 ]]; then
	    	break
	    fi  
	done < "$articlePath"

	date=`echo $date | tr '-' '/'`
}

createIssue() {
	echo 'Creating Issue....'
	# generate article data
	body='文章地址：http://wingjay.com/'$date'/'$permalink
	data='{"title":"《'$title'》评论","body":"'$body'"}'
	echo data: $data

	# create a issue with title + link
	commentId=$(curl --silent -H "Content-Type: application/json" -u wingjay:$ACCESS_TOKEN -X POST -d $data https://api.github.com/repos/wingjay/hellojava/issues | jq -r '.number')
	if [[ $commentId == null ]]; then
		echo "---------\nError: token失效了吧\n---------"
		exit 1
	else 
		return $commentId	
	fi
}

# no input -> deploy
if [ "$#" == 1 ]; then
	echo "---------\n为指定文章创建Issue后再deploy\n---------"
	readFromMdFile
	echo title: $title
	echo date: $date
	echo permalink: $permalink
	echo commentIssueId: $commentIssueId
	if [[ $commentIssueId == commentIssueId:* ]]; then
		echo "---------\n无相关Issue，开始创建Issue\n----------"
		createIssue
		createdIssueId=$?
		echo "新创建的IssueId:" $createdIssueId
		echo "---------\n准备添加IssueId到文章中\n---------"
		sed -i -e "s/commentIssueId.*/commentIssueId: $createdIssueId/" $articlePath
		readFromMdFile
		if [[ $commentIssueId == commentIssueId:* ]]; then
			echo "写入commentIssueId失败，请手动写入后直接deploy：" $createdIssueId
			exit 1
		fi
		echo commentIssueId: $commentIssueId
		echo "---------\nIssueId添加成功，开始deploy\n---------"
		deployAll
	else 
		echo "---------\n已存在Issue，直接Deploy\n---------"
		deployAll
	fi
elif [[ "$#" == 0 ]]; then
	echo "---------\n直接deploy\n---------"
	deployAll
else
	echo "参数错误"
	exit 1	
fi








