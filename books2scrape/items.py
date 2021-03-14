# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class BookItem(Item):
    title = Field()
    price = Field()
    rating = Field()
    upc = Field()
    product_type = Field()
    price_exclude_tax = Field()
    price_include_tax = Field()
    tax = Field()
    availability = Field()
    number_of_reviews = Field()
    description = Field()
    image_href = Field()
    image_urls = Field()
    images = Field()
