"""
Проверка урлов на статус ответа и заголовок h1
"""
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


#Все url сохранить в файлик
url_data = 'url_data.txt'

def check_url_satatus(url):
  r = requests.get(url, timeout=10)
  soup = BeautifulSoup(r.text, 'html.parser')
  data = {
      "url": url,
      "status_code": r.status_code,
      "h1": soup.h1.get_text()
  }
  return data

def main():
  with open(url_data, "r") as f:
    url_list = f.readlines()
    limit_url = len(url_list)

  with open(f"{datetime.now().isoformat(timespec='minutes')}_excel.csv", 'a', newline='') as csvfile:
    fieldnames = ['url', 'status_code', 'h1']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in url_list:
      limit_url -= 1
      print(limit_url, check_url_satatus(i))
      writer.writerow(check_url_satatus(i))

if __name__ == "__main__":
  main()
    
