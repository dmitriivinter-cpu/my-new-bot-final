import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Загружаем ключи из .env
load_dotenv()

# Создаем объекты бота и диспетчера
bot = Bot(token="8509780467:AAEFupPlKIOFXPccj3_SZ1aQJpZYH1B67tA")
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    # Вставляем рабочую ссылку для проверки WebApp
    web_app = WebAppInfo(url="https://dmitriivinter-cpu.github.io/my-telegram-shop/") 
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Открыть магазин 🛒", web_app=web_app)]
        ],
        resize_keyboard=True
    )
    
    await message.answer("Джарвис на связи! Нажми кнопку ниже:", reply_markup=kb)

    
    await message.answer("Джарвис ожил! Нажми кнопку ниже:", reply_markup=kb)

# Главная функция запуска
async def main():
    print("Бот успешно запущен на Python 3.13!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")

