import requests
import csv
# BeautifulSoup
from bs4 import BeautifulSoup


# url to scrape
url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
page = requests.get(url)

# Turn HTML to BeautifulSoup object
soup = BeautifulSoup(page.content, 'html.parser')

# Get information from website using soup
product_page_url = []
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


# Print all information, for loop that grabs link of specific book
for link in soup.find_all('a', href=True):
    url2 = link['href']
product_page_url.append('' + url)
print(product_page_url)

print(universal_product_code)
print(book_title)
print(product_description)
print(price_including_tax)
print(price_excluding_tax)
print(quantity_available)
print(category)
print(review_rating)
print(image_url2)


#phase 2 ---------------------------------------------------------------------------
print("Phase 2 --------------------------------------------------------")

url3 = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'
page2 = requests.get(url3)
Book_url = []

for link in soup.find_all('a', href=True):
    url3 = link['href']
Book_url.append('http://books.toscrape.com/catalogue' + url3)
print(Book_url)




