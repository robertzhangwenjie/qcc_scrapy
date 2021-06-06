import sys

import scrapy

from jobbole.items import JobboleArticleItem

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['blog.jobbole.com','www.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/caijing/cjpl/']
    start_urls = ['http://www.jobbole.com']

    count = 0
    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url,callback=self.parse_topic)

    def parse_topic(self,response):
        '''
        提取网站的每个主题页url
        :param response:
        :return:
        '''
        yield from response.follow_all(response.css('div.sub-nav a::attr(href)').getall())

    def parse(self, response,**kwargs):

        # 获取当前页的所有文章的image标签，它包含img_url和article_url
        # 然后调用self.parse_article对response进行文章的信息提取，提取完成后返回
        article_item_list = response.css('div.list-item')

        for article_item in article_item_list:
            article_url = article_item.css('div.content a::attr(href)').get()
            article_image_url = article_item.css('div.img a img::attr(src)').get()
            yield response.follow(article_url,callback=self.parse_article,meta={"img":article_image_url})

        # 获取下一页的url，然后交给scrapy下载，并调用self.parse对当前url进行处理
        next_url = response.css('div#page > div a.a1:last-child::attr(href)')
        if next_url:
            yield from response.follow_all(next_url,self.parse)

    def parse_article(self, response):
        '''
        对爬取的页面进行解析
        :param response:爬取页面的html
        :return:
        '''

        article_item = JobboleArticleItem()

        # url
        article_url = response.url

        # 文章标题
        title_xpath = '//div[@class="article-head"]/h1[@class="title"]/text()'
        title = response.xpath(title_xpath).get()

        # 创建时间
        create_date_xpath = '//div[@class="article-head"]/div[@class="about"]/div[@class="date"]/span[1]/text()'
        create_date = response.xpath(create_date_xpath).get()

        # 正文内容
        content_xpath='//div[@class="article-main"]'
        content=response.xpath(content_xpath).get()

        # 文章标签
        tag_xpath='//div[@class="word"]/a/@title'
        tags = response.xpath(tag_xpath).getall()

        # 文章img
        img_url = response.meta.get("img","")

        article_item["title"] = title
        article_item["create_date"] = create_date
        article_item["tags"] = tags
        article_item["img_url"] = [img_url]
        article_item["content"] = content
        article_item["url"] = article_url
        self.log(f'article_item:{article_item}')
        yield article_item

