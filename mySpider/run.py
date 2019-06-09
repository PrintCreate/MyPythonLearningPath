from scrapy.cmdline import execute
import os
import sys
from collections import Counter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute('scrapy crawl weibo -s JOBDIR=scrapyjob/001'.split())
execute('scrapy crawl weibo'.split())
# L = []
# for root, dirs, files in os.walk('d://pic2'):
#     for file in files:
#         # if os.path.splitext(file)[1] == '.jpg':
#         L.append(os.path.splitext(file)[0])
# print(L)
# d = {}
# for x in set(L):
#     d[x] = L.count(x)
#     print(d)
