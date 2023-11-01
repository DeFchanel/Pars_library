import requests
import os
import argparse
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
import time


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.HTTPError
    

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_genres(soup):
    genres = soup.find_all(class_='d_book')[1]
    book_genres = genres.find_all('a')
    return [x.text for x in book_genres]


def get_title_and_author(soup):
    title_tag = soup.find('h1')
    title_text = title_tag.text
    title = title_text.split('::')[0].strip()
    author = title_text.split('::')[1].strip()
    return title, author


def get_comments(soup):
    comments = soup.find_all(class_='texts')
    return [comment.find(class_='black').text for comment in comments]


def download_txt(url, filename,  payload, folder='books/'):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    sanitized_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitized_filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_img(book_url, img_tag, folder='images/'):
    img_url = urljoin(book_url, img_tag)
    response = requests.get(img_url)
    response.raise_for_status()
    filename_path = urlsplit(img_tag).path
    filename = filename_path.split('/')[-1]
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_book_page(soup):
    title, author = get_title_and_author(soup)
    genres = get_book_genres(soup)
    comments = get_comments(soup)
    image = soup.find('div', class_='bookimage').find('img')['src']
    return {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'image': image
    }


def download_books(start_book_id, end_book_id):
        for book_id in range(start_book_id, end_book_id + 1):
            payload = {
                'id': book_id
            }
            url = f"https://tululu.org/txt.php"
            try:
                response = requests.get(url, params=payload)
                response.raise_for_status()
                check_for_redirect(response)
                book_url = f"https://tululu.org/b{book_id}/"
                soup = get_soup(book_url)
                parsed_page = parse_book_page(soup)
                download_img(book_url, parsed_page['image'])
                title = parsed_page['title']
                download_txt(url, f'{book_id}.{title}', payload, folder='books/')
                print('Название:', parsed_page['title'])
                print('Автор:', parsed_page['author'])
            except requests.HTTPError:
                print('Книга не найдена')
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения')
                time.sleep(10)


if __name__ == '__main__':
    book_dir_name = 'books'
    images_dir_name = 'images'
    os.makedirs(book_dir_name, exist_ok=True)
    os.makedirs(images_dir_name, exist_ok=True)
    parser = argparse.ArgumentParser(description='Эта программа поможет вам спарсить книги с сайта tululu')
    parser.add_argument('--start_id', help='ID книги, с которой хотите начать', type=int, default=1)
    parser.add_argument('--end_id', help='ID книги, с которой хотите начать', type=int, default=11)
    args = parser.parse_args()
    download_books(args.start_id, args.end_id)