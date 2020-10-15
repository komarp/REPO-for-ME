import requests
from bs4 import BeautifulSoup
import json

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
           'accept': '*/*'}


def get_url():
    return input("Enter URL: ").strip()


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text if r.status_code == 200 else print('Status Code is not 200. Can\'t get a html-page!')


def get_content(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')
    data = []
    cities = soup.find_all('div', class_='city-item')
    for city in cities:
        shops = city.find_all('div', class_='shop-list-item')
        for shop in shops:
            city_name = city.find('h4', class_='js-city-name').get_text()
            address = f"{city_name}, {shop.find('div', class_='shop-address').get_text()}"
            latlon = [float(shop.attrs['data-shop-latitude']),
                    float(shop.attrs['data-shop-longitude'])]
            if not shop.attrs['data-shop-phone']:
                phones = None
            else:
                phones = [shop.attrs['data-shop-phone']]
            data.append({'address': address,
                        'latlon': latlon,
                        'name': shop.attrs['data-shop-name'],
                         'phones': phones,
                         'working_hours': [f'{shop.attrs["data-shop-mode1"]} {shop.attrs["data-shop-mode2"]}']})
    return data


def get_file():
    file_name, prefix = input('Print a file name, you want to write down information: '), '.json'
    return file_name + prefix


def json_writer(data, file_to):
    with open(file_to, 'w') as file_to:
        json.dump(data, file_to, indent=4, ensure_ascii=False)


def main():
    url = get_url()
    html_page = get_html(url)
    get_content(html_page)
    data = get_content(html_page)
    file_to = get_file()
    json_writer(data, file_to)


if __name__ == '__main__':
    main()
