#open Firefox 找名为有类名'bookcover'的元素我们就用 tag_name 属性将它的标签名打印出来
'''
from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://inventwithpython.com')
try:
	elem = browser.find_element_by_class_name('bookcover')
	print('Found <%s> element with that class name!' % (elem.tag_name))
except:
	print('Was not able to find an element with that name.')
'''


#模拟点击事件 进行该元素的点击事件   跳转 or everything
'''
from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://inventwithpython.com')
linkElem = browser.find_element_by_link_text('Read Online for Free')
linkElem.click()
'''

# 自动登录
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
browser = webdriver.Firefox()
#browser = webdriver.Chrome()
browser.get('https://mail.163.com')
delay = 3
browser.switch_to.frame("login_frame")
try:
    WebDriverWait(browser, delay).until(EC.presence_of_element_located(('id', 'u')))
    print ('Page is ready!')
except TimeoutException:
    print('Loading took too much time!')
emailElem = browser.find_element_by_id('auto-id-1523796868387')
emailElem.send_keys('15552739296')
passwordElem = browser.find_element_by_id('auto-id-1523796868351')
passwordElem.send_keys('jsb123000')
passwordElem.submit()
'''


# send 特殊按键
'''
Keys.DOWN, Keys.UP, Keys.LEFT,Keys.RIGHT 键盘箭头键
Keys.ENTER, Keys.RETURN 回车和换行键
Keys.HOME, Keys.END,
Keys.PAGE_DOWN,Keys.PAGE_UP
Home 键、 End 键、 PageUp 键和 Page Down 键
Keys.ESCAPE, Keys.BACK_SPACE,Keys.DELETE Esc、 Backspace 和字母键
Keys.F1, Keys.F2, ... , Keys.F12 键盘顶部的 F1到 F12键
Keys.TAB Tab 键'''
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser = webdriver.Firefox()
browser.get('https://gabrielecirulli.github.io/2048/')
htmlElem = browser.find_element_by_tag_name('html')
js="var q=document.documentElement.scrollTop=50"
browser.execute_script(js)
htmlElem.send_keys(Keys.DOWN)
htmlElem.send_keys(Keys.UP)
'''


# 模拟浏览器的后退、前进、退出、刷新
'''
browser.back()点击“返回”按钮。
browser.forward()点击“前进”按钮。
browser.refresh()点击“刷新”按钮。
browser.quit()点击“关闭窗口”按钮。
'''