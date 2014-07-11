from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from hotelsscrap.items import HotelsscrapItem
from scrapy.http import Request

class HotelspiderSpider(CrawlSpider):
    name = 'hotelspider'
    allowed_domains = ['www.hotels-rates.com']
    start_urls = ['http://www.hotels-rates.com/site_map/USA/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse', follow=True),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        states_links = hxs.select('//div[@id="fourcolumn"]//ul/li/a/@href').extract()
        print states_links
        print len(states_links)
        
        for link in states_links:            
            request = Request(link,callback=self.parse_state_city,dont_filter=True)
            request.meta['link'] = link
            yield request
    
    def parse_state_city(self,response):
        hxs = HtmlXPathSelector(response)
        cities_links = hxs.select('//div[@id="twocolumn"]//ul/li/a/@href').extract()
        print response.meta['link']
        print cities_links
        print len(cities_links)
        
        for link in cities_links:            
            request = Request(link,callback=self.parse_city_hotels,dont_filter=True)
            request.meta['link'] = link
            yield request
            
    def parse_city_hotels(self,response):
        hxs = HtmlXPathSelector(response)
        hotels_links = hxs.select('//div[@id="hotellist"]//dd/p[1]/a/@href').extract()
        print response.meta['link']
        print hotels_links
        print len(hotels_links)
        
        for link in hotels_links:            
            request = Request(link,callback=self.parse_hotel_info,dont_filter=True)
            request.meta['link'] = link
            yield request
            
    def parse_hotel_info(self,response):
        hxs = HtmlXPathSelector(response)
        #html = hxs.select('//div[@id="hotellist"]//dd/p[1]/a/@href').extract()
        item = HotelsscrapItem()
        item['Url'] = response.meta['link']
        print item['Url']
        
        title = hxs.select('//div[@id="hotelinfo"]/h1/text()').extract()
        print title
        item['Title'] = title
        
        address_part1 = hxs.select('normalize-space(//div[@id="hotelinfo"]/h2//text()[1])').extract()
        address_part2 = hxs.select('normalize-space(//div[@id="hotelinfo"]/h2//text()[2])').extract()
        address = '\n'.join(address_part1+address_part2)
        item['Address'] = address
        
        from datetime import datetime
        item['Time'] = str(datetime.now())[:-7]
        print str(item['Time'])[:-7]
        
        hotel_ratings = hxs.select('//p[contains(text(),"Hotel Rating(s)")]/text()').extract()
        if hotel_ratings:
            item['HotelRatings'] = hotel_ratings[0].split(":")[1]
                
        check_in = hxs.select('//p[contains(text(),"Check In:")]/text()').extract()
        if check_in:
            item['CheckIn'] = check_in[0].replace('Check In:','')
        
        
        check_out = hxs.select('//p[contains(text(),"Check Out:")]/text()').extract()
        if check_out:
            item['CheckOut'] = check_out[0].replace('Check Out:','')
            #print item['']
            
        currency = hxs.select('//p[contains(text(),"Currency:")]/text()').extract()
        if currency:
            item['Currency'] = currency[0].split(":")[1]
            
        floors = hxs.select('//p[contains(text(),"Floors:")]/text()').extract()
        if floors:
            item['Floors'] = floors[0].split(":")[1]
                    
        rooms = hxs.select('//p[contains(text(),"Rooms:")]/text()').extract()
        if rooms:
            item['Rooms'] = rooms[0].split(":")[1]
            
        year_opened = hxs.select('//p[contains(text(),"Year Opened:")]/text()').extract()
        if year_opened:
            item['YearOpened'] = year_opened[0].split(":")[1]
            
        year_renovated = hxs.select('//p[contains(text(),"Year Renovated:")]/text()').extract()
        if year_renovated:
            item['YearRenovated'] = year_renovated[0].split(":")[1]
        
        time_zone = hxs.select('//p[contains(text(),"Time Zone:")]/text()').extract()
        if time_zone:
            item['TimeZone'] = time_zone[0].split(":")[1]
            
        yield item
        
        
        