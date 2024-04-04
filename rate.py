import telebot
from telebot import types
from currency_parser import connect_to_database, save_currency_to_db, parse_currency

bot_token = '6996194767:AAGNccCPWwrpplVbqmrw8n-sFgcPx77ji28'
bot = telebot.TeleBot(bot_token)

def save_currency_rate(connection, currency_code, row_value, chat_id):
    rate_info = parse_currency(currency_code, row_value)
    if isinstance(rate_info, dict):
        month = 'April'
        save_currency_to_db(connection, currency_code, rate_info['Покупка'], rate_info['Продажа'], month)
        bot.send_message(chat_id, f"Курс {currency_code}:\nПокупка: {rate_info['Покупка']}\nПродажа: {rate_info['Продажа']}")
    else:
        bot.send_message(chat_id, f"Ошибка при парсинге информации о курсе {currency_code}")

def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currencies = ['USD', 'EUR', 'RUB', 'KZT']
    buttons = [types.KeyboardButton(text=currency) for currency in currencies]
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler(commands=['start'])
def send_currencies(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, "Выберите валюту:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ['USD', 'EUR', 'RUB', 'KZT'])
def send_currency_rate(message):
    currency = message.text
    connection = connect_to_database()
    if connection:
        if currency == 'USD':
            save_currency_rate(connection, 'USD', 'row0', message.chat.id)
        elif currency == 'EUR':
            save_currency_rate(connection, 'EUR', 'row1', message.chat.id)
        elif currency == 'RUB':
            save_currency_rate(connection, 'RUB', 'row1', message.chat.id)
        elif currency == 'KZT':
            save_currency_rate(connection, 'KZT', 'row0', message.chat.id)
        else:
            print("Выбранная валюта не поддерживается.")

        bot.send_message(message.chat.id, f"Данные о курсе {currency} сохранены в базе данных.")

    else:
        bot.send_message(message.chat.id, "Ошибка подключения к базе данных.")

bot.polling()
