# -*- coding: utf-8 -*-

# Scrapy settings for WeiboCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WeiboCrawler'

SPIDER_MODULES = ['WeiboCrawler.spiders']
NEWSPIDER_MODULE = 'WeiboCrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 15
# # Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 100
# # The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'cookie': 'SINAGLOBAL=7134353383474.731.1685979699250; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFj5giNTm6P6ejHTiz0_R_75JpX5KMhUgL.FozNS0.cS0efS022dJLoIEXLxK-LBK-LBoqLxKnL12eLBoqLxK-LB.qL1KnLxK-L122LBK5LxK-L1hqLBo5t; XSRF-TOKEN=9V79dT8GgRR6DdIYAo7ZpUsG; ALF=1690103218; SSOLoginState=1687511220; SCF=AkAZNc_xNE5W6if9143ABxM9ZRLeiYJ7MYErdQLuBh9WLOyaq_kba0_dHxEwCLrrVc7WJ4xndgCpfvejpKX6HrQ.; SUB=_2A25JkRDkDeRhGeRJ7FsX9y3JzD2IHXVq5wUsrDV8PUNbmtAGLUH4kW9NUlcukQIbmyo0kOmmbvHE0ZXeNHWInrzP; _s_tentry=weibo.com; Apache=5807030246516.398.1687511886226; ULV=1687511886272:5:5:1:5807030246516.398.1687511886226:1686549249365; WBPSESS=Oh3-UXsySWUndH4lSeqCIZzvIeiToe-zQKP2RDcEi4t2SzAdEHLU3lDDqf1TAfxseXtRgnUC76f4nnVw4a60QaT5eiWaBSGVxPBxSIAZdQ5d7r___QfQsLKchU-v0JEUk0JHhOJRNXOlJCskf0G8cA==; PC_TOKEN=330fa4510a'
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'WeiboCrawler.middlewares.IPProxyMiddleware': 100,
    'WeiboCrawler.middlewares.TooManyRequestsRetryMiddleware': 543,
}
RETRY_HTTP_CODES = [429, 418, 502]

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'WeiboCrawler.pipelines.WeibocrawlerPipeline': 300,
    # 'WeiboCrawler.pipelines.MongoPipeline': 400,
}
# MONGO_URI = 'localhost'
# MONGO_DB = 'weibo'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# # 图片存储目录
# IMAGES_STORE = 'images/'
# ITEM_PIPELINES = {
#    'WeiboCrawler.pipelines.ImagesnamePipeline': 300,
# }