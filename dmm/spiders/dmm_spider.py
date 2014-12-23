__author__ = 'liguoxiang'

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import Rule,CrawlSpider
from scrapy.contrib.linkextractors import sgml
from dmm.items import DmmItem
from scrapy.selector import HtmlXPathSelector
import re
from scrapy import log
import logging

class DmmSpider(CrawlSpider):
	name="dmm"
	allowed_domains=["www.dmm.co.jp"]
	#start_urls=["http://www.dmm.co.jp/mono/dvd/-/detail/=/cid=iptd932/",
	#            "http://www.dmm.co.jp/mono/dvd/-/detail/=/cid=iptd974/",
	#           "http://www.dmm.co.jp/mono/dvd/-/detail/=/cid=venu457/"]
	start_urls=["http://www.dmm.co.jp/mono/dvd/-/list/=/list_type=dmp/"]
	rules = [Rule(sgml.SgmlLinkExtractor(allow=(r'/mono/dvd/-/detail/=/cid=.*/')), callback='parse_video'),
             Rule(sgml.SgmlLinkExtractor(allow=(r'/mono/dvd/-/list/=/list_type=dmp/page=\d*/')), follow=True)]
	log.start(loglevel=log.INFO,logstdout=False)
	dic={1:'sale_date',2:'video_time',3:'video_actor',5:'video_series',
	     6:'video_company',7:'video_level',8:'video_genre',9:'video_code'}

	def parse_video(self,response):
		log.msg(response.url,level=log.INFO)
		#tds1=response.xpath('//td[@width="100%"]').extract().re('\>(\d{4}\/\d{2}\/\d{2}|\w*)\<\/')
		tds=response.xpath('//td[@width="100%"]').extract()
		title=response.xpath('//h1[@id="title"]/text()').extract()
		performer=response.xpath('//span[@id="performer"]/a/@href').extract()
		thumb=response.xpath('//img[@class="tdmm"]/@src').extract()
		pic=response.xpath('//a[@name="package-image"]/@href').extract()

		item=DmmItem()

		performerId=re.search(r'id=\d*',performer[0]).group(0)
		performerId=performerId[3:]


		for i in range(1,len(tds)):
			m=re.search(r'\>{1}(.*)\<\/',tds[i])
			txt=m.group(0)
			length=len(txt)
			txt=txt[1:length-2]
			#print(str(i)+"========"+txt)
			try:
				item[self.dic[i]]=txt
			except Exception as ex:
				pass
		if performerId:
			item['video_actor']={performerId.encode('utf-8'):item['video_actor']}
		item['video_title']=title[0]
		item['thumb_url']=thumb[0].encode('utf-8')
		item['pic_url']=pic[0].encode('utf-8')

		yield item
		#print(item)


			#txt.sub('[(^\>)|(\<\/$')

		#	print(str(i)+"======="+txt)
