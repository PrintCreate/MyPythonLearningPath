#!python 3
# 打开网页，点击下一个，保存想要的东西(图片)，直到循环到第一个停止
import requests, os, bs4
url = 'http://xkcd.com'
os.makedirs('xkcd', exist_ok=True)
while not url.endswith('#'):
	print('Downloading page %s...' % url)
	res = requests.get(url)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text,"html.parser")
	comicElem = soup.select('#comic img')

	if comicElem == []:
		print('Could not find comic image.')
	else:
		comicUrl = 'http:'+comicElem[0].get('src')
		comicElem[0].get('src')

		# Download the image.
		print('Downloading image %s...' % (comicUrl))
		res = requests.get(comicUrl)
		res.raise_for_status()

		# Save the image to ./xkcd.
		#调用 os.path.basename()时传入 comicUrl，它只返回 URL 的最后部分： 'heartbleed_explanation.png'。
		imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()
	# Get the Prev button's url.
	prevLink = soup.select('a[rel="prev"]')[0]
	url = 'http://xkcd.com' + prevLink.get('href')
print('Done.')