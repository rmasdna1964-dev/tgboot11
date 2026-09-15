import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import LabeledPrice

# Твой токен бота от BotFather
TOKEN = "8838093580:AAEDZArbQx7N5B-acHHp9JIkSCuf6nToQFI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Данные нашего единственного товара
ITEM_TITLE = "Виртуальный номер +65"
ITEM_DESCRIPTION = "Покупка номера +65 (Сингапур). В наличии 1 шт."
PRICE_IN_STARS = 50  # Стоимость в звездах (можешь изменить на свою)

# Переменная для контроля наличия (1 — есть, 0 — продан)
stock_available = True


# Команда /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
      types.InlineKeyboardButton(
          text=f"Купить номер +65 🇸🇬 ({PRICE_IN_STARS} ⭐)",
          callback_data="buy_number"),
  ]])

  await message.answer(
      "👋 Добро пожаловать в магазин номеров!\n\n"
      "📦 **Товар в наличии:**\n"
      "• Номер: `+65` (Сингапур)\n"
      f"• Цена: {PRICE_IN_STARS} ⭐\n\n"
      "Нажми кнопку ниже для покупки:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )


# Обработка нажатия на кнопку покупки
@dp.callback_query(F.data == "buy_number")
async def process_buy(callback: types.CallbackQuery):
  global stock_available

  if not stock_available:
    await callback.answer(
        "❌ Этот номер уже купили! Больше нет в наличии.", show_alert=True
    )
    return

  # Создаем инвойс на оплату Telegram Stars (валюта 'XTR' — это Звезды)
  prices = [LabeledPrice(label="Номер +65", amount=PRICE_IN_STARS)]

  await callback.message.answer_invoice(
      title=ITEM_TITLE,
      description=ITEM_DESCRIPTION,
      prices=prices,
      provider_token="",  # Для цифровых товаров и Звезд параметр всегда пустой ("")
      payload="number_65_payload",
      currency="XTR",  # Код валюты Telegram Stars
  )
  await callback.answer()


# Обязательный этап: предварительная проверка чека перед списанием звезд
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
  global stock_available
  if not stock_available:
    await pre_checkout_query.answer(
        ok=False, error_message="К сожалению, товар только что закончился!"
    )
    return
  await pre_checkout_query.answer(ok=True)


# Успешная оплата (товар куплен)
@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
  global stock_available

  if not stock_available:
    await message.answer("Ошибка: товар уже был продан.")
    return

  # Снимаем товар с продажи
  stock_available = False

  # Сам выданный номер (скрыт под спойлер или отправлен текстом)
  secret_number = "+65 1234 5678 (данные для входа / код)"

  await message.answer(
      "✅ **Оплата прошла успешно! Спасибо за покупку!** 🎉\n\n"
      "Вот твой товар (номер +65):\n"
      f"🔒 `{secret_number}`\n\n"
      "Товар продан, больше в наличии нет.",
      parse_mode="Markdown",
  )


async def main():
  logging.basicConfig(level=logging.INFO)
  print("Магазин запущен и ждет покупателей...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
