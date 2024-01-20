import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def extract_book_info(soup):
    product_page_url = [url]

    universal_product_code = soup.find('body').find('article', {'class': 'product_page'}).select('tr')[0].get_text(strip=True).replace(', ', ' ')
    book_title = soup.find('body').find('h1').get_text(strip=True).replace(',', ' ')
    price_including_tax = soup.find('body').find('article', {'class': 'product_page'}).select('tr')[3].get_text(strip=True).replace(', ', ' ')
    price_excluding_tax = soup.find('body').find('article', {'class': 'product_page'}).select('tr')[2].get_text(strip=True).replace(', ', ' ')
    quantity_available = soup.find('body').find('article', {'class': 'product_page'}).select('p.instock.availability')[0].get_text(strip=True).replace(', ', ' ')
    product_description = soup.find('body').find('article', {'class': 'product_page'}).select('p')[3].get_text(strip=True).replace(',', ' ')
    category = soup.find('body').find('ul', {'class': 'breadcrumb'}).select('a')[2].get_text(strip=True).replace(',', ' ')
    review_rating = soup.find('body').find('article', {'class': 'product_page'}).select('p.star-rating.Four')[0].get_text(strip=True).replace(',', ' ')
    image_url = soup.select('div img')
    image_url2 = image_url[0]['src']

    return {
        'product_page_url': product_page_url,
        'universal_product_code': universal_product_code,
        'book_title': book_title,
        'product_description': product_description,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'quantity_available': quantity_available,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url2
    }


def print_book_info(book_info):
    for key, value in book_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    # url to scrape
    url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"

    # Get information from website using functions
    soup = get_soup(url)
    book_info = extract_book_info(soup)

    # Print all information
    print_book_info(book_info)







