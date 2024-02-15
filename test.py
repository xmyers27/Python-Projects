import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://books.toscrape.com/catalogue/page-'
current_page = 1
books = []
prices = []
stock_availability = []
books_url = []
upc = []
book_description = []

# Function to get total number of pages
def get_total_pages():
    response = requests.get(base_url + '1.html')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pager = soup.find('ul', class_='pager')
        if pager:
            last_page = int(pager.find_all('li')[-2].text.strip())
            return last_page
    return 1  # If total pages not found, return 1

total_pages = get_total_pages()

# Loop through all pages
while current_page <= total_pages:
    url = f'{base_url}{current_page}.html'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    for article in soup.find_all('article'):
        # Grabbing book titles
        title_element = article.h3.a
        title = title_element.text.strip() if title_element else ''
        books.append(title)

        # Grabbing book price
        price_container = article.find('div', class_='product_price')
        price = price_container.p.text.strip() if price_container else ''
        prices.append(price)

        # Grabbing stock availability of each book
        stock_element = article.find('p', class_='instock availability')
        stock_availability.append(stock_element.text.strip() if stock_element else '')

        # Grabbing the link of each book
        link_element = article.find('a', href=True)
        url = 'https://books.toscrape.com/catalogue/' + link_element['href'] if link_element else ''
        books_url.append(url)

        # Extracting additional information from each individual book's page
        book_response = requests.get(url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        # Extracting UPC number
        upc_element = book_soup.find('th', string='UPC').find_next('td')
        upc.append(upc_element.text.strip() if upc_element else '')

        # Extracting book description
        description_element = book_soup.find('meta', {'name': 'description'})
        book_description.append(description_element['content'].strip() if description_element else '')

    current_page += 1

# Outputs to CSV
scraped_data = {
    'TITLE': books,
    'PRICE': prices,
    'STOCK AVAILABILITY': stock_availability,
    'URL': books_url,
    'UPC': upc,
    'DESCRIPTION': book_description
}
scraped_books = pd.DataFrame(scraped_data)
scraped_books.to_csv('scraped_books.csv', index=None)

print("Data scraping and CSV creation completed successfully!")
