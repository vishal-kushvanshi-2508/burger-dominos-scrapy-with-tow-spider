import scrapy
from burger_king_scrapy.items import BurgerKingScrapyItem

class BurgerSpiderSpider(scrapy.Spider):
    print("---- first PAGE () ----")
    name = "burger_spider"
    allowed_domains = ["stores.burgerking.in"]
    start_urls = ["https://stores.burgerking.in/location/gujarat"]

    def parse(self, response):

        base_url = "https://stores.burgerking.in/location/"

        brand_name = response.xpath("//div[@class='search-section']//h1/text()").get()
        state_list = response.xpath("//ul[@class='list-unstyled search-location']//select[@name='state']//option[@value!='']/text()")
    
        ## get all state name and website link .
        for state in state_list:
            if not state:
                continue
            state_name = state.get()

            lower_state_name = state_name.lower().replace(" ", "-")
            
            website_link = f"{base_url}{lower_state_name}#searchAdvance"

            print(state_name, website_link)
            yield scrapy.Request(
                url=website_link,
                callback=self.parse_state_page,
                meta={
                    "brand_name" : brand_name,
                    "state_name": state_name,
                    "lower_state_name" : lower_state_name,
                    "base_url": base_url
                }
            )


   #  Step 3: SECOND FUNCTION (City Extraction)
    def parse_state_page(self, response):
        # print("---- SECOND PAGE (CITY) ----")

        #  Get data from meta
        brand_name = response.meta["brand_name"]
        state_name = response.meta["state_name"]
        lower_state_name = response.meta["lower_state_name"]
        base_url = response.meta["base_url"]

        # 👉 Update XPath based on actual HTML
        cities = response.xpath("//ul[@class='list-unstyled search-location']//select[@name='city']//option[@value!='']")

        for city in cities:
            city_value = city.xpath("./@value").get()
            city_name = city.xpath("./text()").get()
            print(city_value, city_name)

            
            city_link = f"{base_url}{lower_state_name}/{city_value}#searchAdvance"

            yield scrapy.Request(
                url=city_link,
                callback=self.menu_page,
                meta={
                    "brand_name" : brand_name,
                    "state_name": state_name,
                    "city_name": city_name,
                    "city_link": city_link,
                }
            )

    def menu_page(self, response):
        # print("---- third  PAGE (CITY) ----")

        #  Get data from meta
        brand_name = response.meta["brand_name"]
        state_name = response.meta["state_name"]
        city_name = response.meta["city_name"]
        city_link = response.meta["city_link"]

        product_data = response.xpath("//ul[contains(@class,'outlet-detail')]")
        for data in product_data:
            item = BurgerKingScrapyItem()

            item["brand_name"] = brand_name
            item["state_name"] = state_name
            item["city_name"] = city_name
            item["city_link"] = city_link

            # Address
            address_list = data.xpath(
                ".//li[@class='outlet-address']//div[@class='info-text']//span/text()"
            ).getall()
            item["address"] = " ".join(address_list[:2]).strip()

            # Pincode
            item["pincode"] = data.xpath(
                ".//li[@class='outlet-address']//span[contains(@class,'merge-in-next')]//span[last()]/text()"
            ).get()

            # Phone
            item["phone_number"] = data.xpath(
                ".//li[@class='outlet-phone']//a/text()"
            ).get()

            # Time
            item["time"] = data.xpath(
                ".//li[contains(@class,'outlet-timings')]//span/text()"
            ).get()

            # Website
            item["website"] = data.xpath(
                ".//li[@class='outlet-actions']//a[contains(@class,'btn-website')]/@href"
            ).get()

            # Map
            item["map"] = data.xpath(
                ".//li[@class='outlet-actions']//a[contains(@class,'btn-map')]/@href"
            ).get()

            yield item















