import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.exceptions import TelegramNetworkError, TelegramUnauthorizedError
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8600154020:AAE8MmsT_VW0slRs_Mv0NDWGeAXgpJj1d94"
ADMIN_ID = 8650896211

CARD_NUMBER = "5614 6827 1472 4137"
CARD_NAME = "Abdullayeva Xosiyatjon"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_products_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐ VIP - 100 000 so'm", callback_data="prod_1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌟 VIP+ - 150 000 so'm", callback_data="prod_2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 Gold - 200 000 so'm", callback_data="prod_3"
                )
            ],
        ]
    )


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Xush kelibsiz! Kerakli tarifni tanlang:",
        reply_markup=get_products_keyboard(),
    )


@dp.callback_query(F.data.startswith("prod_"))
async def process_product(callback: types.CallbackQuery):
    products = {
        "prod_1": ("VIP tarif", "100 000 so'm"),
        "prod_2": ("VIP+ tarif", "150 000 so'm"),
        "prod_3": ("Gold tarif", "200 000 so'm"),
    }

    title, price = products[callback.data]

    caption = (
        f"<b>📦 Tanlangan tarif:</b> {title}\n"
        f"<b>💰 Narxi:</b> {price}\n\n"
        "💳 <b>To'lov uchun karta:</b>\n"
        f"<code>{CARD_NUMBER}</code>\n"
        f"👤 <b>Ega:</b> {CARD_NAME}\n\n"
        "<i>To'lov qilgach, chek rasmini shu chatga yuboring!</i>"
    )

    await callback.message.answer(caption, parse_mode="HTML")
    await callback.answer()


@dp.message(F.photo)
async def handle_receipt_photo(message: types.Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Mavjud emas"

    admin_text = (
        "<b>📥 YANGI TO'LOV CHEKI!</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"🔗 <b>Username:</b> {username}"
    )

    photo_id = message.photo[-1].file_id
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=admin_text,
        parse_mode="HTML",
    )

    await message.answer(
        "✅ Chek qabul qilindi! Tez orada administrator to'lovni tasdiqlaydi."
    )


@dp.message(F.document)
async def handle_receipt_document(message: types.Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Mavjud emas"

    admin_text = (
        "<b>📥 YANGI TO'LOV CHEKI (Fayl)!</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"🔗 <b>Username:</b> {username}"
    )

    await bot.send_document(
        chat_id=ADMIN_ID,
        document=message.document.file_id,
        caption=admin_text,
        parse_mode="HTML",
    )

    await message.answer(
        "✅ Chek fayli qabul qilindi! Administrator tez orada ko'rib chiqadi."
    )


async def main():
    while True:
        try:
            print("Bot ishga tushdi va ishlamoqda...")
            await dp.start_polling(bot, polling_timeout=30)
        except TelegramUnauthorizedError:
            print(
                "XATOLIK: Bot tokeni noto'g'ri. Iltimos, BotFather'dan yangi token oling!"
            )
            break
        except TelegramNetworkError:
            print("Tarmoq uzilishi. 5 soniyadan so'ng qayta ulanadi...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Xatolik: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
