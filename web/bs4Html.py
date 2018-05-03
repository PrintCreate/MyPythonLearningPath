import requests, bs4
'''从网页加载'''
'''res = requests.get('http://www.baidu.com')
res.raise_for_status()
noStarchSoup = bs4.BeautifulSoup(res.text,"html.parser")'''
'''从本地html加载'''
exampleFile=open('E:\PythonCode\example.html')
exampleSoup=bs4.BeautifulSoup(exampleFile,"html.parser")
elems = exampleSoup.select('#author')
# 找出id="author"的元素。我们使用select('#author')返回一个列表，其中包含所有带有 id="author"的元素。我们将这个 Tag 对象的列表保存在变量中 elems，
'''
		soup.select('div')		            所有名为<div>的元素
		soup.select('#author') 	            带有 id  属性为 author 的元素
		soup.select('.notice')              所有使用 CSS class 属性名为 notice 的元素
		soup.select('div span')             所有在<div>元素之内的<span>元素
		soup.select('div > span')           所有直接在<div>元素之内的<span>元素， 中间没有其他元素
		soup.select('input[name]')          所有名为<input>，并有一个 name 属性，其值无所谓的元素
		soup.select('input[type="button"]') 所有名为<input>，并有一个 type 属性，其值为 button 的元素
'''
print(len(elems)) # 1 len(elems)告诉我们列表中有几个 Tag 对象
elems[0].getText() # 返回该元素的文本
print(elems[0].getText()) # Al Sweigart
print(str(elems[0])) # <span id="author">Al Sweigart</span>
print(elems[0].attrs) # {'id': 'author'}  返回一个字典值

pElems = exampleSoup.select('p')
print(len(pElems)) # 3
for i in pElems:
	print(str(i))
	print(i.getText())
