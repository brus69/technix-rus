"""
Скрипт вытаскивает данные из товарного фида
"""

import xml.etree.ElementTree as ET


# Парсинг XML данных
root = ET.parse("yandex_feed_v2.xml")

# Извлечение предложений
offers = root.find('shop').find('offers').findall('offer')

def parse_offer(offer):
    offer_id = offer.get('id')
    url = offer.find('url').text
    price = offer.find('price').text
    currency_id = offer.find('currencyId').text
    category_id = offer.find('categoryId').text
    pictures = [pic.text for pic in offer.findall('picture')]
    vendor = offer.find('vendor').text
    model = offer.find('model').text
    type_prefix = offer.find('typePrefix').text
    sales_notes = offer.find('sales_notes').text
    params = {param.get('name'): param.text for param in offer.findall('param')}

    return {
        'ID': offer_id,
        'URL': url,
        'Price': price,
        'Currency': currency_id,
        'Category ID': category_id,
        'Pictures': pictures,
        'Vendor': vendor,
        'Model': model,
        'Type Prefix': type_prefix,
        'Sales Notes': sales_notes,
        'Parameters': params
    }


# Вывод предложений
print("Предложения:")
for offer in offers:
  offer_data = parse_offer(offer)
  # print(f"ID категории: {offer_data['Category ID']}")
  if offer_data['Category ID'] == "264" or offer_data['Category ID'] == "67":
    # print(f"ID предложения: {offer_data['ID']}")
    print(f"{offer_data['URL']}")
    # print(f"Цена: {offer_data['Price']}")
    # print(f"Валюта: {offer_data['Currency']}")
    # print(f"ID категории: {offer_data['Category ID']}")
    # print(f"Изображения:")
    # for pic in offer_data['Pictures']:
    #     print(f"  - {pic}")
    # print(f"Производитель: {offer_data['Vendor']}")
    # print(f"Модель: {offer_data['Model']}")
    # print(f"Тип: {offer_data['Type Prefix']}")
    # print(f"Условия продажи: {offer_data['Sales Notes']}")
    # print(f"Параметры:")
    # for key, value in offer_data['Parameters'].items():
    #     print(f"  - {key}: {value}")
