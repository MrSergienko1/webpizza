from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('6979254246:AAFo-QqJi1Df6Q5qZBTs6vILJH-oQjf7c8c')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://itproger.com/telegram.html')))
    await message.answer('Привет,мой друг!', reply_markup=markup)
executor.start_polling(dp)