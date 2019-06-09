# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from mySpider.settings import IMAGES_STORE
import os
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem


class MyspiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [
            scrapy.Request(x, meta={'item': item})
            for x in item.get(self.images_urls_field, [])
        ]

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item_new = request.meta['item']
        # image_guid = item_new['auth'] + ' ' + request.url.split('/')[-1]
        # filename = '{0}'.format(image_guid)
        folder_name = item_new['auth']
        image_guid = request.url.split('/')[-1]
        filename = '{0}/{1}'.format(folder_name, image_guid)

        return filename

    # def process_item(self, item, spider):
    #     fold_name = "".join(item['title'])
    #     images = []
    #     header = {
    #         'USER-Agent':
    #         'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    #         'Cookie': 'b963ef2d97e050aaf90fd5fab8e78633',
    #         #需要查看图片的cookie信息，否则下载的图片无法查看
    #     }
    #     # 所有图片放在一个文件夹下
    #     dir_path = '{}'.format(IMAGES_STORE)
    #     if not os.path.exists(dir_path) and len(item['src']) != 0:
    #         os.mkdir(dir_path)
    #     if len(item['src']) == 0:
    #         with open('..//check.txt', 'a+') as fp:
    #             fp.write("".join(item['title']) + ":" + "".join(item['url']))
    #             fp.write("\n")

    #     for jpg_url, num in zip(item['src'], range(0, 100)):
    #         file_name = str(num)
    #         file_path = '{}//{}'.format(dir_path, file_name)
    #         images.append(file_path)
    #         if os.path.exists(file_path) or os.path.exists(file_name):
    #             continue

    #         with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
    #             req = requests.get(jpg_url, headers=header)
    #             f.write(req.content)

    #     return item
