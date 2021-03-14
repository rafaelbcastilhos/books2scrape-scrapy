import scrapy
from books2scrape.items import BookItem


class BookSpider(scrapy.Spider):
    name = "book_spider"
    allowed_domains = ["books.toscrape.com"]

    product_info_mapping = {
        "UPC": "upc",
        "Product Type": "product_type",
        "Price (excl. tax)": "price_exclude_tax",
        "Price (incl. tax)": "price_include_tax",
        "Tax": "tax",
        "Availability": "availability",
        "Number of reviews": "number_of_reviews",

    }

    def start_requests(self):
        urls = ["http://books.toscrape.com"]
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.logger.info(f"Scrape Page {response.url}")
        book_links = response \
            .xpath("//article[@class='product_pod']//h3//a/@href").getall()
        next_page = response.xpath("//li[@class='next']//@href").get()

        yield from response.follow_all(book_links, self.parse_book)

        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        item = BookItem()

        item["title"] = response.css(".product_main h1::text").get().strip()
        item["price"] = response \
            .css(".product_main p.price_color::text").get().strip()
        item["rating"] = response \
            .css(".product_main p.star-rating::attr(class)").get() \
            .split(" ")[1].strip()
        item["description"] = response \
            .css("#product_description + p::text").get()

        for row in response.css("table.table-striped tr"):
            key = self.product_info_mapping[row.css("th::text").get().strip()]
            value = row.css("td::text").get().strip()
            item[key] = value

        item["image_href"] = response \
            .css("#product_gallery img::attr(src)").get()
        item["image_urls"] = [response.urljoin(item["image_href"])]

        self.logger.info(f"Book: {item['title']} scraped")
        yield item
