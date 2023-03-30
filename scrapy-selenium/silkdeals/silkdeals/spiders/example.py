import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.shell import inspect_response
from scrapy.shell import open_in_browser

from selenium_stealth import stealth

import pdb


class ExampleSpider(scrapy.Spider):
    name = "example"
    script = 'document.querySelector("#searchbox_input").value = "ChatGPT"; '

    def start_requests(self):
        
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=5,
            #screenshot=True,
            callback=self.parse,
            # script='''document.querySelector("#searchbox_input").value = "ChatGPT"
            #           document.querySelector('button[aria-label="Search"]').click()'''
            script='''document.querySelector("#searchbox_input").value = "ChatGPT";'''
        )

    

    def parse(self, response):
        #img = response.meta['screenshot']

        #with open('screenshot.png', 'wb') as f:
        #  f.write(img)

        open_in_browser(response)

        pdb.set_trace()

        #inspect_response(self, response)

        #driver = response.meta['driver']
        #search_input = driver.find_element('xpath', "//input[@id='search_form_input_homepage']")
        #search_input.send_keys('Hello World')

        #driver.save_screenshot('after_filling_input.png')
        yield {
            'a':'a'
        }