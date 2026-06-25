import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
N8N_URL = "https://n8n-production-8399.up.railway.app/webhook/crypto-news"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📰 Новости")],
        [KeyboardButton(text="💰 Цены"), KeyboardButton(text="🔥 Топ движений")],
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Выбери что тебя интересует:",
        reply_markup=keyboard
    )

@router.message(lambda m: m.text == "📰 Новости")
async def cmd_news(message: Message):
    await message.answer("⏳ Собираю крипто-дайджест...")
    async with aiohttp.ClientSession() as session:
        async with session.post(N8N_URL, json={"type": "news"}) as resp:
            digest = await resp.text()
    await message.answer(f"📰 *Крипто-дайджест*\n\n{digest}", parse_mode="Markdown")

@router.message(lambda m: m.text == "💰 Цены")
async def cmd_prices(message: Message):
    await message.answer("⏳ Получаю цены...")
    async with aiohttp.ClientSession() as session:
        async with session.post(N8N_URL, json={"type": "prices"}) as resp:
            prices = await resp.text()
    await message.answer(f"💰 *Цены*\n\n{prices}", parse_mode="Markdown")

@router.message(lambda m: m.text == "🔥 Топ движений")
async def cmd_top(message: Message):
    await message.answer("⏳ Ищу топ движений...")
    async with aiohttp.ClientSession() as session:
        async with session.post(N8N_URL, json={"type": "top"}) as resp:
            top = await resp.text()
    await message.answer(f"🔥 *Топ движений*\n\n{top}", parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
