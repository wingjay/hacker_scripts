import requests
import time
from bs4 import BeautifulSoup

url='http://www.jianshu.com/users/da333fd63fe5/followers'
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Cookie': '_session_id=OGlMSE9KaEdzVjI0NFhJR2V3L2xrT0FmdGVleU5lU3Nza3NRQ1NqUFllRnpQdW5Qd01WTHNQbnN0Z0JPb0RQUUx4SkdVRjRnczF6bUU2RHZaKytvdVYvVlBWUDBwdzVRNW5MTzRkYWpXOUVQQkJ2WERER0FsSGgraDJVQ3JIdGljcjVoRWxqNGJqL2xzV1RVWlMxcU1RaTVhSG5qOUZXQm9EL0Z2UUhWVVJiOVZqaEdxWTlqWGlUemNUVm1zMkx2UUVUY0NYVkFBRmN4VjJEUnlHcEpZUCtpdWVXZzBtVXRyWmdybkh1YkNaelFXaVNWbFlqYk9aY2ZoaVBLMVRmemNlcG9mUFVHNTBLOWp6NmJYN01vdkpEeXN3NnNqT0R6ME4rUlYreGFHdUFnM0t0Qmc4dmtTQStTREF1b0N4TVR5MVFMRU9NUVdMWnRudC9lNkptQlVDd0JkVUVsbEpkZll0b1d0Qjdqa3ArTnl3T1c4ZjhibEZ2REF1TXdubkZnbjFWYnlZMTFnOHEzTTJ0bDRBUEdGME41RzBhODcxRzhINmY0WDBqdmhjZz0tLWQwTkg4NWV6RlRyZDNLQzBGMHFWdUE9PQ%3D%3D--06bafd366cb29bbc19651df6f3a4e47da941d57d; _maleskine_session=MjIzK2hkcitzQkhQbUNtT2xIZFg5U2lTZXQ4WG1XMjMxaW9xQzZucHk1dFZLUmYvQlFGUVRoczFvRVY0R3NyZCtRdXgrQWVBT1gvZ0ZaRlgrYlVOQnlXRmJ2TGx4QlZZUkFOY3NuNkRlUVdOVFZhK2xTNk9qaURyN240ejdiaFVOUkhDcmxadkpEUm1PR2RENVBHTnFVampNZDIrWFZZeGhQWUYwczZqNnNKK05aQnJvUVhyblExaFE2amx2NHZrUkpmSnRUaU50TlAweGlSbm5PYXZXRGlZV3dxVjAzVHNGdzN3KzVBMzJZMCtsR0M1UjBCYTNpdjFPYXdqNG1VcWliWXNGYUFFT21OUzRlREtGWmwrM0tpUmZsUGozeGkwdmpmMXR6RnMvbTkzODdCYmcxazhDdDUzcmwxV1E5QmtaNEUvYitkMlphaDFwSnZZSFBzWGVYSnNmL0V4NTdPZ3lBQ0pvaFArOHcxanhXeTl6T2d5UUxqNzZrR3hzRVRxdDRKQk5ZVHdVTm84cjZucjBDU2krVGRHaFI5YzV5RktLcDRHSHhHOTRIZz0tLWh3RktCN1NPeEQyT1JWdXpJaFUrVFE9PQ%3D%3D--a0974dd3e89ed89e2c4ebe1620aad39163a96a29; remember_user_token=W1syODE2NjVdLCIkMmEkMTAkcDhPV1ZGc0doS2FsbnJMR1ByajE5LiIsIjE1MDk0NDM0NzAuNTIxODM2OCJd--0878fd5b35fd99cc8c8fadbf594653f558cafa4b; _ga=GA1.2.955658140.1499324237; _gid=GA1.2.1157014670.1509265671; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1508985738,1508985758,1509089473,1509343549; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1509452223; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22281665%22%2C%22%24device_id%22%3A%2215f387ce9f02af-0bc506b3a5753d-31607c00-1296000-15f387ce9f192f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22search-recent%22%7D%2C%22first_id%22%3A%2215f387ce9f02af-0bc506b3a5753d-31607c00-1296000-15f387ce9f192f%22%7D; _m7e_session=6f1b9b643eba54bc8c8709e5aaf6c7d3'}

# already finished from 1 -> 100
start_page = 1
final_page = 101

fileName = '../headlessChrome/jianshu/followers.txt'
f = open(fileName, 'w')

def main():
	start_time=time.time()
	for page in range(start_page, final_page):
		find_single_page(page)
	f.close()	
	print 'time: ' + str(time.time() - start_time)

def find_single_page(current_page):
	print 'current_page: ', current_page
	result=requests.get(url, headers=headers, params={'page': current_page})
	html=result.text
	soup=BeautifulSoup(html, "html.parser")
	# print soup.prettify()
	
	user_list = soup.find(class_='user-list')
	a_tags = user_list.find_all('a', class_='avatar')
	for tag in a_tags:
		find_message_url("https://jianshu.com" + tag['href'])

def find_message_url(user_home_url):
	print 'user_home_url' + user_home_url
	retry = True
	while(retry):
		try:
			result=requests.get(user_home_url, headers=headers)
			retry = False
		except Exception as e:
			print 'Retry for user_home_url' + user_home_url
			print e
	html=result.text
	soup=BeautifulSoup(html, "html.parser")
	message_url = soup.find(class_='btn-hollow')['href']
	print 'find a message_url: ' + message_url
	f.write("https://jianshu.com" + message_url + '\n')

if __name__ == '__main__':
    main()