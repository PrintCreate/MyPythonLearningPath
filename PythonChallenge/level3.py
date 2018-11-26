import re
import urllib.request

req=urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/equality.html")
res=req.read()
res=res.decode("UTF-8")
str=''.join(re.findall('<!--(.*)-->',res,re.S))
reg=re.compile('[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]')
chars= ''.join(reg.findall(str))
print(chars)