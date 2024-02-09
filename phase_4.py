import os
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch page {url}. Status code: {response.status_code}")
        return None

def scrape_images(url, download_folder):
    page_content = fetch_page(url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        image_elements = soup.find_all('img', class_='thumbnail')

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for image_element in image_elements:
            image_url = url.rsplit('/', 2)[0] + '/' + image_element['src'].replace('../', '')
            image_name = image_url.split('/')[-1]
            image_path = os.path.join(download_folder, image_name)

            with open(image_path, 'wb') as f:
                f.write(requests.get(image_url).content)

            print(f"Downloaded image: {image_name}")

        # Check for additional pages and scrape images from them
        next_page_link = soup.find('li', class_='next')
        if next_page_link:
            next_page_url = url.rsplit('/', 1)[0] + '/' + next_page_link.a['href']
            scrape_images(next_page_url, download_folder)
    else:
        print("Failed to fetch page content.")

def main():
    base_url = 'https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html'
    download_folder = 'book_images'

    scrape_images(base_url, download_folder)

if __name__ == "__main__":
    main()
