import re
import urllib.request

r=re.compile(r'(\d+)$')
beginNum="8022"
while(1):
    try:
        req = urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%s"%beginNum)
        res = req.read()
        res = res.decode("UTF-8")
        print(res)
        beginNum=(r.search(res).group())
    except:
        print("beginNum:%s"%beginNum)


