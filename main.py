import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Определяем URL сайта
url = 'https://www.cbr.ru/currency_base/daily/'

# Получаем HTML-страницу с помощью requests
response = requests.get(url)
html = response.text

# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html, 'html.parser')

# Находим таблицу с курсами валют
table = soup.find('table', {'class': 'data'})

# Создаем пустой список для данных о валютах
currencies = []

# Проходим по каждой строке таблицы
for tr in table.find_all('tr')[1:]:
    # Получаем название валюты и ее код
    name, code = [td.text.strip() for td in tr.find_all('td')[:2]]
    # Получаем курс валюты к рублю
    rate = float(tr.find_all('td')[4].text.replace(',', '.'))
    # Добавляем данные о валюте в список
    currencies.append({'name': name, 'code': code, 'rate': rate})

# Создаем DataFrame из списка данных о валютах
df = pd.DataFrame(currencies)

# Добавляем столбец с датой
now = datetime.now()
df['date'] = now.strftime('%Y-%m-%d')

# Сохраняем DataFrame в Excel-файл
filename = 'currency_rates_{}.xlsx'.format(now.strftime('%Y%m%d_%H%M%S'))
df.to_excel(filename, index=False)

print('Данные о курсах валют сохранены в файл', filename)