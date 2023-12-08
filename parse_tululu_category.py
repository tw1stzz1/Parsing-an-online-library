import requests
from urllib.parse import urljoin
import time

from bs4 import BeautifulSoup
from main import download_book, download_image, parse_book_page, check_for_redirect

for nunbers in range(1, 5):
    url = f"https://tululu.org/l55/{nunbers}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
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
            download_image(img_url)

            book_txt_url = "https://tululu.org/txt.php"
            params = {
                "id": book_id
            }
            response = requests.get(book_txt_url, params=params)
            check_for_redirect(response)
            download_book(book_id, response, title)
    except requests.exceptions.ConnectionError:
        print("Разрыв соединения c сайтом")
        time.sleep(20)
    except requests.exceptions.HTTPError:
        print("Такой книги нет!", book_id)
