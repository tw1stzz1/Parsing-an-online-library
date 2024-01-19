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
    parser.add_argument('--start_page', default=1, help='Page from which the download will begin')
    parser.add_argument('--end_page', default=4, help='Page where the download will end')
    parser.add_argument('--skip_imgs', action='store_false', help='This setting skips image download')
    parser.add_argument('--skip_txt', action='store_false', help='This setting skips txt file download')
    parser.add_argument('--dest_folder', default="result", help='This setting skips txt file download')
    args = parser.parse_args()

    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)

    book_txt_url = "https://tululu.org/txt.php"
    dest_folder = args.dest_folder
    for numbers in range(int(args.start_page), int(args.end_page)):
        url = f"https://tululu.org/l55/{numbers}/"
        try:
            response = requests.get(url)
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            books_json_parameters = []
            books = soup.find_all(class_='d_book')
            try:
                for book_id in books:
                    book_id = book_id.find('a')['href']
                    book_url = urljoin(url, book_id)
                    book_id = book_id[2:-1]

                    answer = requests.get(book_url)
                    answer.raise_for_status()
                    check_for_redirect(answer)
                    
                    book_parameters = parse_book_page(answer, book_url)
                    title = book_parameters['title']
                    img_url = book_parameters['img_url']
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

                        book_path = download_book(book_id, response, title, dest_folder)
                    else:
                        book_path = None
                    
                    book_json_parameters = {
                    'title': title,
                    'author' : book_parameters['author'],
                    'img_src' : img_path,
                    'book_path' : book_path,
                    'genres' : book_parameters['genres'],
                    'comments' : book_parameters['comments']
                    }
                    
                    books_json_parameters.append(book_json_parameters)
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

    books_json_parameters = json.dumps(books_json_parameters, ensure_ascii=False)

    with open(f"{args.dest_folder}/books_json_parameters.json", "w", encoding='utf8') as my_file:
        my_file.write(books_json_parameters)

if __name__ == "__main__":
    main()
