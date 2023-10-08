import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit


dir1_name = 'books'
dir2_name = 'images'
os.makedirs(dir1_name, exist_ok=True)
os.makedirs(dir2_name, exist_ok=True)


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.HTTPError

def download_books():
    for i in range(1, 11):
        url = f"https://tululu.org/txt.php?id={i}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            book_url = f"https://tululu.org/b{i}/"
            print(download_img(book_url))
            title = get_title(book_url)
            download_txt(url, f'{i}.{title}', folder='books/')
        except requests.HTTPError:
            continue

def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def get_title(book_url):
    soup = get_soup(book_url)
    title_tag = soup.find('h1')
    title_text = title_tag.text
    title = title_text.split('::')[0].strip()
    return title


def download_img(book_url, folder='images/'):
    soup = get_soup(book_url)
    site_url = 'https://tululu.org/'
    img_tag = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(site_url, img_tag)
    response = requests.get(img_url)
    response.raise_for_status()
    filename = urlsplit(img_tag).path
    filename1 = filename.split('/')[-1]
    filepath = os.path.join(folder, filename1)
    print(filepath)
    with open(filepath, 'wb') as file:
        file.write(response.content)

download_books()
