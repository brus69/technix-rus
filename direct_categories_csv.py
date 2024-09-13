import csv
import re
import requests
from bs4 import BeautifulSoup

domains = 'https://technix-rus.ru'
url="https://technix-rus.ru/catalog/"
r = requests.get(url, timeout=10)
name_csv = 'direct.csv'

def black_list():
  ...
  #Страницы которые не нужно добавлять в csv файлик

def catalog_url_hub(html: str) -> list:
  #Страницы хаб если нужно можно добавить отдельно
  soup = BeautifulSoup(html, 'html.parser')
  html_hub = soup.find_all('a', class_='dark_link')
  return html_hub

def catalog_url(html: str) -> list:
  #страницы певого и второго уровня
  soup = BeautifulSoup(html, 'html.parser')
  html = soup.find_all('a', class_='muted777')
  html_one = soup.find_all('a', class_='parent1 section1')
  html.extend(html_one)
  return html

def data_page(data_url) -> dict:
  # Формирование данных о разделе
  r = requests.get(data_url, timeout=10)
  soup = BeautifulSoup(r.text, "html.parser")
  # Исходная строка
  try:
    input_string = soup.find('span', class_='price_value').text
    # Используем регулярное выражение для поиска только цифр
    digits_only = re.sub(r'\D', '', str(input_string))
  except Exception as e:
    print('Нет цены', data_url)
    digits_only = 0

  data = {
      "h1": soup.h1.text,
      "Url": data_url,
      "Title": soup.title.text,
      "Description": soup.find('meta', {'name':'description'}).get('content'),
      "Offer minimal price": digits_only,
      'Currency': 'RUB',
      'Image url 1':domains + soup.find('img', class_='img-responsive').get('src')
  }
  return data

def save_data_csv(data):
  # сохранение результатов в csv
  with open(name_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['h1', 'Url', 'Title', 'Description', 'Offer minimal price', 'Currency', 'Image url 1']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Запись заголовков
    writer.writeheader()

    # Запись строк данных
    for row in data:
        writer.writerow(row)

def main():
  #Страница HUB не участвует в поиске
  catalog_list = catalog_url(r.text)
  count = []
  num = len(catalog_list)
  for i in catalog_list:
    url = domains + i.get('href')
    data_page_r = data_page(url)
    count.append(data_page_r)
    num = num - 1
    print(num)
  save_data_csv(count)


main()
