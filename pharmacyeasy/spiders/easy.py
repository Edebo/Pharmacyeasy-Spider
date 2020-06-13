# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import json


class EasySpider(Spider):
    name = 'easy'
    allowed_domains = ['pharmeasy.in']
    start_urls = ['https://pharmeasy.in/health-wellness']
    product_url ="https://pharmeasy.in/api/otc/getCategoryProducts?categoryId="
    pageEnd= False

    def parse(self, response):
        urls = response.xpath("//*[@class='_3nEAy']/@href").extract()
        for url in urls:
            self.pageEnd=False
            categoryId= url.split("-")[-1]
            print(categoryId)
            category_url = self.product_url + str(categoryId)

            for page in range(30):               
                if self.pageEnd:
                    break            
                page_url = category_url + "&page=" + str(page)
                yield Request(url=page_url ,callback=self.parse_category)

        
    
    def parse_category(self,response):
        jsonresponse = json.loads(response.text)

        if len(jsonresponse["data"]["products"]):           
            for product in jsonresponse['data']['products']:

                images= []
                if product["damImages"] is None:
                    try:
                        images = product["images"]
                    except KeyError as e:
                        images = ["No Image for this product"]
                    
                else:
                    for x in product["damImages"]:
                        images.append(x["url"])
               
                item={
                    "name":product['name'],
                    "slug":product["slug"],
                    "manufacturer":product["manufacturer"],
                    "price":product["salePriceDecimal"],
                    "availability":product["productAvailabilityFlags"]["isAvailable"],
                    "images":", ".join(images)
                }                
                yield item

        
        else:
            self.pageEnd=True