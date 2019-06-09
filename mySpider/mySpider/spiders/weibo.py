#coding:utf-8
import scrapy
import requests
import json
import base64
from mySpider import login_weibo2
from mySpider.items import MyspiderItem
from urllib import request
import re
import os
from retry import retry


class WeiboSpider(scrapy.Spider):
    # 用weibo 取setting 开启 DEFAULT_REQUEST_HEADERS
    username = 'jsb123000@qq.com'  # 微博账号
    password = 'jsb520572123'  # 微博密码
    uid = '5627839527'
    name = 'weibo'
    cookies = None
    straturls = []
    start_urls = []
    allowed_domains = ['weibo.cn', 'm.weibo.cn']
    base_url = 'https://weibo.cn'
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value={uid}&containerid=100505{uid}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value={uid}&containerid=107603{uid}'

    # L = []
    # for root, dirs, files in os.walk('d://pic2'):
    #     for file in files:
    #         # if os.path.splitext(file)[1] == '.jpg':
    #         L.append(os.path.splitext(file)[0])
    # header={"User-Agen":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    def start_requests(self):
        # 这个方法当下载器开始发起请求之前被调用
        # 在这个方法我们可以把下载器截获，改变其原来的请求方式
        login_url = "https://passport.weibo.cn/sso/login"  # post请求的接口url
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

        yield scrapy.FormRequest(url=login_url,
                                 formdata=data,
                                 callback=self.parse_login)

    def parse_login(self, response):
        # 判断登录是否成功
        if json.loads(response.text)["retcode"] == 20000000:
            print("登录成功！")
            # 访问主页
            main_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231093_-_selffollowed'
            #main_url ='https://m.weibo.cn/' + self.uid + '/follow'
            yield scrapy.Request(url=main_url, callback=self.parse_guanZhu)

        else:
            print("登录失败！")

    @retry(tries=5, delay=5)
    def parse_guanZhu(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(
                result.get('data').get('cards')) and result.get('data').get(
                    'cards')[-1].get('card_group'):
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                # auth = follow.get('desc1')
                auth = follow.get('user').get('screen_name')
                uid = follow.get('user').get('id')
                print(auth, uid)
                request = scrapy.Request(self.weibo_url.format(uid=uid),
                                         callback=self.parse_info)
                request.meta['auth'] = auth
                request.meta['uid'] = uid
                yield request

    def parse_info(self, response):
        # &since_id={since_id}
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            since_id = result.get('data').get('cardlistInfo').get('since_id')
            auth = response.meta['auth']
            uid = response.meta['uid']
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog and mblog.get('pics'):
                    pics = mblog.get('pics')
                    for pic in pics:
                        picurl = pic.get('large').get('url')
                        print(since_id, auth, picurl)
                        path = 'd://pic2//' + auth + '//' + re.sub(
                            'https://wx\\d.sinaimg.cn/large/', '', picurl)
                        if not os.path.exists(path):
                            item = MyspiderItem()
                            item['auth'] = auth
                            item['images_urls'] = [picurl]
                            yield item
                            url = self.weibo_url.format(
                                uid=uid) + '&since_id=' + str(since_id)
                            request = scrapy.Request(url,
                                                     callback=self.parse_info)
                            request.meta['auth'] = auth
                            request.meta['uid'] = uid
                            yield request


# https://m.weibo.cn/u/2974645912?uid=2974645912&luicode=10000011&lfid=231093_-_selffollowed
# https://m.weibo.cn/api/container/getIndex?uid=2974645912&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value=2974645912&containerid=1005052974645912
# https://m.weibo.cn/api/container/getIndex?uid=2974645912&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value=2974645912&containerid=1076032974645912
# https://m.weibo.cn/api/container/getIndex?uid=2974645912&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value=2974645912&containerid=1076032974645912&since_id=4374040841673393
# @retry(tries=5, delay=5)
# def parse_info(self, response):
#     result = json.loads(response.text)
#     print(result)
#     papers = response.xpath('//tr')
#     for paper in papers:
#         url = paper.xpath('./td[2]/a[1]//@href').extract_first()
#         self.straturls.append(url)
#     if response.xpath('//*[@id="pagelist"]/form/div/a//text()').extract(
#     )[0] == u'下页':
#         next_href = response.xpath(
#             '//*[@id="pagelist"]/form/div/a//@href').extract()[0]
#         yield scrapy.Request(self.base_url + next_href,
#                              callback=self.parse_info)
#     else:
#         for url in self.straturls:
#             yield scrapy.Request(url, callback=self.parse)

# # 取所有微博图片链接
# @retry(tries=5, delay=5)
# def parse(self, response):
#     # name = response.xpath('//title//text()').extract()[0]
#     # print(name)
#     papers = response.xpath(
#         '//a[re:test(@href,"^https://weibo.cn/mblog/pic/[a-zA-Z0-9?]+rl=0$")]//@href'
#     ).extract()
#     for href in papers:
#         yield scrapy.Request(
#             href,
#             callback=self.view_ListPic,
#         )

# # 进入微博组图
# @retry(tries=5, delay=5)
# def view_ListPic(self, response):
#     source_Pic = response.xpath('//img//@src').extract()[0]
#     picName = re.sub('http://ww\\d.sinaimg.cn/bmiddle/', '', source_Pic)
#     if picName not in self.L:
#         request.urlretrieve(source_Pic, 'd://pic//' + picName)
#         self.L.append(picName)
#     # item = MyspiderItem()
#     # if source_Pic not in item:
#     #     item['title'] = 's'  #name
#     #     item['src'] = source_Pic
#     #     print(item)
#     #     yield item
#     try:
#         page = response.css('body > div:nth-child(4) > div:nth-child(4)')
#         if page:
#             if page.xpath('./a[1]//text()').extract()[0] == '下一张':
#                 next_page = response.xpath(
#                     '//div[@class="tc"][last()]/a[1]//@href').extract()[0]
#                 yield scrapy.Request(self.base_url + next_page,
#                                      callback=self.view_ListPic)
#     except:
#         page = response.css('body > div:nth-child(3) > div:nth-child(4)')
#         if page:
#             if page.xpath('./a[1]//text()').extract()[0] == '下一张':
#                 next_page = response.xpath(
#                     '//div[@class="tc"][last()]/a[1]//@href').extract()[0]
#                 yield scrapy.Request(self.base_url + next_page,
#                                      callback=self.view_ListPic)

# def downLoadPic(self, response):
#     print(response.text())

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
