# Парсер книг с сайта [tululu.org](tululu.org)
Это программа, которая скачивает нужные Вам книги по ID или книги с нужных вам страниц с сайта [tululu.org](tululu.org)

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить
Запустить код для скачивания книг по ID можно с помощью команды:
```python
python3 main.py --start_id 1 --end_id 1
```
указав нужные аргументы

Запустить код для скачивания книг по страницам можно с помощью команды:
```python
python3 parse_tululu_category.py --start_page 1 --end_page 1 --skip_imgs True --skip_txt True --dest_img_folder images --dest_books_folder books --dest_books_json books
```
### Аргументы

В 1 программе доступны два необязательных аргументов: `--start_id` и `--end_id`
1. `--start_id` - ID книги, с которой надо скачивать.
2. `--end_id` - ID книги, по которою надо скачивать.
Если эти аргументы не указаны, то первая программа скачивает книги с 1 по 10.

Во 2 программе доступны семь необязательных аргументов: --start_page, --end_page, --skip_imgs, --skip txt, --dest_img_folder,--dest_books_folder и --dest_books_json
1.'--start_page' - Номер страницы, с которой надо скачивать книги
2.'--end_page' - Номер страницы, по которую надо скачивать книги
3.'--skip_imgs' - Надо ли пропускать скачивание картинок
4.'--skip txt' - Надо ли пропускать скачивание текста
5.'--dest_img_folder' - Название папки для картинок
6.'--dest_books_folder' - Название папки для текстов
7.'--dest_books_json' - Название файла с информацией по книгам

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).