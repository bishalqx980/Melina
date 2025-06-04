from pyrogram import Client, filters
from pyrogram.types import Message
from app import app

@app.on_message(filters.command("id", ["/", "-", "!", "."]))
async def func_id(client: Client, message: Message):
    user = message.from_user
    chat = message.chat

    text = (
        f"ChatID: `{chat.id}`\n"
        f"UserID: `{user.id}`"
    )
    
    await message.reply_text(text)
