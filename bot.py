import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = os.environ.get("BOT_TOKEN")
N8N_URL = "https://n8n-production-8399.up.railway.app/webhook/crypto-news"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Напиши /news для крипто-дайджеста")

@router.message(Command("news"))
async def cmd_news(message: Message):
    await message.answer("⏳ Собираю крипто-дайджест...")
    async with aiohttp.ClientSession() as session:
        async with session.post(N8N_URL, json={"chat_id": message.chat.id}) as resp:
            digest = await resp.text()
    await message.answer(f"📰 *Крипто-дайджест*\n\n{digest}", parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())