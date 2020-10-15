import requests
from bs4 import BeautifulSoup
import json

# https://www.tui.ru/offices/
HEADERS = {'user-agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
           'accept': '*/*'}


def get_url():
    return input('Print URL: ').strip()


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text if r.status_code == 200 else print('Status Code is not 200. Can\'t get a html-page!')


def main():
    url = get_url()
    html_page = get_html(url)
    print(html_page)


if __name__ == "__main__":
    main()

