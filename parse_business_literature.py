import requests
import argparse
import time

from tools import download_book, download_image, parse_book_page, check_for_redirect


def main():
    parser = argparse.ArgumentParser(description='This code allows you to download books and their covers form tululu')
    parser.add_argument('--start_id', default=1, help='Id of the book from which the download will begin')
    parser.add_argument('--end_id', default=11, help='Id of the book where the download will end')
    parser.add_argument('--dest_folder', default="result", help='This setting skips txt file download')
    args = parser.parse_args()

    book_txt_url = "https://tululu.org/txt.php"
    dest_folder = args.dest_folder
    for book_id in range(int(args.start_id), int(args.end_id)):
        params = {
            "id": book_id
        }
        try:
            response = requests.get(book_txt_url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            book_url = f"https://tululu.org/b{book_id}/"

            answer = requests.get(book_url)
            answer.raise_for_status()
            check_for_redirect(answer)

            book_parameters = parse_book_page(answer, book_url)
            title = book_parameters['title']
            img_url = book_parameters['img_url']
            download_image(img_url, dest_folder)

            download_book(book_id, response, title, dest_folder)
        except requests.exceptions.ConnectionError:
            print("Разрыв соединения c сайтом")
            time.sleep(20)
        except requests.exceptions.HTTPError:
            print("Такой книги нет!", book_id)



if __name__ == "__main__":
    main()
