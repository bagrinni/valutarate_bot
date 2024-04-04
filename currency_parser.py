import requests
from bs4 import BeautifulSoup as Bs
import psycopg2
from psycopg2 import Error

def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="bagr",
            password="2569",
            host="localhost",
            database="valutarate"
        )
        return connection
    except (Exception, Error) as error:
        print(error)

def save_currency_to_db(connection, currency_name, buy_rate, sell_rate, month):
    try:
        cursor = connection.cursor()
        insert_query = '''INSERT INTO currency (currency_name, buy_rate, sell_rate, month)
                          VALUES (%s, %s, %s, %s);'''
        cursor.execute(insert_query, (currency_name, buy_rate, sell_rate, month))
        connection.commit()
        cursor.close()
    except (Exception, Error) as error:
        print(error)

def parse_currency(currency_code, row_value):
    URL = 'https://www.optimabank.kg/index.php?option=com_nbrates&view=default&Itemid=196&lang=ru'  
    r = requests.get(URL)
    soup = Bs(r.content, 'html.parser')
    
    block = soup.find(f'div', class_=f'iso-{currency_code} {row_value}')  
    buy_rate = block.find('div', class_='rate buy').find('span').get_text(strip=True)
    sell_rate = block.find('div', class_='rate sell').find('span').get_text(strip=True)
    return {'Покупка': buy_rate, 'Продажа': sell_rate}
