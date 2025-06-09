from pyrogram import Client, filters
from pyrogram.types import Message
from app import app

@app.on_message(filters.command("id", ["/", "-", "!", "."]))
async def func_id(client: Client, message: Message):
    user = message.from_user
    chat = message.chat
    reply = message.reply_to_message
    replied_user = reply.from_user if reply else None
    
    text = (
        f"• {chat.title}\n"
        f"  » ID: `{chat.id}`\n\n"

        f"• {user.full_name}\n"
        f"   » ID: `{user.id}`\n\n"
    )

    if replied_user:
        text += (
            f"• {replied_user.full_name}\n"
            f"   » ID: `{replied_user.id}`"
        )
    
    await message.reply_text(text)
