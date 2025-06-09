import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from app import app
from config import CONFIG

@app.on_message(filters.command("log", ["/", "-", "!", "."]))
async def func_log(client: Client, message: Message):
    user = message.from_user
    chat = message.chat

    if user.id != CONFIG.OWNER_ID:
        await message.reply_text("Access Denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await message.reply_text("This command is made for private chat!")
        await asyncio.sleep(3)
        await sent_message.delete()
        try:
            await message.delete()
        except:
            pass
        return
    
    await message.reply_document(open("sys/log.txt", "rb"), file_name="log.txt")
