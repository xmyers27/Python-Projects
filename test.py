import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

URL = 'https://books.toscrape.com/catalogue/page-'

books = []
Price = []
Stock_availability = []
Books_url = []
upc = []
book_description = []

for page in range(1, 2):
    Source = requests.get(URL + str(page) + '.html')
    if Source.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {Source.status_code}")
        continue

    Scrape = BeautifulSoup(Source.text, 'html.parser')

    for article in Scrape.find_all('article'):
        # Grabbing book titles
        title_element = article.h3.a
        title = title_element.text.strip() if title_element else ''
        books.append(title)

        # Grabbing book price
        price_container = article.find('div', class_='product_price')
        price = price_container.p.text.strip() if price_container else ''
        Price.append(price)

        # Grabbing stock availability of each book
        stock_element = Scrape.find('p', class_='instock availability')
        stock_availability = stock_element.text.strip() if stock_element else ''
        Stock_availability.append(stock_availability)

        # Grabbing the link of each book
        link_element = article.find('a', href=True)
        url = 'https://books.toscrape.com/catalogue/' + link_element['href'] if link_element else ''
        Books_url.append(url)

        # Extracting additional information from each individual book's page
        book_response = requests.get(url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        # Extracting UPC number
        upc_element = book_soup.find('th', string='UPC').find_next('td')
        upc.append(upc_element.text.strip() if upc_element else '')

        # Extracting book description
        description_element = book_soup.find('meta', {'name': 'description'})
        book_description.append(description_element['content'].strip() if description_element else '')

# Outputs to CSV
Scraped_Data = {'TITLE': books, 'PRICE': Price, 'STOCK AVAILABILITY': Stock_availability, 'URL': Books_url, 'UPC': upc, 'DESCRIPTION': book_description}
Scraped_Books = pd.DataFrame(Scraped_Data)
Scraped_Books.to_csv('SCB.csv', index=None)

print(Books_url)

