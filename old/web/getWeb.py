import requests,sys
# requests.get 获得到整个网页
res = requests.get('http://www.gutenberg.org/cache/epub/1112/pg1112.txt')
try:
		# 通过检查 Response 对象的 status_code 属性，你可以了解对这个网页的请求是否成功。如果该值等于 requests.codes.ok，那么一切都好
        res.raise_for_status()
except Exception as exc:
        print('There was a problem: %s' % (exc))
# 验证是否连接成功 成功则继续
if res.status_code==requests.codes.ok:
	playFile = open('E:\PythonCode\RomeoAndJuliet.txt', 'wb')
	for chunk in res.iter_content(100000):
		playFile.write(chunk)
	playFile.close()
	print('OK!')
