import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Только токен от BotFather (можно вписать прямо сюда или через переменные окружения)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8838093580:AAEDZArbQx7N5B-acHHp9JIkSCuf6nToQFI")
AUTO_REPLY_TEXT = "Привет! Сейчас меня нет на сети, отвечу позже. 1+ rep 🇺🇸"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
  await message.answer("Бот-автоответчик успешно активирован!")


@dp.message()
async def all_messages_handler(message: types.Message):
  if message.chat.type == "private":
    await message.answer(AUTO_REPLY_TEXT)


async def main():
  logging.basicConfig(level=logging.INFO)
  print("Бот запущен и ждет сообщения...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
