import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Все url сохранить в файлик
url_data = 'url_data.txt'

def check_url_status(url):
    try:
        payload = {'utm': 'test'} #Добавляем тестовые параметры
        r = requests.get(url.strip(), timeout=5, params=payload)
        r.raise_for_status()  # Проверка на HTTP ошибки
        soup = BeautifulSoup(r.text, 'html.parser')
        h1_tag = soup.h1
        h1_text = h1_tag.get_text() if h1_tag else "No H1 tag"
        data = {
            "url": url.strip(),
            "status_code": r.status_code,
            "h1": h1_text
        }
        return data
    except requests.RequestException as e:
        return {
            "url": url.strip(),
            "status_code": "Error",
            "h1": str(e)
        }

def main():
    with open(url_data, "r") as f:
        url_list = f.readlines()
        url_list = list(set(url.strip() for url in url_list))  # Удаление дубликатов и пробелов

    filename = f"{datetime.now().isoformat(timespec='minutes')}_excel.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['url', 'status_code', 'h1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url in url_list:
            result = check_url_status(url)
            print(result)
            writer.writerow(result)

if __name__ == "__main__":
    main()
