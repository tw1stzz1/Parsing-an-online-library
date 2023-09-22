import os
import requests
import argparse
from pathlib import Path
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
    book_info = {}
    raw_genre = soup.find_all(class_='d_book')[1].text
    genre = raw_genre.split(':')[1].strip()
    book_info['genre'] = (genre)

    title_text = soup.find(id='content').find('h1').text
    title = title_text.split('::')
    title = title[0].strip()
    book_info['title'] = (title)

    raw_img = soup.find(class_='bookimage').find('img')['src']
    img_url = urljoin("https://tululu.org", raw_img)
    download_image(img_url)
    book_info['img_url'] = (img_url)
    
    raw_comment = soup.find(id='content').find_all(class_="texts")
    for comment in raw_comment:
        comment = comment.find('span').text
        book_info['comments'] = (comment)
    return book_info



def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', default=1)
    parser.add_argument('--end_id', default=11)
    args = parser.parse_args()

    url = "https://tululu.org/txt.php"

    for book_id in range(int(args.start_id), int(args.end_id)):
        params = {
        "id" : book_id
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            url_for_soup = f"https://tululu.org/b{book_id}"
            answer = requests.get(url_for_soup)
            answer.raise_for_status()

            soup = BeautifulSoup(answer.text, 'lxml')
            book_info = parse_book_page(soup)
            title = book_info['title']

            download_book(book_id, response, title)
        except requests.exceptions.HTTPError:
            print("Такой книги нет!", book_id)


if __name__ == "__main__":
    main()
