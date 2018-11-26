# coding:utf-8
import urllib.request
from lxml import etree
import requests


def Schedule(blocknum, blocksize, totalsize):
	'''

	:param blocknum: 已下载的数据块
	:param blocksize: 数据块的大小
	:param totalsize: 远程文件的大小
	:return:
	'''
	per = 100.0 * blocknum * blocksize / totalsize
	if per > 100:
		per = 100
		print('当前下载进度', per)


user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
r = requests.get('http://www.ivsky.com/tupian/ziranfengguang', headers=headers)
html = etree.HTML(r.text)
img_urls = html.xpath('.//img/@src')
i = 0
for img_url in img_urls:
	urllib.request.urlretrieve(img_url, 'img' + str(i) + '.jpg', Schedule)
	i += 1
