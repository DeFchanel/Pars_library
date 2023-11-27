import requests
import os
import argparse
from urllib.parse import urljoin
from parse_tululu_book import get_soup, parse_book_page, download_img, download_txt
import json
import time


def download_books_pages(books, page, skip_imgs, skip_txt, dest_img_folder, dest_books_folder):
    url = f'http://tululu.org/l55/{page}'
    soup = get_soup(url)
    books_ids = []
    books_selector = ".d_book"
    selected_books = soup.select(books_selector)
    for book in selected_books:
        books_ids.append(book.select_one('a')['href'][2: -1])
    for book_id in books_ids:
        payload = {
            'id': book_id
        }
        book_url = urljoin('http://tululu.org/', f'b{book_id}')
        book_page_soup = get_soup(book_url)
        parsed_page = parse_book_page(book_page_soup)
        if not skip_imgs:
            try:
                download_img(book_url, parsed_page['image'])
            except requests.HTTPError:
                print('Ошибка скачивания картинки')
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения')
                time.sleep(10)
        title = parsed_page['title']
        if not skip_txt:
            try:
                download_txt('https://tululu.org/txt.php', f'{title}', payload)
            except requests.HTTPError:
                print('Ошибка скачивания текста')
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения')
                time.sleep(10)
        books.append(
            {
                "title": title,
                "author": parsed_page['author'],
                "img_src": urljoin(f'{dest_img_folder}/', parsed_page['author'][7:]),
                "book_path": urljoin(f'{dest_books_folder}/', f'{title}.txt'),
                "comments": parsed_page['comments'],
                "genres": parsed_page['genres']
            }
        )


if __name__ == '__main__':
    books = []
    parser = argparse.ArgumentParser(description='Эта программа поможет вам спарсить книги с сайта tululu')
    parser.add_argument('--start_page', help='Страница с которой хотите начать', type=int, default=1)
    parser.add_argument('--end_page', help='Страница, на которой вы хотите закончить', type=int, default=1)
    parser.add_argument('--skip_imgs', help='Хотите ли вы пропустить скачивание картинок', action='store_true')
    parser.add_argument('--skip_txt', help='Хотите ли вы пропустить скачивание текста книг', action='store_true')
    parser.add_argument('--dest_img_folder', help='Название папки для фотографий', type=str, default='images')
    parser.add_argument('--dest_books_folder', help='Название папки для текста книг', type=str, default='books')
    parser.add_argument('--dest_books_json', help='Название файла для информации по книгам', type=str, default='books')
    args = parser.parse_args()
    images_dir_name = args.dest_img_folder
    book_dir_name = args.dest_books_folder
    os.makedirs(book_dir_name, exist_ok=True)
    os.makedirs(images_dir_name, exist_ok=True)
    for page in range(args.start_page, args.end_page + 1):
        try:
            download_books_pages(books, page, args.skip_imgs, args.skip_txt, images_dir_name, book_dir_name)
        except requests.HTTPError:
            print('Книга не найдена')
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
            time.sleep(10)
    with open(f"{args.dest_books_json}.json", "w", encoding="utf-8") as books_file:
            json.dump(books, books_file)