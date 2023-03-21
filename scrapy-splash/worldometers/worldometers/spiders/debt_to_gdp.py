import scrapy

class DebtToGDPSpider(scrapy.Spider):
    name = 'debt_to_gdp'
    allowed_domains = ['www.tradingeconomics.com']
    start_urls = ['https://www.tradingeconomics.com/country-list/government-debt-to-gdp']

    def parse(self, response):
        
        rows = response.xpath('//table/tr')

        for row in rows:
            country_name = row.xpath(".//td[1]/a").xpath("normalize-space()").get()
            debt_to_gdp = row.xpath(".//td[2]/text()").get()

            yield {
                'country_name': country_name,
                'debt_to_gdp': debt_to_gdp
            }