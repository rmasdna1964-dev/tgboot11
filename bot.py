import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message

# Укажите токен вашего бота от @BotFather
BOT_TOKEN = "8872260684:AAHU65LnhHmLAItW3J6ECA-l9RyAOaSwAy8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Обработка команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Нажми на кнопку Mini App ниже, чтобы запустить Рулетку."
    )

# 2. Ловим клик из Mini App (когда пользователь нажимает "Крутить за 5 ⭐")
@dp.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    if message.web_app_data.data == "buy_spin_5":
        await message.answer_invoice(
            title="Попытка в рулетке",
            description="Вращение рулетки за 5 Telegram Stars",
            payload="spin_5_stars_payload",
            provider_token="",  # Для Stars оставляем пустым
            currency="XTR",     # Валюта Telegram Stars
            prices=[
                LabeledPrice(label="5 Звёзд", amount=5)
            ]
        )

# 3. Подтверждение готовности принять платеж (обязательный шаг Telegram)
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 4. Обработка успешной оплаты
@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment = message.successful_payment
    await message.answer(
        f"🎉 **Оплата успешно прошла!**\n\n"
        f"Вы заплатили {payment.total_amount} ⭐.\n"
        f"🎰 Вращаем рулетку..."
    )
    # Здесь можно добавить логику выпадения приза (выдача предмета, случайное число и т.д.)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
