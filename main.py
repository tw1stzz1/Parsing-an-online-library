import os
import requests
import argparse
from pathlib import Path

import time
from urllib.parse import urljoin
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_book(book_id, response, title):
    book_filename = sanitize_filename(f"{book_id}.{title}.txt")
    book_filepath = os.path.join("books", book_filename)

    with open(book_filepath, 'wb') as file:
        file.write(response.content)
    return book_filepath


def download_image(img_url):
    img_filename = urlsplit(img_url)[2]
    img_filename = img_filename.split('/')[-1]
    img_filepath = os.path.join("images", img_filename)

    response = requests.get(img_url)
    response.raise_for_status() 

    with open(img_filepath, 'wb') as file:
        file.write(response.content)
    return img_filepath


def parse_book_page(soup):
    book_parameters = {}
    raw_genre = soup.find_all(class_='d_book')[1].text
    genre = raw_genre.split(':')[1].strip()

    title_text = soup.find(id='content').find('h1').text
    title = title_text.split('::')
    title = title[0].strip()

    raw_img = soup.find(class_='bookimage').find('img')['src']
    img_url = urljoin("https://tululu.org/shots/", raw_img)
    
    book_parameters = {
        'genre' : genre,
        'title' : title,
        'img_url' : img_url,
    }

    raw_comment = soup.find(id='content').find_all(class_="texts")
    for comment in raw_comment:
        comment = comment.find('span').text
        book_parameters['comments'] = comment
    return book_parameters


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description='This code allows you to download books and their covers form tululu')
    parser.add_argument('--start_id', default=1, help='Id of the book from which the download will begin')
    parser.add_argument('--end_id', default=11, help='Id of the book where the download will end')
    args = parser.parse_args()

    book_txt_url = "https://tululu.org/txt.php"

    for book_id in range(int(args.start_id), int(args.end_id)):
        params = {
            "id": book_id
        }
        try:
            response = requests.get(book_txt_url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            book_url = f"https://tululu.org/b{book_id}"
            answer = requests.get(book_url)
            answer.raise_for_status()
            check_for_redirect(answer)

            soup = BeautifulSoup(answer.text, 'lxml')
            book_parameters = parse_book_page(soup)
            title = book_parameters['title']
            img_url = book_parameters['img_url']
            download_image(img_url)

            download_book(book_id, response, title)
        except requests.exceptions.ConnectionError:
            print("Разрыв соединения с сайтом")
            time.sleep(20)
        except requests.exceptions.HTTPError:
            print("Такой книги нет!", book_id)



if __name__ == "__main__":
    main()
