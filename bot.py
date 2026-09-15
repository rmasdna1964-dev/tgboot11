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

# Твой токен бота @shadowboto_bot
TOKEN = "8955553619:AAFzP7YvQW96OJ_UCG8plZcHau9EUZI3DsI"

router = Router()

# Команда /start (поддерживает переход с сайта через параметр)
@router.message(CommandStart())
async def cmd_start(message: Message):
    print(f"[LOG] Команда /start получена от пользователя: {message.from_user.id} (@{message.from_user.username})")
    
    args = message.text.split()
    # Если перешли по ссылке с сайта с параметром покупки номера +65
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
        "👋 Привет! Добро пожаловать в официальный бот магазина **@shadowboto_bot**.\n\n"
        "Здесь вы можете приобрести личный Telegram-номер **+65** за Звезды ⭐.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Команда /help и кнопка помощи
@router.message(Command("help"))
@router.callback_query(F.data == "help_info")
async def cmd_help(event: Message | CallbackQuery):
    text = (
        "🤖 **Доступные команды бота:**\n\n"
        "/start — Главное меню\n"
        "/buy — Купить номер +65 за 150 ⭐\n"
        "/help — Список команд"
    )
    if isinstance(event, CallbackQuery):
        await event.message.answer(text, parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, parse_mode="Markdown")

# Команда /buy
@router.message(Command("buy"))
async def cmd_buy(message: Message):
    await send_invoice_number_65(message)

# Обработка нажатия кнопки покупки в боте
@router.callback_query(F.data == "buy_number_65")
async def callback_buy_number(callback: CallbackQuery):
    await send_invoice_number_65(callback.message)
    await callback.answer()

# Функция отправки счета на оплату Звездами (currency="XTR")
async def send_invoice_number_65(message: Message):
    print(f"[LOG] Выставление инвойса на номер +65 для пользователя {message.chat.id}")
    prices = [LabeledPrice(label="Номер +65", amount=150)]
    
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="Покупка номера +65",
        description="Личный номер телефона для Telegram. После оплаты бот выдаст данные.",
        payload="number_65_payload",
        currency="XTR",  # Валюта Telegram Stars
        prices=prices,
        start_parameter="buy-number-65"
    )

# Обязательное подтверждение платежа перед списанием
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    print(f"[LOG] Предоплата запрошена для пользователя {pre_checkout_query.from_user.id}")
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Успешная оплата
@router.message(F.successful_payment)
async def success_payment(message: Message):
    payment_info = message.successful_payment
    print(f"[LOG] УСПЕШНАЯ ОПЛАТА! Пользователь {message.from_user.id} оплатил {payment_info.total_amount} XTR")
    
    await message.answer(
        "🎉 **Оплата успешно прошла!**\n\n"
        "Спасибо за покупку номера **+65** за 150 ⭐.\n"
        "Администратор уже уведомлен, скоро вам пришлют данные от аккаунта.",
        parse_mode="Markdown"
    )

async def main():
    # Инициализация бота
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Сбрасываем вебхуки на случай, если они висели, и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот @shadowboto_bot успешно запущен и ожидает сообщения...")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
