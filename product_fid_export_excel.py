"""
Скрипт берёт товарный фид и преобразует в Excel
"""
import requests
import xml.etree.ElementTree as ET
import csv

# URL XML файла
url = 'https://technix-rus.ru/bitrix/catalog_export/yandex_feed_v2.xml'

# Получаем XML данные
r = requests.get(url)

# Проверяем статус код ответа
if r.status_code == 200:
    # Парсинг XML данных
    root = ET.fromstring(r.content)

    # Открываем CSV файл для записи
    with open('offers.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Записываем заголовки
        writer.writerow(['ID', 'Модель', 'Цена', 'Производитель', 'Описание', 'Ссылка'])

        # Извлечение информации о товарах (offers)
        for offer in root.findall('.//offer'):
            offer_id = offer.get('id')
            offer_url = offer.find('url').text
            offer_price = offer.find('price').text
            offer_model = offer.find('model').text
            offer_vendor = offer.find('vendor').text

            # Проверка на наличие description
            offer_description = offer.find('description')
            offer_description_text = offer_description.text if offer_description is not None else "Описание отсутствует"

            # Записываем данные в CSV
            writer.writerow([offer_id, offer_model, offer_price, offer_vendor, offer_description_text, offer_url])

    print("Данные успешно сохранены в 'offers.csv'.")
else:
    print(f"Ошибка: {r.status_code}")
