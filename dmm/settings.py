# -*- coding: utf-8 -*-

# Scrapy settings for dmm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dmm'

SPIDER_MODULES = ['dmm.spiders']
NEWSPIDER_MODULE = 'dmm.spiders'
ITEM_PIPELINES={
	'dmm.pipelines.DmmPipeline':300,
}
LOG_FILE='log/dmm.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dmm (+http://www.yourdomain.com)'
