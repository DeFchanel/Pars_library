import requests
import os
from urllib.parse import urljoin
from main import get_soup, parse_book_page, download_img, download_txt
import json


book_dir_name = 'books'
images_dir_name = 'images'
os.makedirs(book_dir_name, exist_ok=True)
os.makedirs(images_dir_name, exist_ok=True)

for book in range(1, 4):
    books_info = []
    url = f'http://tululu.org/l55/{book}'
    soup = get_soup(url)
    books_ids = []
    books = soup.find_all(class_='d_book')
    for book in books:
        books_ids.append(book.find('a')['href'][2: -1])
    for book_number, id in enumerate(books_ids):
        try:
            payload = {
                'id': id
            }
            book_url = urljoin('http://tululu.org/', f'b{id}')
            book_page_soup = get_soup(book_url)
            parsed_page = parse_book_page(book_page_soup)
            download_img(book_url, parsed_page['image'])
            title = parsed_page['title']
            download_txt('https://tululu.org/txt.php?id=11477', f'{title}', payload)
            books_info.append(
                {
                    "title": title,
                    "author": parsed_page['author'],
                    "img_src": urljoin('images/', parsed_page['author'][7:]),
                    "book_path": urljoin('books/', f'{title}.txt'),
                    "comments": parsed_page['comments'],
                    "genres": parsed_page['genres']
                }
            )
            books_info_json = json.dumps(books_info)
            with open("books.json", "w", encoding="utf-8") as my_file:
                my_file.write(books_info_json)

        except requests.HTTPError:
            print('Книга не найдена')