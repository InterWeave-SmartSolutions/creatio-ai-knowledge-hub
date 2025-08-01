# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    """Item for storing page data"""
    url = scrapy.Field()
    title = scrapy.Field()
    content_type = scrapy.Field()
    status_code = scrapy.Field()
    text_content = scrapy.Field()
    html_content = scrapy.Field()
    links = scrapy.Field()
    media_links = scrapy.Field()
    resources = scrapy.Field()
    crawl_timestamp = scrapy.Field()
    depth = scrapy.Field()
    parent_url = scrapy.Field()


class ResourceItem(scrapy.Item):
    """Item for storing resource data (videos, PDFs, images, etc.)"""
    url = scrapy.Field()
    resource_type = scrapy.Field()
    content_type = scrapy.Field()
    file_size = scrapy.Field()
    status_code = scrapy.Field()
    parent_page = scrapy.Field()
    crawl_timestamp = scrapy.Field()
