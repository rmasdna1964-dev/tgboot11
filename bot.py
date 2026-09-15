import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice,
    PreCheckoutQuery
)

TOKEN = "8955553619:AAFzP7YvQW96OJ_UCG8plZcHau9EUZI3DsI"

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    print(f"--> Получена команда /start от пользователя: {message.from_user.id} ({message.from_user.username})")
    args = message.text.split()
    if len(args) > 1 and args[1] == "buy_number_65":
        await send_invoice_number_65(message)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📱 Купить номер +65 (150 ⭐)", callback_data="buy_number_65")],
            [InlineKeyboardButton(text="ℹ️ Помощь / Команды", callback_data="help_info")]
        ]
    )
    await message.answer(
        "👋 Привет! Добро пожаловать в **@shadowboto_bot**.\n\n"
        "Здесь ты можешь приобрести личный Telegram-номер **+65** за Звезды ⭐.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(Command("buy"))
@router.callback_query(F.data == "buy_number_65")
async def cmd_buy(event: Message | CallbackQuery):
    print("--> Запрос на покупку номера +65")
    message = event.message if isinstance(event, CallbackQuery) else event
    await send_invoice_number_65(message)
    if isinstance(event, CallbackQuery):
        await event.answer()

async def send_invoice_number_65(message: Message):
    prices = [LabeledPrice(label="Номер +65", amount=150)]
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="Покупка номера +65",
        description="Личный номер телефона для Telegram. После оплаты бот выдаст данные.",
        payload="number_65_payload",
        currency="XTR",
        prices=prices,
        start_parameter="buy-number-65"
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def success_payment(message: Message):
    await message.answer(
        "🎉 **Оплата успешно прошла!**\n\n"
        "Спасибо за покупку номера **+65** за 150 ⭐.",
        parse_mode="Markdown"
    )

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Бот @shadowboto_bot запущен и ожидает сообщения...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
