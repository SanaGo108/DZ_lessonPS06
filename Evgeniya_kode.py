import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализируем браузер
driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://www.divan.ru/category/svet"

# Открываем веб-страницу
driver.get(url)

# Используем WebDriverWait для ожидания загрузки элементов
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'lsooF')))
except Exception as e:
    print(f"Ошибка ожидания элемента: {e}")
    driver.quit()
    exit()

# Находим все карточки с товарами с помощью названия класса
lights = driver.find_elements(By.CLASS_NAME, 'lsooF')

print(f"Найдено {len(lights)} светильников")

parsed_data = []

# Перебираем коллекцию товаров
for light in lights:
    try:
        # Находим элементы внутри карточки товара по значению CSS селектора
        title_element = light.find_element(By.CSS_SELECTOR, 'a.ProductName span[itemprop="name"]')
        title = title_element.text

        # Находим цену без скидки
        try:
            original_price_element = light.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU.ui-SVNym.bSEDs[data-testid="price"]')
            original_price = original_price_element.text
        except Exception as e:
            original_price = "N/A"
            print(f"Ошибка при парсинге цены без скидки: {e}")

        # Находим цену со скидкой
        try:
            discounted_price_element = light.find_element(By.CSS_SELECTOR, 'div.pY3d2 span[data-testid="price"]')
            discounted_price = discounted_price_element.text
        except Exception as e:
            discounted_price = "N/A"
            print(f"Ошибка при парсинге цены со скидкой: {e}")

        # Находим ссылку на товар
        try:
            link_element = light.find_element(By.CSS_SELECTOR, 'a[data-testid="color2"].ui-GPFV8.JudwW')
            link = link_element.get_attribute('href')
        except Exception as e:
            link = "N/A"
            print(f"Ошибка при парсинге ссылки на товар: {e}")

        print(title, original_price, discounted_price, link)
        parsed_data.append([title, original_price, discounted_price, link])
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Закрываем подключение браузера
driver.quit()

# Записываем данные в CSV файл
with open("light.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название светильника', 'Цена без скидки', 'Цена со скидкой', 'Ссылка на товар'])
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в light.csv")