import scrapy
import datetime
import requests
import json
from scrapy import Selector
from target.items import *
from target.utils import extract_data, extract_distinct



class TargetScraperNew(scrapy.Spider):
    name = "target_new"


    def __init__(self, url=None, *args, **kwargs):
        super(TargetScraperNew, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % url]
        self.url = url
        self.tcin = url.split("?preselect=")[-1]
        self.headers = {
                        'authority': 'redsky.target.com',
                        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                        'accept': 'application/json',
                        'sec-ch-ua-mobile': '?0',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                        'origin': 'https://www.target.com',
                        'sec-fetch-site': 'same-site',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-dest': 'empty',
                        'referer': url,
                        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        }


    def start_requests(self):
        params = (
            ('key', 'ff457966e64d5e877fdbad070f276d18ecec4a01'),
            ('tcin', self.tcin),
            ('store_id', '3203'),
            ('has_store_id', 'true'),
            ('pricing_store_id', '3203'),
            ('scheduled_delivery_store_id', '3203'),
            ('has_scheduled_delivery_store_id', 'true'),
            ('has_financing_options', 'false'),
        )
        yield scrapy.FormRequest('https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1', self.parse,
                                 formdata=params, method="GET", headers=self.headers)

    def parse(self, response):
        data_json = json.loads(response.text)
        title = data_json["data"]["product"]["item"]["product_description"]["title"]
        description = data_json["data"]["product"]["item"]["product_description"]
        details_dict = data_json["data"]["product"]["item"]["product_description"]["bullet_descriptions"]
        price = data_json["data"]["product"]["price"]
        item = TargetItem()
        item.update({
            "url": self.url,
            "tcin": self.tcin,
            "upc": '',
            "price": price,
            "title": title,
            "description": description,
            "specs":
                details_dict
        })
        yield item