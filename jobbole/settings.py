# Scrapy settings for jobbole project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_NAME = 'jobbole'

SPIDER_MODULES = ['jobbole.spiders']
NEWSPIDER_MODULE = 'jobbole.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'jobbole (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'jobbole.middlewares.JobboleSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'jobbole.middlewares.RandomUserAgentMiddleware': 543,
    # 'jobbole.middlewares.RandomProxyMiddleware': 544,
    'jobbole.middlewares.RandomCookieMiddleware': 545,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

}

# useragent type, the value can be one of the following, default random
# random,ie,chrome,firefox,safari,opera
UA_TYPE = 'random'

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'jobbole.pipelines.JoboleImagesPipeline': 301,
    'jobbole.pipelines.MysqlPipeline': 302,
    'jobbole.pipelines.QccCsvPipeline': 303,
}
IMAGES_URLS_FIELD = 'img_urls'
IMAGES_RESULT_FIELD = 'img_urls'
IMAGES_STORE = os.path.join(PROJECT_DIR, 'images')

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False
# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# mysql config
MYSQL_HOST = "www.robertzwj.com"
MYSQL_USER = "robert"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "scrapy"

# webdriver
Webdriver_Path = os.path.join(os.path.dirname(PROJECT_DIR), 'webdrivers')
ChromeDriver = os.path.join(Webdriver_Path, 'chromedriver.exe')

# qcc excel
COMPANY_EXCEL_PATH_DIR = os.path.join(PROJECT_DIR, 'qcc', 'excel')
COMPANY_RESULT_PATH_DIR = os.path.join(PROJECT_DIR, 'qcc', 'result')

# qcc账号
QCC_ACCOUNTS = [
    {
        'phone': '13995553697',
        'password': 'zhangwenjie64656'
    },
    {
        'phone': '17771786590',
        'password': 'zhangwenjie64656'
    },

]
