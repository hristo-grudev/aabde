import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import AabdeItem
from itemloaders.processors import TakeFirst


class AabdeSpider(scrapy.Spider):
	name = 'aabde'
	start_urls = ['https://www.aab.de/aabweb/partner/service/pressemitteilungen/pressemitteilung01022021']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class, "col-md-12")]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//article[@class="text-block"]/h2/text()').get()
		description = response.xpath('//section[@class="einspaltig"]//text()[normalize-space() and not(ancestor::h2)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-12 active"]/a/text()').get()
		try:
			date = re.findall(r'\d{2}\.\d{2}\.\d{4}', date)[0]
		except:
			date = ''


		item = ItemLoader(item=AabdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
