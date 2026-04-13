from pyrogram import Client, filters
import pyrogram.errors

# --- HOTFIX: PYROGRAM PATCH ---
if not hasattr(pyrogram.errors, 'GroupcallForbidden'):
    pyrogram.errors.GroupcallForbidden = getattr(pyrogram.errors, 'BroadcastForbidden', Exception)

from pytgcalls import PyTgCalls, idle
from pytgcalls.types import MediaStream
import yt_dlp

# --- GLOBAL QUEUE TRACKER ---
playlist = {}

# --- 1. CREDENTIALS ---
API_ID = 0 # Enter your API ID here
API_HASH = "" # Enter your API HASH here
BOT_TOKEN = "" # Enter your Bot Token here

# --- 2. DUAL-CLIENT ARCHITECTURE ---
bot_app = Client("liliya_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("liliya_user", api_id=API_ID, api_hash=API_HASH)
call_py = PyTgCalls(user_app)

# --- 3. TEST COMMAND ---
@bot_app.on_message(filters.command("ping"))
async def ping_test(client, message):
    await message.reply(f"The Innkeeper's Daughter is here! 🍻\n🔍 Group ID: `{message.chat.id}`")

# --- 4. THE MAGIC COMMAND (/PLAY) ---
@bot_app.on_message(filters.command("play"))
async def play_music(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a YouTube link! Example: `/play https://youtu...`")
        return
    
    url = message.command[1]
    status_message = await message.reply("🔍 The Innkeeper's Daughter is calling the bards... Preparing the notes!")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info.get('title', 'Unknown Song')

        chat_id = message.chat.id
        
        # Add to playlist logic
        if chat_id not in playlist:
            playlist[chat_id] = []
        playlist[chat_id].append({"url": audio_url, "title": title})

        # If nothing is playing, start now
        if len(playlist[chat_id]) == 1:
            await call_py.play(
                chat_id,
                MediaStream(audio_url, video_flags=MediaStream.Flags.IGNORE)
            )
            await status_message.edit_text(f"🎧 **Now Playing:** {title}\nThe Innkeeper's Daughter wishes you a Nat 20! 🎲")
        else:
            await status_message.edit_text(f"📝 **Added to Queue:** {title}\nPosition in line: {len(playlist[chat_id])-1}")

    except Exception as e:
        await status_message.edit_text(f"❌ The spell fizzled, the bard's string broke:\n`{str(e)}`")

# --- 5. PAUSE COMMAND (/pause) ---
@bot_app.on_message(filters.command("pause"))
async def pause_music(client, message):
    try:
        await call_py.pause(message.chat.id) 
        await message.reply("⏸️ The music has been paused.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

# --- 6. RESUME COMMAND (/resume) ---
@bot_app.on_message(filters.command("resume"))
async def resume_music(client, message):
    try:
        await call_py.resume(message.chat.id) 
        await message.reply("▶️ The music continues!")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

# --- 7. MUTE/UNMUTE COMMANDS ---
@bot_app.on_message(filters.command("mute"))
async def mute_bot(client, message):
    try:
        await call_py.mute(message.chat.id) 
        await message.reply("🔇 The bard is now silent.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

# --- 8. STOP COMMAND (/stop) ---
@bot_app.on_message(filters.command("stop"))
async def stop_music(client, message):
    try:
        playlist[message.chat.id] = [] # Clear the queue
        await call_py.leave_call(message.chat.id)
        await message.reply("⏹️ Show's over! The bards have left the building.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

# --- 9. SKIP COMMAND (/skip) ---
@bot_app.on_message(filters.command("skip"))
async def skip_music(client, message):
    chat_id = message.chat.id
    if chat_id not in playlist or len(playlist[chat_id]) <= 1:
        await message.reply("📭 No more songs in the queue to skip to!")
        return
    
    try:
        playlist[chat_id].pop(0) # Remove current song
        next_song = playlist[chat_id][0] # Get next song
        
        await call_py.play(
            chat_id,
            MediaStream(next_song['url'], video_flags=MediaStream.Flags.IGNORE)
        )
        await message.reply(f"⏭️ Skipped! Now playing: **{next_song['title']}**")
    except Exception as e:
        await message.reply(f"❌ Could not skip: `{e}`")

# System Run Loop (Keep this at the very bottom)
if __name__ == "__main__":
    print("The tavern doors are opening... Bot and Assistant are waking up.")
    bot_app.start()
    user_app.start() 
    call_py.start()
    print("Everything is ready! Nat 20 awaits!")
    idle()