from scrapy import Spider, Request
from scrapy.selector import Selector
from ulta.items import UltaItem
import re
import numpy as np

class UltaSpider(Spider):
	name = 'ulta_spider'
	allowed_urls = ['https://www.ulta.com/']
	start_urls = ['https://www.ulta.com/skin-care-suncare?N=27fe']
	# Other category skin care products to replace above:
		# Cleanser - 'https://www.ulta.com/skin-care-cleansers?N=2794'
		# Eye - 'https://www.ulta.com/skin-care-eye-treatments?N=270k'
		# Moisturizer - 'https://www.ulta.com/skin-care-moisturizers?N=2796'
		# Serum - 'https://www.ulta.com/skin-care-treatment-serums?N=27cs'
		# Sunscreen - 'https://www.ulta.com/skin-care-suncare?N=27fe'


	def parse(self,response):
		# Retrieve number of pages and result urls for each subsequent page
		num_pages = int(re.findall('\d+', response.xpath('//span[@class = "upper-limit"]/text()').extract_first())[0])
		result_urls = [f'https://www.ulta.com/skin-care-suncare?N=27fe&No={i*96}&Nrpp=96' for i in range(num_pages)]
		# Other category skin care products to replace above:
			# Cleanser - https://www.ulta.com/skin-care-cleansers?N=2794&No=
			# Eye - https://www.ulta.com/skin-care-eye-treatments?N=270k&No=
			# Moisturizer - https://www.ulta.com/skin-care-moisturizers?N=2796&No=
			# Serum - https://www.ulta.com/skin-care-treatment-serums?N=27cs&No=
			# Sunscreen - https://www.ulta.com/skin-care-suncare?N=27fe&No=

		for url in result_urls:
			yield Request(url = url, callback = self.parse_results_page)

	def parse_results_page(self, response):
		# Use product container to retrieve product urls, reviews, and ratings

		product_container = response.xpath('//div[@class="productQvContainer"]')
		for u in product_container:
			product_urls = response.urljoin(u.xpath('.//a/@href').extract()[0])
			try:
				reviews = int(re.findall('\d+', u.xpath('.//span[@class="prodCellReview"]//text()').extract()[1])[0])
				rating = u.xpath('./a//label[@class="sr-only"]/text()').extract_first()
			except:
				reviews = ""
				rating = ""

			yield Request(url = product_urls, callback=self.parse_product_page, meta ={'reviews': reviews, 'rating': rating})


	def parse_product_page(self, response):
		# Brand Name
		try:
			brand = response.xpath('.//a[@class="Anchor Anchor__withDivider"]//text()').extract()[0]
		except:
			brand = np.nan
		# Product Type
		try:	
			product = response.xpath('.//span[@class="Text Text--subtitle-1 Text--left Text--small Text--text-20"]//text()').extract()[0]
		except:
			product = np.nan
		# Price
		try:
			price = response.xpath('.//span[@class="Text Text--title-6 Text--left Text--bold Text--small Text--neutral-80"]//text()').extract()[-1]
		except:
			price = np.nan
		# Details of product
		try:
			details = response.xpath('.//div[@class="ProductDetail__productContent"]//text()').extract()
		except:
			details = np.nan
		# Categories
		try:
			categories = response.xpath('.//a[@class="Anchor Tertiary"]//text()').extract()
		except:
			categories = np.nan
		# Size
		try:
			size = response.xpath('.//p[@class="Text Text--body-2 Text--left Text--small"]//text()').extract()[0]
		except:
			size = np.nan

		item = UltaItem()

		item['brand'] = brand
		item['product'] = product
		item['price'] = price
		item['details'] = details
		item['categories'] = categories
		item['size'] = size
		item['reviews'] = response.meta['reviews']
		item['rating'] = response.meta['rating']

		yield item

