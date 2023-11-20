import telebot
import sqlite3
import webbrowser
from telebot import types
bot = telebot.TeleBot('6979254246:AAFo-QqJi1Df6Q5qZBTs6vILJH-oQjf7c8c')
name = None
#как только запускаешь бота сразу появляются кнопки
@bot.message_handler(commands=['start'])
def start(message):
    #видео 4
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    # конец видео
    bot.send_message(message.chat.id, 'Привет, сейчас зарегистрируемся! Введите ваше имя ')
    bot.register_next_step_handler(message, user_name)
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn1)
    markup.row(btn2, btn3)
    #приветсвует в виде аудиофайла
    '''file = open('./photo.mp3', 'rb')
    bot.send_audio(message.chat.id, file , reply_markup=markup)'''
    #вместо приветствия отправляет файл
    file = open('./photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    #приветсвует в виде текстого сообщения
    '''bot.send_message(message.chat.id, 'Привет', reply_markup=markup)'''
    #чтобы кнопки работали то нужно их закодить следсвенно то что будет ниже; pov - если нажать на одну кнопку то остальные не сработуют поэтому нужно кодить их отдельно
    bot.register_next_step_handler(message, on_click)
#видео 4
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль ')
    bot.register_next_step_handler(message, user_pass)
def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    #bot.send_message(message.chat.id, 'Введите пароль ')
    #bot.register_next_step_handler(message, user_pass)
#ПРОДОЛЖЕНИЕ ЧТОБЫ КНОПКИ РАБОТАЛИ
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)
# конец видео
def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website  is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Delete')

# перекидывает на ссылку которую ты указал
@bot.message_handler(commands=['site','website'])
def site(message):
    webbrowser.open('https://www.hse.ru')

# start чтобы написал привет, {message.from_user.first_name}-для того чтобы бот к нам обращался по имени
'''
@bot.message_handler(commands=['start','main','hello'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
'''
# help чтобы написал информацию для помощи
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'Help information')
#обрабатывает информацию который ты написал к примеру если написал id то он выведет твой айди
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

#reply markup -при отправке фото комментирует его;markup.add- добавляет кнопки внутри;callback_data- это при нажатии делает то что ты написал после колбэка
#markup.row-выстраивает кнопки в ряд
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1)
    markup.row(btn2,btn3)
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)
#@bot.callback_query_handler-каждый раз при нажатии на колбэк дата которая выше то она перекинет ее на этот бот queryhandler который будет отвечать за саму кнопку
# lambda - это анонимная функция. колбэк тру возвращает тру в случае если ламбда будет обладать нулевым параметрам
# callback.message.chat.id - сначала обращается к колбек потом к месаж потом к чату потом к айди
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        # - 1 это удалять предыдущее сообщение -2 это удалить 2-ое предыдущее сообщение
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

# чтобы работала постоянно
bot.polling(none_stop=True)