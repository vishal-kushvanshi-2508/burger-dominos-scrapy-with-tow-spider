import scrapy
from burger_king_scrapy.items import BurgerKingScrapyItem

class DominosSpiderSpider(scrapy.Spider):
    name = "dominos_spider"
    allowed_domains = ["www.dominos.co.in"]
    start_urls = ["https://www.dominos.co.in/store-location/"]

    def parse(self, response):
        import re

        state_list = response.xpath("//ul[@class='citylist-ul']//li")

        print("Total cities:", len(state_list))

        for data in state_list:
            # Get city name safely
            city_name = data.xpath(".//a/text()").get()

            if not city_name:
                continue

            # Clean city name (remove "(123)")
            clean_city_name = re.sub(r"\(\d+\)", "", city_name).strip()

            # Get relative URL
            relative_url = data.xpath(".//a/@href").get()

            if not relative_url:
                continue

            # Convert to absolute URL
            city_url = response.urljoin(relative_url)

            print("now data : ", clean_city_name, city_url)

            # Send request to next page
            yield scrapy.Request(
                url=city_url,
                callback=self.parse_city,   # your next function
                meta={
                    "city_name": clean_city_name,
                    "city_url": city_url
                }
            )
            # break



    def parse_city(self, response):

        # Get meta data (passed from previous request)
        city_name = response.meta.get("city_name")
        city_url = response.meta.get("city_url")

        print(city_url, city_name)
        dominos_data = response.xpath("//section[@id='content']//div[@class = 'panel panel-default custom-panel']")
        for data in dominos_data:
            item = BurgerKingScrapyItem()

            item["city_name"] = city_name
            item["city_link"] = city_url

            item["brand_name"] = data.xpath(".//h2[@class='media-heading city-main-title fontsize0']/text()").get().strip()
            
            
            item["address"] = data.xpath(".//p[@class='grey-text mb-0']/text()").get().strip()
            
            item["region"] = data.xpath(".//p[@class='city-main-sub-title']/text()").get().strip()
            
            item["delivery_time"] = data.xpath(".//p[@class='red-text mb-0']/text()").get().strip().replace(" delivery", "")
            
            item["cost"] = data.xpath(".//span[@class='col-xs-9 col-md-9 pl0']/text()").get().strip()
            
            item["time"] = data.xpath(".//div[@class='col-xs-9 col-md-9 pl0 search-grid-right-text']/text()").get().strip()
            
            item["good_for"] = data.xpath(".//span[@class='col-xs-9 col-md-9 nowrap  pl0']//p[@class='mb-0']/text()").get().strip()
            
            item["phone_number"] = data.xpath(".//p[@class='fontsize2 bold zred']/text()").get().strip()
            yield item
