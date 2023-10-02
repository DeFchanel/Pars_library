import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


dir_name = 'books'
os.makedirs(dir_name, exist_ok=True)

def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.HTTPError

def download_books():
    for i in range(1, 11):
        url = f"https://tululu.org/txt.php?id={i}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            book_url = f"https://tululu.org/b{i}/"
            check_for_redirect(response)
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

def get_title(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    title = title_text.split('::')[0].strip()
    return title

download_books()
