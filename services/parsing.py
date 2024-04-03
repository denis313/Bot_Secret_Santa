# парсиинг магазинов для списков подарко
import json
import logging

from bot import logger
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
import requests

dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


def get_categories(query):
    logging.debug(f'Categories: {query}')
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search?' \
          '&curr=rub' \
          '&lang=ru' \
          '&locale=ru' \
          f'&query={query}' \
          '&resultset=catalog' \
          '&sort=popular' \
          '&page=1'

    url2 = f'https://search.wb.ru/exactmatch/ru/common/v5/search?ab_testing=false&appType=1&curr=rub&dest=-5551775&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&uclusters=8&uiv=2&uv=I9SxhqZZrQSnbKHHJPuo-yX5sPcpuiM7q5-bbCzLLhyorKbJsRSsejAXJYuxc6wFLSexzKATq8KtNiogpveg9Sg7rfSrC6vGobUxRhjiKjgloaFwMOIfxq6Jlg2pSqybrJ-tXSV6o-cr96cfqZmq4yJFMNIv16FULQIu0CeJJP4wXTHisIwtIia5qFCerCLCpLUweTA6qg8q0S-psC6t5TAFoX8wVSwkqc2tzKXzsMwqGyjZKBadxC1QMKYiUbDwLSmlpinprEQSgyxCreevnCinrOSo4atVJV2xXi1SIy0i1iWXrTOvvCxasRshQqy1MBQloTG1KAcmaif6sCo1Rw'
    try:
        response = requests.get(url=url2)
        response.raise_for_status()  # проверяем статус кода ответа
        # print(response.json()["data"])
        return response.json()

    except requests.RequestException as e:
        logging.debug(f"Error fetching data: {e}")
        return None


def prepare_items(response) -> list:
    products = []
    # print(response)
    products_row = response.get('data', {}).get('products', [])
    for product in products_row:
        if product.get('supplierRating', 0) > 4.5 and product.get('feedbacks', 0) > 1000:
            products.append({
                "id_gift": product.get('id', None),
                "shop": 'Wildberries',
                "brand": product.get('supplier', None),
                "name": product.get('name', None),
                "price": product.get('sizes', [])[0].get('price', {}).get('product', 'Цена не указана') / 100,
                "supplierRating": product.get('supplierRating', None),
                "feedbacks": product.get('feedbacks', None)
            })
    logging.debug(f'Products: {products}')
    return products


async def gift_list_generation(gifts, user_id):
    gifts_data = []
    for gift in gifts.split(','):
        logging.debug(gift)
        response = get_categories(query=gift)
        if response:
            list_products = prepare_items(response=response)
            if list_products:
                sorted_items = sorted(list_products, key=lambda im: im["price"])
                cheapest_item, most_expensive_item = sorted_items[0], sorted_items[-1]
                for item, status in [(cheapest_item, 'Дешевый'), (most_expensive_item, 'Дорогой')]:
                    logging.debug(f'item -{item}\nstatus -{status}')
                    item["gift"] = gift
                    item["user_id"] = user_id
                    item["status"] = status
                    logging.debug(f'Generates: {item}')
                    await db_manager.add_generate_gift(gifts_data=item)

# def read_json(user_id):
#     with open(f'services/gift_list{user_id}.json', 'r') as file:
#         data = json.load(file)
#     sorted_dict = sorted(data, key=lambda items: items["price"])
#     return sorted_dict


# if __name__ == '__main__':
#     main()
#     print(read_json()[0], read_json()[-1])
