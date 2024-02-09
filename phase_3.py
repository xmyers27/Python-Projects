import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def fetch_page(url, page):
    page_url = f'{url}{page}.html'
    source = requests.get(page_url)
    if source.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {source.status_code}")
        return None
    return source.text

def scrape_books(scrape, base_url):
    books = []
    Books_url = []

    for article in scrape.find_all('article'):
        # Grabbing book titles
        title_element = article.h3.a
        title = title_element.text.strip() if title_element else ''
        books.append(title)

        # Grabbing the link of each book
        link_element = article.find('a', href=True)
        url = f"{base_url}/{link_element['href']}" if link_element else ''
        Books_url.append(url)

    return books, Books_url

def write_to_csv(data, filename):
    scraped_books_df = pd.DataFrame(data)
    scraped_books_df.to_csv(filename, index=None)

def determine_number_of_pages(base_url):
    page = 1
    num_pages = 0

    while True:
        source_text = fetch_page(base_url, page)
        if source_text is None:
            break

        scrape = BeautifulSoup(source_text, 'html.parser')
        num_pages += 1

        next_page_link = scrape.find('li', class_='next')
        if next_page_link:
            page += 1
        else:
            break

    return num_pages

def main():
    base_url = 'http://books.toscrape.com/catalogue/category/books/young-adult_21'
    URL = f'{base_url}/page-'

    num_pages = determine_number_of_pages(URL)

    all_books = []
    all_books_url = []

    for page in range(1, num_pages + 1):
        source_text = fetch_page(URL, page)
        if source_text is not None:
            scrape = BeautifulSoup(source_text, 'html.parser')
            books, books_url = scrape_books(scrape, base_url)

            all_books.extend(books)
            all_books_url.extend(books_url)

    # Outputs to CSV
    scraped_data = {'TITLE': all_books, 'URL': all_books_url}
    write_to_csv(scraped_data, 'SCB.csv')

    print(all_books_url)

if __name__ == "__main__":
    main()





