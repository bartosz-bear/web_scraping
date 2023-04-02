# Collection of web scraping scripts, spiders and crawlers

Collection consists of two parts:

1. Scrapy spiders and crawlers built with `scrapy` and `splash`
2. Asynchronous web scraping script using `BeautifulSoup` in combination with `asyncio` and `aiohttp`

# Scrapy spiders and crawlers

There are 7 scrapy spiders and crawlers organized in 4 scrapy projects, all living in `scrapy-splash` folder.

1. `best_movies` crawler, scraping from live `www.imdb.com`. Crawler visits 'Top 250 best movies of all times' ranking which is split into 5 pages, 50 movies each. Then it proceeds to visit each movie's URL to scrap detailed data about each movie.

2. `books` crawler, scraping from scraping `http://quotes.toscrape.com/`. 1000 books. Deals with pagination. 10 pages with 100 books each.

3. `writers` spider, scraping also from `http://quotes.toscrape.com/`. 83 quotes from 10 different pages. Deals with pagination and JavaScript, dynamically generated content using `splash`.

4. `special_offers` spider scraping 500 products from archived version, of currently defunct electronics, e-commerce store `www.tinydeal.com`.

5. `fancy_glasses` spider scraping 250 products from live eyeware e-commerce store `https://www.glassesshop.com/`

6. `countries` spider scraping 4200 population datapoints for countries around the world between 1995 and 2020 from live economic page `https://www.worldometers.info`

7. `debt_to_gdp` spider scraping current Debt-to-GDP ratio for 173 countries, also from `https://www.worldometers.info`

# Asynchronous web scraping script using `BeautifulSoup` with `asyncio` and `aiohttp`

This is version 2.0 of a web scraping script which takes course category as input, scrapes all available courses from Coursera.org for the chosen category and saves them as an Excel file on your local drive. If you don't want to download the file and see the output in the console instead, comment out line 170 `df.to_excel('courses_final.xlsx', index=False, engine='xlsxwriter')`.

Version 2.0 is 8 times faster on average than version 1.0. Performance improvement was achieved by replacing synchronous http requests with asychronous http requests.

## Example Output

![](/images/excel-output.png)

# How to run this script locally?

## Create an isolated virtual environment


`conda create -n scraper python=3.11`

`conda activate scraper`

`conda install -c conda-forge requests aiohttp beautifulsoup4 pandas lxml xlsxwriter`

## Open `async_coursera_scraper.py` in your favorite file editor


Uncomment last line `#scrap('math-and-logic')`

You can leave `math-and-logic` as an argument or you can replace it with one from the following categories:
`['data-science', 'business', 'personal-development', 'language-learning', 'math-and-logic', 'physical-science-and-engineering]`

## Run the script


`python async_coursera_scraper.py`

Voilla! After about 15 seconds you should see an Excel file with the scraping results on your hard drive.