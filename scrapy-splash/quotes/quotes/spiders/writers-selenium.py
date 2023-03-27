import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.shell import inspect_response 
from shutil import which

class WritersSpiderSelenium(scrapy.Spider):
    name = "writers_selenium"
    allowed_domains = ["quotes.toscrape.com"]

    start_urls = ["http://quotes.toscrape.com"]

    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('detach', True)
        
        chrome_path = which('chromedriver')
        

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

        driver.get('http://quotes.toscrape.com')

        quote = driver.find_element('xpath', "//li[@class='next']")
        quote.click()

        self.html = driver.page_source
        driver.close()


    def parse(self, response):
        
        resp = Selector(text=self.html)

        inspect_response(self, resp)

        yield {'test': 't'}