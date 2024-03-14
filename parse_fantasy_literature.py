import requests
from urllib.parse import urljoin
import time
import json
import argparse
from pathlib import Path

from bs4 import BeautifulSoup
from tools import download_book, download_image, parse_book_page, check_for_redirect


def main():
    parser = argparse.ArgumentParser(description='This code allows you to download books and their covers form tululu')
    parser.add_argument('--start_page', default=1, help='Page from which the download will begin', type=int)
    parser.add_argument('--end_page', default=4, help='Page where the download will end', type=int)
    parser.add_argument('--skip_imgs', action='store_true', help='This setting skips image download')
    parser.add_argument('--skip_txt', action='store_true', help='This setting skips txt file download')
    parser.add_argument('--dest_folder', default="result", help='This setting skips txt file download')
    args = parser.parse_args()

    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)

    book_txt_url = "https://tululu.org/txt.php"
    dest_folder = args.dest_folder
    books_archive = []
    for number in range(int(args.start_page), int(args.end_page)):
        page_url = f"https://tululu.org/l55/{number}/"
        try:
            response = requests.get(page_url)
            check_for_redirect(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            books = soup.find_all(class_='d_book')
            for book in books:
                book_link = book.find('a')['href']
                book_url = urljoin(page_url, book_link)
                book_id = book_link[2:-1]
                try:
                    answer = requests.get(book_url)
                    check_for_redirect(answer)
                    answer.raise_for_status()

                    parsed_book = parse_book_page(answer, book_url)
                    title = parsed_book['title']
                    img_url = parsed_book['img_url']
                    if not args.skip_imgs:
                        img_path = download_image(img_url, dest_folder)
                    else:
                        img_path = None

                    if not args.skip_txt:
                        params = {
                            "id": book_id
                        }
                        response = requests.get(book_txt_url, params=params)
                        check_for_redirect(response)
                        response.raise_for_status()

                        book_path = download_book(book_id, response, title, dest_folder)
                    else:
                        book_path = None

                    books_archive.append(
                        {
                            'title': title,
                            'author': parsed_book['author'],
                            'img_src': img_path,
                            'book_path': book_path,
                            'genres': parsed_book['genres'],
                            'comments': parsed_book['comments']
                        }
                    )
                except requests.exceptions.ConnectionError:
                    print("Разрыв соединения c сайтом")
                    time.sleep(20)
                except requests.exceptions.HTTPError:
                    print("Такой книги нет!", book_id)
        except requests.exceptions.HTTPError:
            print("Такой страницы нет!")
        except requests.exceptions.HTTPError:
            print("Разрыв соединения c сайтом")
            time.sleep(20)

    with open(f"{args.dest_folder}/books_parameters.json", "w", encoding='utf8') as file:
        json.dump(books_archive, file, ensure_ascii=False)


if __name__ == "__main__":
    main()
