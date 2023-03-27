from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

from shutil import which

chrome_path = which('chromedriver')

options = Options()
#options.add_argument('--headless')
options.add_experimental_option('detach', True)

service = Service(chrome_path)

browser = webdriver.Chrome(service=service, options=options)

browser.get('https://duckduckgo.com')

#search_btn = browser.find_element_by_id('search_form_input_homepage')
#search_btn.send_keys('My User Agent')

#search_input = browser.find_element_by_xpath("(//input[contains(@class, 'js-search-input')])[1]")
#search_input = browser.find_element('xpath', "(//input[contains(@class, 'js-search-input')])[1]")
search_input = browser.find_element('xpath', "//input[@id='search_form_input_homepage']")
search_input.send_keys('My User Agent')

#search_btn = browser.find_element('xpath', "//input[@id='search_button_homepage']")
#search_btn.click()

search_input.send_keys(Keys.ENTER)

page_source = search_input.page_source

browser.close()

'''
browser.find_elements_by_class_name()
browser.find_elements_by_tag_name('h1')
browser.find_element_by_xpath('')
browser.find_element_by_css_selector('')
'''
