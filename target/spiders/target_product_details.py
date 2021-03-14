import scrapy
import datetime
import requests
import json
from scrapy import Selector
from target.items import *
from target.utils import extract_data, extract_distinct



class TargetScraper(scrapy.Spider):
    name = "target"


    def __init__(self, url=None, *args, **kwargs):
        super(TargetScraper, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % url]
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


    def parse(self, response):
        sel = Selector(response)
        print(response.url)
        url = response.url
        title = extract_data(sel, '//div//h1[@data-test="product-title"]//text()')
        description = extract_data(sel, '//div[@class="h-margin-v-default"]//text()')
        other_details = extract_distinct(sel,
                                         '//div[@class="Col__StyledCol-sc-1yf5b3p-0 hodSWf h-padding-h-default"]//text()')
        other_details_list = other_details.split("\n")
        other_details_list_modified = [item for item in other_details_list if item != ':']
        details_dict = {other_details_list_modified[i]: other_details_list_modified[i + 1] for i in
                        range(1, len(other_details_list_modified), 2)}
        tcin = details_dict['TCIN']
        upc = details_dict['UPC']
        params = (
            ('key', 'ff457966e64d5e877fdbad070f276d18ecec4a01'),
            ('tcin', tcin),
            ('store_id', '3203'),
            ('has_store_id', 'true'),
            ('pricing_store_id', '3203'),
            ('scheduled_delivery_store_id', '3203'),
            ('has_scheduled_delivery_store_id', 'true'),
            ('has_financing_options', 'false'),
        )
        yield scrapy.FormRequest('https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1', self.get_price,
                                 formdata=params, method="GET", headers=self.headers, meta={"url": url,"tcin": tcin,"upc": upc,"title": title,"description": description,"specs": details_dict})

    def get_price(self, response):
        url = response.meta.get("url")
        title = response.meta.get("title")
        description = response.meta.get("description")
        tcin = response.meta.get("tcin")
        upc = response.meta.get("upc")
        details_dict = response.meta.get("specs")
        data_json = json.loads(response.text)
        price = data_json["data"]["product"]["price"]
        item = TargetItem()
        item.update({
            "url": url,
            "tcin": tcin,
            "upc": upc,
            "price": price,
            "title": title,
            "description": description,
            "specs":
                details_dict
        })
        yield item



# import requests
#
# headers = {
#     'authority': 'redsky.target.com',
#     'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
#     'accept': 'application/json',
#     'sec-ch-ua-mobile': '?0',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
#     'origin': 'https://www.target.com',
#     'sec-fetch-site': 'same-site',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-dest': 'empty',
#     'referer': 'https://www.target.com/p/toddler-girls-shanel-fisherman-sandals-cat-jack/-/A-81204099?preselect=80859208',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
# }
#
# params = (
#     ('key', 'ff457966e64d5e877fdbad070f276d18ecec4a01'),
#     ('tcin', '81204099'),
#     ('store_id', '3203'),
#     ('has_store_id', 'true'),
#     ('pricing_store_id', '3203'),
#     ('scheduled_delivery_store_id', '3203'),
#     ('has_scheduled_delivery_store_id', 'true'),
#     ('has_financing_options', 'false'),
# )
#
# response = requests.get('https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1', headers=headers, params=params)
#
# #NB. Original query string below. It seems impossible to parse and
# #reproduce query strings 100% accurately so the one below is given
# #in case the reproduced version is not "correct".
# # response = requests.get('https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=ff457966e64d5e877fdbad070f276d18ecec4a01&tcin=81204099&store_id=3203&has_store_id=true&pricing_store_id=3203&scheduled_delivery_store_id=3203&has_scheduled_delivery_store_id=true&has_financing_options=false', headers=headers)
