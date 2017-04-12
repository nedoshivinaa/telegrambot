# -*- coding: utf-8 -*-
import config
import telebot
import logging

from subprocess import call

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('Bot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

bot = telebot.TeleBot(config.token)
#upd=bot.get_updates()
#print(upd[-1].message)

bot.send_message(154928, "Bot is online")
#bot.send_message(245768282, "Текст")

@bot.message_handler(commands=['start'])
def send_start(message):
    # отправка простого сообщения
    bot.send_message(message.chat.id, "Привет, я тестовый бот! Отправьте мне /help для вывода справки.")

@bot.message_handler(commands=['help'])
def send_help(message):
    # отправка сообщения с поддержкой разметки Markdown
    bot.send_message(message.chat.id, "".join(config.help_string), parse_mode="Markdown")

@bot.message_handler(commands=['command1'])
def send_server(message):
    try:
        # по этому пути на сервере лежит скрипт сбора информации по статусу сервера
        call(["status.sh"])
        # читает файл с результатами выполнения скрипта
        status = open("status.txt", "rb").read()
        bot.send_message(message.chat.id, status, parse_mode="Markdown")
    except Exception as e:
        logger.exception(str(e))
        bot.send_message(message.chat.id, "Ошибка при получении статуса сервера. Подробности в журнале.")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)



bot.polling(none_stop=True)
