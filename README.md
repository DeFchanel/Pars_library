# Парсер книг с сайта [tululu.org](tululu.org)
Это программа, которая скачивает нужные Вам книги по ID с сайта [tululu.org](tululu.org).

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить
Запустить код можно с помощью команды:
```python
python3 main.py --start_id 1 --end_id 1
```
указав нужные аргументы
### Аргументы

В программе доступны два необязательных аргументов: `--start_id` и `--end_id`
1. `--start_id` - ID книги, с которой надо скачивать.
2. `--end_id` - ID книги, по которой надо скачивать.
Если эти аргументы не указаны, то первая программа скачивает книги с 1 по 10.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).