# Парсер книг с сайта tululu.org
Данный код позволяет скачивать книги жанра: детектив или фантастика, а еще их обложки [tululu](https://tululu.org)

### Как установить
Python3 должен быть уже установлен. Используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Аргументы
#### dest_folder
При запуске любого из файлов можно указать, куда будут скачиваться файлы. Для этого существует аргумент `--dest_folder`.
По умолчанию код создает папку `result` в той же папке что и файл скачивания. С помщью `--dest_folder` вы можете поменять название этой папки или указать существующее
```
python parse_fantasy_literature.py --dest_folder ваше_название_папки
```
#### start_page и end_page
При запуске `parse_fantasy_literature.py` можно указать аргумент `--start_page` и/или `--end_page`
`--start_page` - то с какой страницы начнется скачивание, по умолчанию равен 1.
`--end_page` - то на какой страницы закончится скачивание, по умолчанию равен 4.
```
python parse_fantasy_literature.py --start_page 3 --end_page 5
```
#### skip_imgs и skip_txt
При запуске `parse_fantasy_literature.py` можно указать аргумент `--skip_imgs` и/или `--skip_txt`, эти аргументы приниимают только значения `True` или `False`
`--skip_imgs` - при значение `True`, пропускает скачивание обложек
`--skip_txt` - при значение `True`, пропускает скачивание текста книг
Код ниже пропустит установку и текста, и обложек.
```
python parse_fantasy_literature.py --skip_imgs True --skip_txt True
```
#### start_id и end_id
При запуске `parse_business_literature.py` можно указать аргумент `--start_id` и/или `--end_id`
`--start_id` - то с какой книги начнется скачивание, по умолчанию равен 1.
`--end_id` - то на какой книги закончится скачивание, по умолчанию равен 11.
```
python parse_business_literature.py --start_id 12 --end_id 30
```
### Пример запуска кода
Для скачивания детективов и их обложек используйте эту команду:
```
python parse_business_literature.py
``` 
Для скачивания фантастики нужно лишь заменить `parse_business_literature.py` на `parse_fantasy_literature.py`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

