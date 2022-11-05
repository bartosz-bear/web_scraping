import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import pandas as pd

########## FIRST TRY ##########



#get_instructors()

def scrap(category):

    category

    # MAIN PAGE

    url = f"https://www.coursera.org/browse/data-science"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')

    ### MAYBE THESE TWO ARE UNCESSARY ###

    # COURSE, SPECIALIZATIONS, ETC CONTAINER NR 1
    card_title_link = soup.find('a', {'class':'card-title-link'}).find_all('div')[0].get_text()
    card_title_links = soup.find_all('a', {'class':'card-title-link'})

    print('card_title_link: ',len(card_title_links))
    print('card_title_link', card_title_link)

    # DESKTOP COLLECTIONS

    desktop_collection = soup.find('div', {'class':'rc-desktopCollection'})
    desktop_collections = soup.find_all('div', {'class':'rc-desktopCollection'})

    ### SPECIFIC ITEMS IN CONTAINERS

    #card_text_link = card_title_link.find('a', {'class':'CardText-link'})

    # RC-PRODUCTCARD

    rc_ProductCard = soup.find('div', {'class':'rc-ProductCard'})
    rc_ProductCards = soup.find_all('div', {'class':'rc-ProductCard'})

    print(rc_ProductCard)
    print('rc_ProductsCars', len(rc_ProductCards))


    # CARDTEXT LINK-COURSE_NAME

    course_name = rc_ProductCard.find('a', {'class': 'CardText-link'}).get_text()
    course_type = rc_ProductCard.find('label', {'class': 'rc-CardText css-1feobmm'}).get_text()
    course_link = rc_ProductCard.find('a', {'class':'CardText-link'})['href']

    # ALL COURSES IN ALL PRODUCT CARDS


    all_courses = []
    for i, j in enumerate(rc_ProductCards):
        all_items = {'index': 0,
                     'course_name': '',
                     'course_type': '',
                     'course_link': ''}
        all_items['index'] = i

        all_items['course_name'] = j.find('a', {'class': 'CardText-link'}).get_text()
        #print('##### ', j.find('a', {'class': 'CardText-link'}).get_text())
        all_items['course_type'] = j.find('label', {'class': 'rc-CardText css-1feobmm'}).get_text()
        #print('##### ', j.find('label', {'class': 'rc-CardText css-1feobmm'}).get_text())
        all_items['course_link'] = j.find('a', {'class':'CardText-link'})['href']
        #print('##### ', j.find('a', {'class':'CardText-link'})['href'])
        all_courses.append(all_items)
        #print(len(items_list))

    print('all items: ', all_courses[0])

    # COURSE PAGE

    root = "https://www.coursera.org/"
    #webpage = f'{root}{course_link}'
    webpage2 = 'https://www.coursera.org/learn/foundations-data'
    r2 = requests.get(webpage2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
    course_soup = BeautifulSoup(r2.content, 'lxml', from_encoding='utf-8')

    # ITERATING OVER ALL SUBPAGES


    # FILTER 'COURSES' ONLY


    only_courses = []
    for c in all_courses:
        if c['course_type'] == 'Course':
            only_courses.append(c)

    # Removing duplicates
    only_courses = [dict(t) for t in {tuple(d.items()) for d in only_courses}]
    #only_courses = list(set(only_courses))

    df = pd.DataFrame(only_courses)
    #df = df[df['course_type'] == 'Course']
    #print(df.head())
    df.to_csv('courses.csv')

    def get_instructor(course_path):

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        browser = webdriver.Chrome(options=options)

        browser.get(f'https://www.coursera.org{course_path}')

        time.sleep(1)  # instructor-name headline-3-text bold

        # Instructor

        titles_element = browser.find_element_by_xpath("//h3[@class='instructor-name headline-3-text bold']").text
        print('text instructor: ', titles_element)
        stripped_instr = titles_element.replace('\nTOP INSTRUCTOR', '')
        print('stripped_instructor', stripped_instr)

        print('instructor: ', stripped_instr, '\n')

        return stripped_instr

    def get_description(course_soup2):
        descriptions = course_soup2.find_all('div', {'class': 'content-inner'})
        desc = descriptions[0].find_all('p')

        my_list = []
        for i in desc:
            my_list.append(i.get_text())

        full_desc = ''.join(my_list)
        return full_desc

    def get_enrolled(course_soup2):
        product_metrics = course_soup2.find('div', {'class': 'rc-ProductMetrics'}).find('strong').find('span').get_text()
        enrolled = int(product_metrics.replace(',', ''))
        return enrolled

    def get_ratings(course_soup2):
        ratings_count = course_soup2.find('span', {'data-test': 'ratings-count-without-asterisks'}).find('span').get_text()
        ratings_count = int(ratings_count.strip(' ratings').replace(',', ''))
        return ratings_count

    final_list = []
    for single_course in only_courses[:2]:
        root = "https://www.coursera.org/"
        webpage3 = f"{root}{single_course['course_link']}"
        r3 = requests.get(webpage3, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
        course_soup2 = BeautifulSoup(r3.content, 'lxml', from_encoding='utf-8')
        print(single_course['course_link'])
        try:
            single_course['instructor'] = get_instructor(single_course['course_link'])
            single_course['description'] = get_description(course_soup2)
            single_course['students_enrolled'] = get_enrolled(course_soup2)
            single_course['ratings'] = get_ratings(course_soup2)
        except:
            single_course['description'] = "The course hasn't started yet."
            single_course['students_enrolled'] = "0"
            single_course['ratings'] = "0"
        print('single course: ', single_course)
        final_list.append(single_course)

    df = pd.DataFrame(final_list)#.drop('index')
    #df = df[df['course_type'] == 'Course']
    #print(df.head())
    df.to_csv('courses_final.csv')

    print("final_list ", len(final_list), final_list[0])

    return final_list

#scrap('data-science')

def get_dropdown_choices():

    url = "https://www.coursera.org/browse"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')

    ### MAYBE THESE TWO ARE UNCESSARY ###

    # COURSE, SPECIALIZATIONS, ETC CONTAINER NR 1
    category = soup.find('div', {'class': 'topic-column'}).find('a')['to'][8:]
    print('cat1 ', category)
    categories = soup.find_all('div', {'class': 'topic-column'})
    print(len(categories))

    categories_list = ['data-science']
    for c in categories:
        categories_list.append(c.find('a')['to'][8:])

    categories_dict = {}
    for c in categories_list:
        categories_dict[c.replace('-', ' ').capitalize()] = c

    #print('CATEGORIES ', categories_dict)

    return categories_dict



### END OF SCRIPT ###

"""

# BANNER INSTRUCTOR INFO

#h3 = course_soup.find(class_='instructor-name headline-3-text bold')
banner_instructor_info = course_soup.find('h3', {'class': 'instructor-name headline-3-text bold'})
#instructor_info = banner_instructor_info.find('span')

#data = requests.get(webpage).json()


#print('course name', course_name)
#print('course type', course_type)
#print('course link', course_link)
#print('instructor: ', course_soup.prettify())

# DESCRIPTION

descriptions = course_soup.find_all('div', {'class': 'content-inner'})
desc = descriptions[0].find_all('p')

#print('desk', len(desc))

my_list = []
for i in desc:
    my_list.append(i.get_text())


full_desc = ''.join(my_list)
#print(full_desc)

# STUDENTS ENROLLED

product_metrics = course_soup.find('div', {'class':'rc-ProductMetrics'}).find('strong').find('span').get_text()

enrolled = int(product_metrics.replace(',', ''))

#import unicodedata as ud

#print('unicode', ud.lookup(','))
#print('unicode', ud.name(','))

#print('product metrics', type(enrolled), enrolled)

# RATINGS

ratings_count = course_soup.find('span', {'data-test':'ratings-count-without-asterisks'}).find('span').get_text()
ratings_count = int(ratings_count.strip(' ratings').replace(',', ''))

#print('ratings', ratings_count)

### FROM PYTHON TO PANDAS TO CSV

import pandas as pd

df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
                   'mask': ['red', 'purple'],
                   'weapon': ['sai', 'bo staff']})

df.to_csv('my_csv.csv', index=False)

csv_template = {'Course Name': [],
                'Course Provider': [],
                'Course Description': [],
                '# of Students Enrolled': [],
                '# of Ratings': []}



################## SELENIUM ######################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

browser = webdriver.Chrome(options=options)


browser.get('https://www.coursera.org/learn/foundations-data')

time.sleep(3) #instructor-name headline-3-text bold

# Instructor

titles_element = browser.find_element_by_xpath("//h3[@class='instructor-name headline-3-text bold']").text
stripped_instr = titles_element.strip('\nTOP INSTRUCTOR')

print('instructor: ', stripped_instr, '\n')



# Description

description = browser.find_elements_by_xpath("//div[@class='content-inner']/p")

#print(dir(webdriver.remote.webelement.WebElement))
#print('element: ',description[1].text)
#print('element: ',description[1].tag_name)
#print('element: ',description[1].value_of_css_property())
#print(description[7].prettify())


for i in description:
    if i.text == "":
        print('aria-hidden', i.get_attribute("aria-hidden"))
    else:
        print('description: ', i.text)


browser.quit()

"""


#print(driver.page_source)



# RC-COLLECTION

#rc_collection = soup.find('section', {'class':'rc-Collection'})
#rc_collections = soup.find_all('section', {'class':'rc-Collection'})

#print(rc_collection.prettify())

#print(rc_collection.prettify())

#for i in card_title_link:
#    print(i)

#print(desktop_collection.prettify())
#print(len(desktop_collections), len(rc_collections))

#print(soup_data.find('meta'))
#print(soup_data.prettify())
#cds-33 css-bku0rr cds-35
#cds-33 css-bku0rr cds-35

########## SECOND TRY ##########
"""
url = "https://www.coursera.org/search?query=data%20science&index=prod_all_launched_products_term_optimization_skills_test_for_precise_xdp_imprecise_variant&entityTypeDescription=Courses"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')

h2_all = soup.find('h2', {'class':"cds-33 css-bku0rr cds-35"})
print(h2_all)

#for i in h2_all:
#    print(i)
"""

















#cds-33 css-14d8ngk cds-35
#cds-33 css-14d8ngk cds-35

#_1g3eaodg
#_1g3eaodg