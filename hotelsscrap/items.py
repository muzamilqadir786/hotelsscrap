# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HotelsscrapItem(Item):
    # define the fields for your item here like:
    # name = Field()
    Url = Field()
    Title = Field()
    Address = Field()
    HotelRatings = Field()
    CheckIn = Field()
    CheckOut = Field()
    Currency = Field()
    Floors = Field()
    Rooms = Field()
    YearOpened = Field()
    YearRenovated = Field()
    TimeZone = Field()
    Time = Field()
    
    pass
