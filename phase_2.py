import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


def extract_links():
    category_urls = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if 'category' in url:  # Adjust this condition based on the specific pattern indicating a category link
            category_urls.append('http://books.toscrape.com/' + url)

    for category in category_urls:
        print(category)


extract_links()



