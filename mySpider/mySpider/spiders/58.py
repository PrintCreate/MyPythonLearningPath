import scrapy
from openpyxl import Workbook
import re
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup
import base64
import io
import html
class FangTianXiaSpider(scrapy.Spider):
    name = '58Spider'
    allowed_domains = ['dy.58.com']
    wb = Workbook()
    ws = wb.active
    # 租房
    # def start_requests(self):
    #     login_url = "https://dy.58.com/dydongcheng/chuzu/" # post请求的接口ur
    #     yield scrapy.FormRequest(url=login_url,callback=self.parse)
    # def parse(self,response):
    #     tex = response.text
    #     tex = html.unescape(response.text)
    #     key = re.findall(r"base64,(.*)'\).format", tex)[0]
    #     dehtml = self.decode58Fangchan(tex, key)
    #     soup = BeautifulSoup(dehtml, "lxml")
    #     ul = soup.select('body > div.mainbox > div > div.content > div.listBox > ul > li')
    #     try:
    #         for li in ul:
    #             title =  li.select('div.des > h2')[0].text.strip()
    #             href=li.select('div.des > h2 > a.strongbox')[0].get("href")
    #             jieshao =li.select('div.des > p.room.strongbox')[0].text.strip()
    #             price=li.select('div.listliright > div.money')[0].text.strip()
    #             # address=li.select('div.des > p.add >a')[1].text.strip()
    #             print(title,price,href,jieshao)
    #             self.ws.append([title,price,href,jieshao])
            # try:
    #             next_page=soup.select('#bottom_ad_li > div.pager > a.next')[0].get("href")
    #             print(next_page)
    #             yield scrapy.Request(url=next_page,callback=self.parse)
    #         except:
    #             self.wb.save('d:/1.xlsx')
    #     except :
    #         try:
    #             next_page=soup.select('#bottom_ad_li > div.pager > a.next')[0].get("href")
    #             print(next_page)
    #             yield scrapy.Request(url=next_page,callback=self.parse)
    #         except:
    #             self.wb.save('d:/1.xlsx')
    
    
    # 二手房
    def start_requests(self):
        login_url = "https://dy.58.com/dydongcheng/ershoufang/" # post请求的接口ur
        yield scrapy.FormRequest(url=login_url,callback=self.parse)
    def parse(self,response):
        tex = response.text
        soup = BeautifulSoup(tex, "lxml")
        ul = soup.select('body > div.main-wrap > div.content-wrap > div.content-side-left > ul > li')
        try:
            for li in ul:
                title =  li.select('div.list-info > h2')[0].text.strip()
                href=li.select('div.list-info > h2 > a')[0].get("href")
                jieshao =li.select('div.list-info > p:nth-of-type(1) > span:nth-of-type(1)')[0].text.strip()
                jieshao =jieshao+' '+li.select('div.list-info > p:nth-of-type(1) > span:nth-of-type(2)')[0].text.strip()
                jieshao =jieshao+' '+li.select('div.list-info > p:nth-of-type(1) > span:nth-of-type(3)')[0].text.strip()
                jieshao =jieshao+' '+li.select('div.list-info > p:nth-of-type(1) > span:nth-of-type(4)')[0].text.strip()
                address=li.select('div.list-info > p:nth-of-type(2) > span > a:nth-of-type(1)')[0].text.strip()
                address=address+' '+li.select('div.list-info > p:nth-of-type(2) > span > a:nth-of-type(2)')[0].text.strip()
                address=address+' '+li.select('div.list-info > p:nth-of-type(2) > span > a:nth-of-type(3)')[0].text.strip()
                sumprince=li.select('div.price > p.sum')[0].text.strip()    
                price=li.select('div.price > p.unit')[0].text.strip()
                print(title,price,sumprince,address,href,jieshao)
                self.ws.append([title,price,jieshao,sumprince,address,href])
            try:
                next_page=soup.select('body > div.main-wrap > div.content-wrap > div.content-side-left > div.pager > a.next')[0].get("href")
                print(next_page)
                yield scrapy.Request(url='https://dy.58.com'+next_page,callback=self.parse)
            except:
                self.wb.save('d:/1.xlsx')
        except BaseException as e:
            print(e) 
            try:
                next_page=soup.select('body > div.main-wrap > div.content-wrap > div.content-side-left > div.pager > a.next')[0].get("href")
                print(next_page)
                yield scrapy.Request(url='https://dy.58.com'+next_page,callback=self.parse)
            except:
                self.wb.save('d:/1.xlsx')
    
    
    # 通用解析58乱码转数字
    def decode58Fangchan(self,html,key):
        glyphdict = {
            'glyph00001': '0',
            'glyph00002': '1',
            'glyph00003': '2',
            'glyph00004': '3',
            'glyph00005': '4',
            'glyph00006': '5',
            'glyph00007': '6',
            'glyph00008': '7',
            'glyph00009': '8',
            'glyph00010': '9'
        }    
        data = base64.b64decode(key)  #base64解码
        fonts = TTFont(io.BytesIO(data))  #生成二进制字节
        cmap = fonts.getBestCmap()  #十进制ascii码到字形名的对应{38006:'glyph00002',...}
        chrMapNum = {}  #将变为{‘龥’:'1',...}
        for asc in cmap:
            chrMapNum[chr(asc)] = glyphdict[cmap[asc]]

        return self.multReplace(html,chrMapNum)
    def multReplace(self,text, rpdict):
        rx = re.compile('|'.join(map(re.escape, rpdict)))
        return rx.sub(lambda match:rpdict[match.group(0)], text)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      # div=response.xpath('//dl[@class="clearfix"]')
      # for detail in div:
      #   title=detail.xpath('./dd[1]/h4[@class="clearfix"]/a/span[@class="tit_shop"]/text()').extract()[0]
      #   href=self.base_url+detail.xpath('./dd[1]/h4[@class="clearfix"]/a/@href').extract()[0]
      #   jieshao=detail.xpath('./dd[1]/p[@class="tel_shop"]/text()').extract()[1].strip()
      #   # jieshao=''
      #   # for jianjie in jianjielist:
      #   #   jieshao=jieshao+' '+jianjie.strip()
      #   price=detail.xpath('./dd[2]/span[2]/text()').extract()[0]
      #   zongjia=detail.xpath('./dd[2]/span[1]/b/text()').extract()[0]+detail.xpath('./dd[2]/span[1]/text()').extract()[0]
      #   self.ws.append([title,jieshao,price,zongjia,href])
      #   print(title,jieshao,price,zongjia,href)
      # try:
      #   next_page=response.xpath('//a[contains(text(),"下一页")]/@href').extract()[0]
      #   if next_page!='':
      #       if self.base_url+next_page not in self.url:
      #         self.url.append(self.base_url+next_page)
      #         yield scrapy.Request(url=self.base_url+next_page,callback=self.findpage)
      #   else:
      #     pass
      # except:
      #   self.wb.save('d:/1.xlsx')
        
      