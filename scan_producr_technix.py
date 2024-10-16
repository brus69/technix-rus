"""
Скрипт сканирование товаров синхронно
"""
from re import S
import csv
import requests
from bs4 import BeautifulSoup
import time

#Список url которые нужно проверить
urls = [
'https://technix-rus.ru/catalog/podshipniki/',
'https://technix-rus.ru/catalog/trapetseidalnye_gayki_i_vinty/',
'https://technix-rus.ru/catalog/sistemy_lineynogo_peremeshcheniya/',
'https://technix-rus.ru/catalog/shvp/',
'https://technix-rus.ru/catalog/zubchatye_reyki/',
'https://technix-rus.ru/catalog/soedinitelnye_mufty/',
'https://technix-rus.ru/catalog/elementy_soedineniya/',
'https://technix-rus.ru/catalog/smazki/',
'https://technix-rus.ru/catalog/vtulki/',
'https://technix-rus.ru/catalog/zvezdochki/',
'https://technix-rus.ru/catalog/zubchatye_kolesa/',
'https://technix-rus.ru/catalog/podshipniki_gost/',
'https://technix-rus.ru/catalog/podshipnikovye_uzly_agro_rider/',
'https://technix-rus.ru/catalog/shkivy_1/',
'https://technix-rus.ru/catalog/stupitsy_agro_rider/',
]


domain = 'https://technix-rus.ru'

def number_pages(url: str) -> int:
    try:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find('div', class_='nums'):
                html_nums = soup.find('div', class_='nums')
                num_link = html_nums.find_all('a', class_='dark_link')
            else:
                return 1
            count = 0
            for i in num_link:
                count = int(i.get_text())
            return count
        else:
            print('Ошибка', r.status_code)
    except Exception as e:
        print('Ошибка', e)

def links_products(url: str, pages: int) -> list:
    if pages >= 1:
        count = []
        for i in range(1, pages + 1):  # Исправляем начало индекса пагинации
            payload = {'PAGEN_1': i}
            r = requests.get(url, params=payload)
            print(r.url)
            soup = BeautifulSoup(r.text, 'html.parser')
            html_wrapper_inner = soup.find('div', id='content')
            html_link_item_title = html_wrapper_inner.find_all('div', class_='item-title')
            for i in html_link_item_title:
                url_product = domain + i.a.get('href')
                count.append(url_product)
        return count

def product_details(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Получаем название товара
        name_product = soup.h1.get_text() if soup.h1 else "Название не найдено"

        # Получаем цену товара
        price_value_element = soup.find('span', class_='price_value')
        price_value = price_value_element.get_text().replace('\xa0', '') if price_value_element else "Цена не найдена"

        # Получаем наличие товара
        availability_element = soup.find('span', class_='store_view dotted')
        availability = availability_element.get_text() if availability_element else "Наличие не указано"

        # Получаем количество товаров в наличии
        num_availability_html = soup.find('span', class_='value font_sxs')
        text = num_availability_html.get_text(strip=True) if num_availability_html else "Количество не указано"
        quantity = text.split(':')[-1].strip() if ':' in text else "Количество не указано"

        data = {
            'Url': url,
            'Название товара': name_product,
            'Цена': price_value,
            'Наличие': check_availability(availability),
            'Кол-во товаров в наличии': quantity
        }

        return data
    except Exception as e:
        print('Ошибка', e)

def check_availability(text):
    if text == 'Есть в наличии':
        return 'Да'
    elif text == 'Нет в наличии':
        return 'Нет'

def write_csv(data):
    seconds = time.time() + 10800
    local_time = time.localtime(seconds)  # Выравниваем по времени

    name_data_file = time.strftime('%d_%m_%Y', local_time)
    # Открываем файл в режиме "добавления" (append), чтобы не перезаписывать каждую строку
    with open(f'products_{name_data_file}.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Url', 'Название товара', 'Цена', 'Наличие', 'Кол-во товаров в наличии']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Если файл только создан, записываем заголовки
        file.seek(0, 2)  # Проверяем длину файла, чтобы избежать дублирования заголовков
        if file.tell() == 0:
            writer.writeheader()

        # Записываем строку данных
        writer.writerow(data)

# Основная логика
for i in urls:
  num_page = number_pages(i)
  list_product = links_products(i, num_page)
  for i in list_product:
      res = product_details(i)
      if res:
          print(res)
          write_csv(res)
