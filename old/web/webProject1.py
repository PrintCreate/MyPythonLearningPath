#! python3
#根据搜索引擎每个标题的类名 打开前几个地址
import requests, sys, webbrowser, bs4

print('Googling...')
res = requests.get('https://www.google.com/search?q='+''.join(sys.argv[1:]))
#res = requests.get('https://www.baidu.com/s?wd='+''.join(sys.argv[1:]))
try:
	res.raise_for_status()
except Exception as exc:
	print('There was a problem: %s' % (exc))
if res.status_code==requests.codes.ok:
	soup = bs4.BeautifulSoup(res.text,"html.parser")
	#linkElems = soup.select('c-gap-bottom-small a')
	linkElems = soup.select('.r a')
	numOpen = min(5, len(linkElems))
	for i in range(numOpen):
		#webbrowser.open('http://www.baidu.com' + linkElems[i].get('href'))
		webbrowser.open('http://www.google.com' + linkElems[i].get('href'))