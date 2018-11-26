import re
import urllib.request

req=urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/ocr.html")
res=req.read()
res=res.decode("UTF-8")
str=''.join(re.findall('<!--\n%(.*)-->',res,re.S))
print("".join(re.compile(r'[a-z]').findall(str)))
# print(str)
# equality