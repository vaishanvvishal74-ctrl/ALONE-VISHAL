import os
import asyncio
from aiohttp import web

# Python 3.14 event loop fix
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
import yt_dlp

API_ID = int(os.getenv("API_ID", "34006000"))
API_HASH = os.getenv("API_HASH", "4450b56f158c1c3529520d35ffe30522")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8661256440:AAETek4kGNRfULuVuZoB6gU1Dm_ouo7uZDg")

# Sirf Bot Token se Client start hoga (Koi String Session ki zaroorat nahi)
app = Client(
    "my_bot",
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

@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Kripya gaane ka naam likhein! Jaise: `/play Nazm Nazm`")
        return
    
    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 Searching for **{query}**...")

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'default_search': 'ytsearch',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get('title', 'Audio')

        await m.edit_text(f"▶️ **Song Found:** {title}\n✅ Bot is working!")
    except Exception as e:
        await m.edit_text(f"❌ Error: {e}")

async def main():
    await start_web_server()
    await app.start()
    print("Bot Safalta Purvak Live Ho Gaya Hai!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
