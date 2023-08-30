import os
import requests
from pathlib import Path


def download_book_txt(book_id):

    url = "https://tululu.org/txt.php?"
    params = {
        "id" : book_id
    }

    book_filename = f"id{book_id}.txt"
    book_filepath = os.path.join("books", book_filename)

    response = requests.get(url, params, verify=False)
    response.raise_for_status() 

    with open(book_filepath, 'wb') as file:
        file.write(response.content)
    return response.content



def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    

    for book_id in range(1,11):
        download_book_txt(book_id)

    
if __name__ == "__main__":
    main()
