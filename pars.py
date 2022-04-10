import pandas as pd
import requests
from bs4 import BeautifulSoup
from local_settings import headers

from Db import engine
from sqlalchemy.orm import sessionmaker


session = sessionmaker(bind=engine)
s = session()


def get_html(url, params=None):
    response = requests.get(url, headers=headers, params=params)
    html = response.text
    return html


def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        good_count = soup.find(
            'span', class_='goods-count').get_text(strip=True).replace('\xa0', '').split()[0]
        print(good_count)
        pages = int(good_count) // 100 + 1
    except:
        pages = 1
    return pages


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="product-card")
    cards = []
    for item in items:
        discount = item.find('span', class_='product-card__sale active')
        if discount:
            discount = discount.get_text(strip=True)
        else:
            discount = ''
        cards.append({
            'brand': item.find('strong', class_='brand-name').get_text(strip=True).replace('/', ''),
            'product_name': item.find('span', class_='goods-name').get_text().split('/')[0],
            'price': int(item.find(class_='lower-price').get_text(strip=True).replace('\xa0', '').replace('₽', '')),
            'discount': discount,
            'link': f'https://www.wildberries.ru{item.find("a", class_="product-card__main").get("href")}',
        })
    return cards


def parse(url):
    global search
    search = url
    print(f'Парсим данные с: "{search}"')
    html = get_html(url)
    pages = get_pages(html)
    print(f'Количество страниц: {pages}')
    cards = []
    pages = int(input('Введите количество страниц: '))
    for page in range(1, pages + 1):
        print(f'Парсинг страницы: {page}')
        html = get_html(url, params={'sort': 'popular', 'page': page})
        cards.extend(get_content(html))
    print(f'Всего: {len(cards)} позиций')
    save_data(cards)


def save_data(data: list):
    datfr = pd.DataFrame(data)
    datfr.to_sql('Product', engine, if_exists='replace', index=False)


if __name__ == "__main__":
    parse('https://www.wildberries.ru/brands/m65-casual')
