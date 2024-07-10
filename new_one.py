import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализируем браузер
driver = webdriver.Chrome()

# Указываем URL для парсинга
url = "https://www.divan.ru/category/podvesnye-svetilniki"

# Открываем указанную страницу
driver.get(url)

# Используем WebDriverWait для ожидания загрузки элементов
wait = WebDriverWait(driver, 10)

# Находим все карточки с товарами с помощью селектора
try:
    lights = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.VHx4T.ZdH1P.kQXIE')))
except Exception as e:
    print(f"Не удалось найти элементы с товарами: {e}")
    driver.quit()
    exit()

parsed_data = []

for light in lights:
    try:
        # Находим название товара
        name = light.find_element(By.CSS_SELECTOR, 'a[data-testid="color2"] span[itemprop="name"]').text

        # Находим цену товара
        price = light.find_element(By.CSS_SELECTOR, 'div.pY3d2 span[data-testid="price"]').get_attribute('content')

        # Находим ссылку на товар
        link = light.find_element(By.CSS_SELECTOR, 'a[data-testid="color2"]').get_attribute('href')

        # Добавляем данные в список
        parsed_data.append([name, price, link])
    except Exception as e:
        print(f"Произошла ошибка при парсинге элемента: {e}")
        continue

# Закрываем браузер
driver.quit()

# Записываем данные в CSV файл
with open("new.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара', 'Цена', 'Ссылка на товар'])
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в new.csv")