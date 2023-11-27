import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

URL = 'https://books.toscrape.com/catalogue/page-'

books = []
Price = []
Stock_availability = []
Books_url = []
# For loop to crawl and get information from multiple pages.
for page in range(1, 6):
    Source = requests.get(URL + str(page) + '.html')
    Scrape = BeautifulSoup(Source.text, 'html.parser')
    # print(Scrape.prettify())

    # Grabbing book titles
    for article in Scrape.find_all('article'):
        books.append(article.h3.a.text)
        # print(books)
        # Grabbing book price
        Price.append(article.find('div', class_='product_price').p.text)
        # print(Price)
        # Grabbing stock availability of each book
        Stock = Scrape.find('p', class_='instock availability').text.strip()
        Stock_availability.append(Stock)
        # print(Stock_availability)

        # Grabbing the link of each book
        for link in article.find_all('a', href=True):
            url = link['href']
        Books_url.append('https://books.toscrape.com/catalogue/' + url)
        # print(Books_url)

Scraped_Data = {'TITLE': books, 'PRICE': Price, 'STOCK AVAILABILTY': Stock_availability, 'URL': Books_url}
Scraped_Books = pd.DataFrame(Scraped_Data)
Scraped_Books[:5]
Scraped_Books.to_csv('SCB.csv', index=None)