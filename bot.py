import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

# Токен первого бота (Магазин): @vouch_01_rep_bot
SHOP_TOKEN = "8838093580:AAEDZArbQx7N5B-acHHp9JIkSCuf6nToQFI"

# Токен второго бота (Админ-бот), который присылает тебе уведомления
ADMIN_BOT_TOKEN = "8623258820:AAEInCHPfQXtgMcW6i5Ftt07ewy9JXFlxaE"

# Твой реальный Telegram ID
MY_TELEGRAM_ID = 8706958823

bot_shop = Bot(token=SHOP_TOKEN)
bot_admin_sender = Bot(token=ADMIN_BOT_TOKEN)
dp = Dispatcher()

stock_available = True  # В наличии 1 шт. (+65)


@dp.message(CommandStart())
async def start_handler(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
      types.InlineKeyboardButton(
          text="🎁 Забрать номер +65 🇸🇬 (0 ⭐)", callback_data="claim_free_number"
      ),
  ]])
  await message.answer(
      "👋 Добро пожаловать!\n\n"
      "📦 **Товар в наличии:**\n"
      "• Номер: `+65` (Сингапур)\n"
      "• Цена: **0 ⭐** (Бесплатно)\n\n"
      "Нажми кнопку ниже, чтобы забрать:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )


@dp.callback_query(F.data == "claim_free_number")
async def process_claim(callback: types.CallbackQuery):
  global stock_available

  if not stock_available:
    await callback.answer(
        "❌ Этот номер уже кто-то забрал! Больше нет в наличии.", show_alert=True
    )
    return

  # Снимаем товар с наличия, чтобы больше никто не забрал
  stock_available = False
  secret_number = "+65 1234 5678 (данные для входа / код)"

  # 1. Выдаем номер пользователю прямо в чат
  await callback.message.edit_text(
      "✅ **Номер успешно получен!** 🎉\n\n"
      "Вот твой товар:\n"
      f"🔒 `{secret_number}`",
      parse_mode="Markdown",
  )

  # 2. Собираем данные о покупателе
  buyer = callback.from_user
  buyer_name = buyer.full_name
  buyer_username = f"@{buyer.username}" if buyer.username else "нет юзернейма"
  buyer_id = buyer.id

  # 3. Формируем отчет для тебя
  notification_text = (
      "🚨 **Кто-то забрал номер (+65)!**\n\n"
      f"👤 **Пользователь:** {buyer_name} ({buyer_username})\n"
      f"🆔 **ID:** `{buyer_id}`\n"
      "📦 **Товар:** Номер +65\n"
      "⭐ **Цена:** 0 Stars"
  )

  # Кнопка для быстрой связи с этим конкретным пользователем
  contact_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
      types.InlineKeyboardButton(
          text="💬 Написать покупателю", url=f"tg://user?id={buyer_id}"
      )
  ]])

  # 4. Второй бот отправляет тебе личное уведомление с рабочей кнопкой
  try:
    await bot_admin_sender.send_message(
        chat_id=MY_TELEGRAM_ID,
        text=notification_text,
        reply_markup=contact_keyboard,
        parse_mode="Markdown",
    )
  except Exception as e:
    logging.error(f"Не удалось отправить уведомление админу: {e}")

  await callback.answer()


async def main():
  logging.basicConfig(level=logging.INFO)
  print("Бот запущен и готов к работе...")
  await dp.start_polling(bot_shop)


if __name__ == "__main__":
  asyncio.run(main())
