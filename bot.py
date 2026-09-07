import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import PreCheckoutQuery, Message

BOT_TOKEN = "8872260684:AAHU65LnhHmLAItW3J6ECA-l9RyAOaSwAy8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обязательное подтверждение платежа перед списанием
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# Сообщение от бота СРАЗУ ПОСЛЕ оплаты
@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    # Закрываем Mini App (если нужно) или просто отправляем сообщение в чат
    await message.answer("🎉 Оплата принята! Игра начинается! 🎰")


async def main():
    print("Бот запущен и ждет оплаты...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
