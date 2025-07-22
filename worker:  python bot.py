import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Получение токена из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer("👋 Привет! Бот запущен и готов к работе.")

# Ответ на любые другие сообщения
@dp.message_handler()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
