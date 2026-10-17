import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPurl
import yt_dlp

API_ID = int(os.getenv("API_ID", "34006000"))
API_HASH = os.getenv("API_HASH", "4450b56f158c1c3529520d35ffe30522")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8661256440:AAETek4kGNRfULuVuZoB6gU1Dm_ouo7uZDg")
STRING_SESSION = os.getenv("STRING_SESSION")

# Assistant Client jo VC join karega
app = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call_py = PyTgCalls(app)

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
            stream_url = info['url']
            title = info.get('title', 'Audio')

        await call_py.join_group_call(
            message.chat.id,
            AudioPurl(stream_url)
        )
        await m.edit_text(f"▶️ Playing **{title}** in Voice Chat!")
    except Exception as e:
        await m.edit_text(f"❌ Error: {e}")

async def main():
    await app.start()
    await call_py.start()
    print("Voice Chat Bot Start Ho Gaya Hai!")
    import asyncio
    await asyncio.gather()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
  
