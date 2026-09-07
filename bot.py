import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message
from aiohttp import web
import aiohttp_cors  # нужно установить: pip install aiohttp-cors

BOT_TOKEN = "8872260684:AAHU65LnhHmLAItW3J6ECA-l9RyAOaSwAy8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. API-метод, который сайт вызывает для создания счета
async def create_invoice_handler(request):
    data = await request.json()
    stars = data.get("stars", 10) # Количество звезд по умолчанию

    # Создаем официальную ссылку на оплату Telegram Stars (валюта обязательно "XTR")
    invoice_link = await bot.create_invoice_link(
        title="Покупка попытки в рулетке",
        description=f"Дает право прокрутить рулетку за {stars} зв.",
        payload=f"roulette_spin_{stars}",
        provider_token="",  // ДЛЯ ЗВЕЗД ВСЕГДА ПУСТАЯ СТРОКА!
        currency="XTR",
        prices=[LabeledPrice(label="Звезды", amount=stars)]
    )

    return web.json_response({"invoice_url": invoice_link})

# 2. Обязательный этап проверки перед покупкой
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

# 3. Обработка успешной оплаты
@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment_info = message.successful_payment
    total_stars = payment_info.total_amount
    await message.answer(f"🎉 Спасибо! Платеж на {total_stars} ⭐ успешно зачислен.")

async def main():
    app = web.Application()
    
    # Настраиваем CORS, чтобы сайт (GitHub/Vercel) мог стучаться к вашему серверу
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
    })

    route = app.router.add_post('/api/create-invoice', create_invoice_handler)
    cors.add(route)

    # Запускаем локальный веб-сервер для бэкенда на порту 8080
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
