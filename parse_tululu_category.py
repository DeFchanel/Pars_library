import requests
import os
import argparse
from urllib.parse import urljoin
from main import get_soup, parse_book_page, download_img, download_txt
import json


def download_books_pages(start_page, end_page, skip_imgs, skip_txt, dest_img_folder, dest_books_folder, dest_books_json):
    for book in range(start_page, end_page + 1):
        books_info = []
        url = f'http://tululu.org/l55/{book}'
        soup = get_soup(url)
        books_ids = []
        books_selector = ".d_book"
        books = soup.select(books_selector)
        for book in books:
            books_ids.append(book.select_one('a')['href'][2: -1])
        for id in books_ids:
            try:
                payload = {
                    'id': id
                }
                book_url = urljoin('http://tululu.org/', f'b{id}')
                book_page_soup = get_soup(book_url)
                parsed_page = parse_book_page(book_page_soup)
                if not skip_imgs:
                    download_img(book_url, parsed_page['image'])
                title = parsed_page['title']
                if not skip_txt:
                    download_txt('https://tululu.org/txt.php?id=11477', f'{title}', payload)
                books_info.append(
                    {
                        "title": title,
                        "author": parsed_page['author'],
                        "img_src": urljoin(f'{dest_img_folder}/', parsed_page['author'][7:]),
                        "book_path": urljoin(f'{dest_books_folder}/', f'{title}.txt'),
                        "comments": parsed_page['comments'],
                        "genres": parsed_page['genres']
                    }
                )
                books_info_json = json.dumps(books_info)
                with open(f"{dest_books_json}.json", "w", encoding="utf-8") as books_file:
                    books_file.write(books_info_json)
            except requests.HTTPError:
                print('Книга не найдена')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Эта программа поможет вам спарсить книги с сайта tululu')
    parser.add_argument('--start_page', help='Страница с которой хотите начать', type=int, default=1)
    parser.add_argument('--end_page', help='Страница, на которой вы хотите закончить', type=int, default=1)
    parser.add_argument('--skip_imgs', help='Хотите ли вы пропустить скачивание картинок', type=bool, default=False)
    parser.add_argument('--skip_txt', help='Хотите ли вы пропустить скачивание текста книг', type=bool, default=False)
    parser.add_argument('--dest_img_folder', help='Название папки для фотографий', type=str, default='images')
    parser.add_argument('--dest_books_folder', help='Название папки для текста книг', type=str, default='books')
    parser.add_argument('--dest_books_json', help='Название файла для информации по книгам', type=str, default='books')
    args = parser.parse_args()
    images_dir_name = args.dest_img_folder
    book_dir_name = args.dest_books_folder
    os.makedirs(book_dir_name, exist_ok=True)
    os.makedirs(images_dir_name, exist_ok=True)
    download_books_pages(args.start_page, args.end_page, args.skip_imgs, args.skip_txt, images_dir_name, book_dir_name, args.dest_books_json)