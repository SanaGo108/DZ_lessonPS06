import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://www.divan.ru/category/podvesnye-svetilniki"

driver.get(url)
time.sleep(3)

vacancies = driver.find_elements(By.CLASS_NAME, 'VHx4T ZdH1P kQXIE')
parsed_data = []
for vacancy in vacancies:
   try:
       name = vacancy.find_element(By.CSS_SELECTOR, 'span itemprop="name"').text
       price = vacancy.find_element(By.CSS_SELECTOR, 'meta itemprop="price"').text
       link = vacancy.find_element(By.CSS_SELECTOR, 'a.itemprop="availability"').get_attribute('href')
   except:
       print("произошла ошибка при парсинге")
       continue

   parsed_data.append([name, price, link])

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара',  'цена', 'ссылка на товар'])
    writer.writerows(parsed_data)
