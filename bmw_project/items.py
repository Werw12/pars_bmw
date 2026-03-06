import scrapy


class CarItem(scrapy.Item):

    name = scrapy.Field()
    model = scrapy.Field()

    mileage = scrapy.Field()
    registered = scrapy.Field()
    engine = scrapy.Field()
    range = scrapy.Field()

    fuel = scrapy.Field()
    transmission = scrapy.Field()

    registration = scrapy.Field()

    exterior = scrapy.Field()
    upholstery = scrapy.Field()

   