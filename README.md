# Asynchronous web scraping with `asyncio` and `aiohttp`

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