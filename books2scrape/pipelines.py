# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os, re
from books2scrape.items import BookItem
from scrapy.exporters import JsonLinesItemExporter
from scrapy.utils.python import to_bytes


class JsonExporter(JsonLinesItemExporter):
    def start_exporting(self):
        self.file.write(b"[\n")

    def finish_exporting(self):
        self.file.seek(-2, os.SEEK_END)
        self.file.truncate()
        self.file.write(b"\n]")

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        data = "\t" + self.encoder.encode(itemdict) + ',\n'
        self.file.write(to_bytes(data, self.encoding))


class Books2ScrapePipeline:
    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def open_spider(self, spider):
        self.file = open('books.json', 'wb')
        self.exporter = JsonExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            item["price"] = item["price"][1:]
            item["tax"] = item["price"][1:]
            item["price_exclude_tax"] = item["price_exclude_tax"][1:]
            item["price_include_tax"] = item["price_include_tax"][1:]
            item["rating"] = self.rating_mapping[item["rating"]]
            match = re.findall(r"(?<=\().+(?=\))", item["availability"])[0]
            item["availability"] = match.split(" ")[0] if match else 0

            self.exporter.export_item(item)
            return item
        else:
            raise Exception("invalid class")

