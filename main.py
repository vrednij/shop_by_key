import telebot
from telebot import types
import random
import threading

keys = {}

db_lock = threading.Lock()

ADMIN_ID = 'Твой админ айди'

def save_key(key, links):
    with db_lock:
        with open('keys.txt', 'a') as file:
            file.write(f"{key}:{links}\n")

TOKEN = 'Токен бота'
bot = telebot.TeleBot(TOKEN)

with open('keys.txt', 'a+') as file:
    pass

def load_keys():
    keys = {}
    with open('keys.txt', 'r') as file:
        for line in file:
            key, links = line.strip().split(':')
            keys[key] = links.split(',') if links else None
    return keys

keys = load_keys()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('ℹКак получить ключ?')
    markup.add('💌Дискорд сервер')
    markup.add('📋Отзывы')
    if message.from_user.id == ADMIN_ID:
        markup.add('/g_key')
        markup.add('/add')
    bot.send_message(message.chat.id, 'Йоу whats up, ты попал в ...., просто скинь мне ключ и получи файл...', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'ℹКак получить ключ?')
def get_admin_contacts(message):
    bot.send_message(message.chat.id, '☎ Для того чтобы получить ключ напиши одному из админов: @Vrednij_OVH....')

@bot.message_handler(func=lambda message: message.text == '💌Дискорд сервер')
def get_discord_server(message):
    bot.send_message(message.chat.id, '🔄 Ссылка на дискорд сервер: https://discord.gg/')

@bot.message_handler(func=lambda message: message.text == '📋Отзывы')
def get_reviews(message):
    bot.send_message(message.chat.id, '🏷 Ссылка на телеграм канал с отзывами: https://t.me/')

@bot.message_handler(commands=['g_key'])
def generate_key(message):
    if message.from_user.id == ADMIN_ID:
        key = ''.join(random.choice('0123456789ABCDEF') for _ in range(12))
        links = None
        keys[key] = links
        save_key(key, None)
        bot.send_message(message.chat.id, f'🔑 Вот ключ: {key}')
    else:
        bot.send_message(message.chat.id, '❌ Недостаточно прав для выполнения команды.')

@bot.message_handler(commands=['add'])
def add_link(message):
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, '❌ Неверно написал дебил, попробуй так: /add ключ ссылка')
        return
    key = args[1]
    link = args[2]
    if key in keys:
        if keys[key] is not None:
            bot.send_message(message.chat.id, f'♻ Ключ {key} уже был использован.')
        else:
            keys[key] = link
            save_key(key, link)
            bot.send_message(message.chat.id, f'✅ Ссылка успешно добавлена к ключу {key}.')
    else:
        bot.send_message(message.chat.id, f'❌ Ключ {key} не найден.')


@bot.message_handler(func=lambda message: True)
def get_links(message):
    key = message.text
    if key in keys:
        if keys[key] is not None:
            bot.send_message(message.chat.id, f'📋 Ссылка для ключа {key}:')
            bot.send_message(message.chat.id, keys[key])
            keys[key] = None
        else:
            bot.send_message(message.chat.id, f'❌ Ключ использован!')
    else:
        bot.send_message(message.chat.id, '❌ Неверный ключ. Попробуйте еще раз.')

bot.polling(none_stop=True)

