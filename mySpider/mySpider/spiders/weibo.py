#coding:utf-8
import scrapy
import requests
import json
import base64
from mySpider import login_weibo2

class WeiboSpider(scrapy.Spider):
    username = 'jsb123000@qq.com' # 微博账号
    password = 'jsb520572123' # 微博密码
    uid='5627839527'
    name = 'weibo'
    cookies =None
    straturls=[]
    allowed_domains = ['weibo.cn','weibo.com','sina.com.cn']
    header={"User-Agen":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    def start_requests(self):
        # 这个方法当下载器开始发起请求之前被调用
        # 在这个方法我们可以把下载器截获，改变其原来的请求方式
        login_url = "https://passport.weibo.cn/sso/login" # post请求的接口url
        # post提交的数据
        data = {
            'username': self.username,
            'password': self.password,
            'savestate': '1',
            'r': 'https://weibo.cn/?luicode=20000174',
            'ec': '0',
            'pagerefer': 'https://weibo.cn/pub/?vt=',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }

        yield scrapy.FormRequest(url=login_url,formdata=data,callback=self.parse_login)

    def parse_login(self, response):

        # print(response.text)
        # 判断登录是否成功
        if json.loads(response.text)["retcode"] == 20000000:
            print("登录成功！")
            # 访问主页
            main_url = 'https://weibo.cn/'+self.uid+'/follow'
            yield scrapy.Request(url=main_url,callback=self.parse_info)

        else:
            print("登录失败！")

    def parse_info(self, response):
        # print(response.text)
        papers=response.xpath('//tr')
        for paper in papers:
            url=paper.xpath('./td[2]/a[1]/@href').extract_first()
            # title=paper.xpath('.//*[@class="postTitle"]/a/text()').extract()[0]
            # time=paper.xpath('.//*[@class="dayTitle"]/a/text()').extract()[0]
            # content=paper.xpath('.//*[@class="c_b_p_desc"]/text()').extract()[0]
            # print(url,title,time,content)
            self.straturls.append(url)
            # print(url)
        if response.xpath('//*[@id="pagelist"]/form/div/a/text()').extract()[0] == u'下页':
          next_href = response.xpath('//*[@id="pagelist"]/form/div/a/@href').extract()[0]
          yield scrapy.Request('https://weibo.cn' + next_href, callback=self.parse_info)
        else:
          yield self.parse()
        # nextpage=response.xpath('//div[(@id,"pagelist")]//from//div//a[1]//@href').extract_first()
        # href=nextpage.xpath('.
        # print(nextpage)
    def parse(self):
        print(self.straturls)
        



    '''
    weibo.com
    '''
    # def start_requests(self):
    #     if not self.cookies:
    #        self.cookies=login_weibo2.login(self.username,self.password,self.header)
    #     # return [scrapy.Request('https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)', meta = {'cookiejar': 1},callback=self.parse_login)]
    #     main_url = "https://weibo.com/"+self.uid+"/follow"
    #     yield scrapy.Request(url=main_url,dont_filter=True, cookies=self.cookies, callback=self.parse_info)
    # def parse_info(self, response):
    #     Cookie2 = response.request.headers.getlist('Cookie')
    #     print(Cookie2)
    #     print(response.text)
    #     return self.parse(response)
    # # def start_requests(self):
    # #     yield scrapy.Request('https://weibo.cn/'+self.uid+'/follow',cookies=self.cookie)
    # def parse(self,response):
    #     papers=response.xpath('//tr')
    #     for paper in papers:
    #         url=paper.xpath('./td[2]/a[1]/@href').extract_first()
    #         # title=paper.xpath('.//*[@class="postTitle"]/a/text()').extract()[0]
    #         # time=paper.xpath('.//*[@class="dayTitle"]/a/text()').extract()[0]
    #         # content=paper.xpath('.//*[@class="c_b_p_desc"]/text()').extract()[0]
    #         # print(url,title,time,content)
    #         print(url)
    #     nextpage=response.xpath('//div[contains(@class,"pa")]')
    #     href=nextpage.xpath('.from/div/a[1]@href').extract_first()
    #     print(href)
    # def start_requests(self):
    #     login_url = "https://passport.weibo.cn/signin/login"
    #     formdata = {
    #             'username': 'jsb123000@qq.com',
    #             'password': 'jsb520572123',
    #             'savestate': '1',
    #             'r': 'https: // weibo.cn /',
    #             'ec': '0',
    #             'pagerefer': 'https: // weibo.cn / pub /',
    #             'entry': 'mweibo',
    #             'wentry': '',
    #             'loginfrom': '',
    #             'client_id': '',
    #             'code': '',
    #             'qq': '',
    #             'mainpageflag': '1',
    #             'hff': '',
    #             'hfp': '',
    #     }
    #     yield scrapy.FormRequest(url=login_url, formdata=formdata, callback=self.parse_login)

    # def parse_login(self, response):
    #     print("+++++++++++++++++")
    #     #对响应体判断是否登录成功
    #     json_res = json.loads(response.text)
    #     if json_res["retcode"] == 20000000:
    #         #登陆成功，访问详情资料
    #         info_url = "https://weibo.cn/?since_id=GvDAIAMb0&max_id=GvCRr7fmv&prev_page=%d&page=%d"
    #         for i in range(1, 2):
    #             url = info_url % (i-1, i)
    #             yield scrapy.Request(url=url, callback=self.parse_info)
    #     else:
    #         print('登陆失败！')

    # def parse_info(self, response):
    #     weibo_list = response.xpath("//div[@class='c' and @id]")
    #     for weibo in weibo_list:
    #         div = weibo.xpath("./div")
    #         print(div)



