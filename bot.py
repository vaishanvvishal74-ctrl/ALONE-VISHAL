import os
import asyncio
from aiohttp import web

# Python 3.14 event loop fix
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID", "34006000"))
API_HASH = os.getenv("API_HASH", "4450b56f158c1c3529520d35ffe30522"))
BOT_TOKEN = os.getenv("BOT_TOKEN", "8661256440:AAETek4kGNRfULuVuZoB6gU1Dm_ouo7uZDg")

app = Client(
    "test_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Web server to keep Render live
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    web_app = web.Application()
    web_app.router.add_get("/", handle)
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server running on port {port}")

# Simple ping-pong command
@app.on_message(filters.command("ping"))
async def ping_cmd(client, message):
    await message.reply_text("🏓 Pong! Bot is working perfectly!")

async def main():
    await start_web_server()
    await app.start()
    print("Test Bot Live Ho Gaya Hai!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
