import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
from pprint import pprint

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
            soup = get_soup(book_url)
            download_img(soup)
            title = get_title(soup)
            download_txt(url, f'{i}.{title}', folder='books/')
            print(title)
            get_book_genre(soup)
            #download_comments(soup)
        except requests.HTTPError:
            continue

def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def get_title(soup):
    title_tag = soup.find('h1')
    title_text = title_tag.text
    title = title_text.split('::')[0].strip()
    return title


def get_book_genre(soup):
    genres = soup.find_all(class_='d_book')[1]
    genres1 = genres.find_all('a')
    print([x.text for x in genres1])
    


def download_comments(soup):
    comments = soup.find_all(class_='texts')
    for comment in comments:
        if comment:
            print(comment.find(class_='black').text)


def download_img(soup, folder='images/'):
    site_url = 'https://tululu.org/'
    img_tag = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(site_url, img_tag)
    response = requests.get(img_url)
    response.raise_for_status()
    filename = urlsplit(img_tag).path
    filename1 = filename.split('/')[-1]
    filepath = os.path.join(folder, filename1)
    with open(filepath, 'wb') as file:
        file.write(response.content)

download_books()
