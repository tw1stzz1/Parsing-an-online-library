import os
import requests
from pathlib import Path

from urllib.parse import urljoin
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_book(book_id, response, title, dest_folder):
    full_path = f'{dest_folder}/books'

    Path(full_path).mkdir(parents=True, exist_ok=True)

    book_filename = sanitize_filename(f"{book_id}.{title}.txt")
    book_filepath = os.path.join(full_path, book_filename)

    with open(book_filepath, 'wb') as file:
       file.write(response.content)
    return book_filepath


def download_image(img_url, dest_folder):
    full_path = f'{dest_folder}/images'

    Path(full_path).mkdir(parents=True, exist_ok=True)

    img_filename = urlsplit(img_url)[2]
    img_filename = img_filename.split('/')[-1]
    img_filepath = os.path.join(full_path, img_filename)

    response = requests.get(img_url)
    response.raise_for_status()

    with open(img_filepath, 'wb') as file:
        file.write(response.content)
    return img_filepath


def parse_book_page(answer, book_url):
    soup = BeautifulSoup(answer.text, 'lxml')
    comments = []
    raw_genres = soup.select(".d_book")[1].text
    genre = raw_genres.split(':')[1].strip()
    genre = genre[:-1].split(',')

    title_text = soup.select_one("#content h1").text
    title = title_text.split('::')
    title = title[0].strip()

    author = soup.select_one("#content h1 a").text

    raw_img = soup.select_one(".bookimage img")["src"]
    img_url = urljoin(book_url, raw_img)

    raw_comments = soup.select("#content .texts")
    for comment in raw_comments:
        comment = comment.select_one("span").text
        comments.append(comment)
    book_parameters = {
        'title': title,
        'author': author,
        'img_url': img_url,
        'genres': genre,
        'comments': comments
    }
    return book_parameters


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError
