import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

TOKEN = '6222913580:AAG524H9EyYMOpNJ3OScMxWJbVSxLmQBwOA'

exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Hello!'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные варианты валют: '
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Некорректное количество указанных параметров')
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в операции\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка\n{e}')
    else:
        bot.reply_to(message, answer)


bot.infinity_polling()
