import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Converter
from datetime import datetime


bot = telebot.TeleBot(TOKEN)

current_datetime = datetime.now()

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! Чтобы начать работу введите команду боту в следующем формате:' \
           '\n<имя валюты цену которой нужно узнать>' \
            '<имя валюты в которой надо узнать цену первой валюты> ' \
            '<количество первой валюты> ' \
            '\nПример команды боту: Доллар Рубль 500' \
            '\nПосмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # text = f'Цена {amount} {quote} в {base} - {total_base}'
        total_base = round(float(total_base)*float(amount), 2)
        text = f'Цена {amount} {quote} в {base} - {total_base}\n Актуально на {current_datetime.hour} часов {current_datetime.minute} минут '
        bot.send_message(message.chat.id, text)


bot.polling()

