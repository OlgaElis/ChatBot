import telebot
from config import currency, TOKEN
from extentions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Если хотите перевести одну валюту в другу, то введите запрос в формате:\n<Название переводимой валюты> \
    <Название валюты, в которую надо перевести> \
    <Количество переводимой валюты>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Вы можете выбрать валюты: '
    for cur in currency.keys():
        text = '\n'.join((text, cur, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def exchange(message: telebot.types.Message):
    try:
        info = message.text.split(' ')

        if len(info) > 3 or len(info) <= 2:
            raise APIException(f'Параметров должно быть 3')

        base, quote, amount = info
        global_currency = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Вы ввели неверные данные: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Увы, бот не смог обработать команду \n{e}')
    else:
        text = f"Cумма {amount} {base} в {quote} составляет {global_currency}"
        bot.send_message(message.chat.id, text)

bot.polling()


