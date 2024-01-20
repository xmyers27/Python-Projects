import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

base_url = 'http://books.toscrape.com/catalogue/category/books/young-adult_21'
URL = f'{base_url}/page-'

books = []
Books_url = []

for page in range(1, 2):
    source = requests.get(f'{URL}{page}.html')
    if source.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {source.status_code}")
        continue

    scrape = BeautifulSoup(source.text, 'html.parser')

    for article in scrape.find_all('article'):
        # Grabbing book titles
        title_element = article.h3.a
        title = title_element.text.strip() if title_element else ''
        books.append(title)

        # Grabbing the link of each book
        link_element = article.find('a', href=True)
        url = f"{base_url}/{link_element['href']}" if link_element else ''
        Books_url.append(url)

# Outputs to CSV
scraped_data = {'TITLE': books, 'URL': Books_url}
scraped_books_df = pd.DataFrame(scraped_data)
scraped_books_df.to_csv('SCB.csv', index=None)

print(Books_url)



