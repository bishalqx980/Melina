from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from app import app
from app.helpers import BuildKeyboard

@app.on_message(filters.command("info", ["/", "-", "!", "."]))
async def func_info(client, message: Message):
    user = message.from_user
    reply = message.reply_to_message
    replied_user = reply.from_user if reply else None
    args = " ".join(message.command[1:])

    victim = None # get info of
    fetch_info = False

    if not replied_user and not args:
        victim = user
    else:
        if args: fetch_info = True
        victim = args or replied_user
    
    if fetch_info:
        user_info = await app.get_users(victim)
    else:
        user_info = victim

    async for photo in app.get_chat_photos(user_info.id, 1):
        photo = photo.file_id or None
    
    text = (
        f"• Name: {user_info.full_name}\n"
        f"  - First: {user_info.first_name}\n"
        f"  - Last: {user_info.last_name}\n"
        f"• Username: @{user_info.username or "username"}\n"
        f"• ID: `{user_info.id}`\n"
        f"• DC: `{user_info.dc_id}`\n"
        f"• Lang: {user_info.language_code}"
    )

    if photo:
        await message.reply_photo(photo, caption=text)
    else:
        await message.reply_text(text)
