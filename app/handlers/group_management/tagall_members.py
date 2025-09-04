from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus
from app import bot
from .auxiliary.pm_error import pm_error
from app.utils.database import MemoryDB

@bot.on_message(filters.command("tagall", ["/", "-", "!", "."]))
async def func_tagallusers(client, message: Message):
    user = message.from_user
    chat = message.chat

    if chat.type == ChatType.PRIVATE:
        await pm_error(chat.id)
        return
    
    user_info = await chat.get_member(user.id)
    if user_info.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await message.reply_text("You don't have enough permission to tag all chat members!")
        return
    
    await message.reply_text(f"Tagging all user started by: {user.mention}")
    
    # variables
    counter = 0
    text = ""

    MemoryDB.insert("data_center", chat.id, {"tagging_running": True})

    async for member in chat.get_members():
        chat_data = MemoryDB.data_center.get(chat.id)
        stop_tagging = chat_data.get("stop_tagging")
        if stop_tagging:
            MemoryDB.insert("data_center", chat.id, {"tagging_running": False, "stop_tagging": False})
            break

        if not member.user.is_bot and not member.user.is_deleted:
            text += f"{member.user.mention}\n"
            counter += 1

            if counter >= 10:
                await message.reply_text(text)
                text = ""
                counter = 0
    
    if text:
        await message.reply_text(text)
    
    MemoryDB.insert("data_center", chat.id, {"tagging_running": False})


@bot.on_message(filters.command("stoptagall", ["/", "-", "!", "."]))
async def func_tagallusers(client, message: Message):
    user = message.from_user
    chat = message.chat

    if chat.type == ChatType.PRIVATE:
        await pm_error(chat.id)
        return

    user_info = await chat.get_member(user.id)
    if user_info.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await message.reply_text("You don't have enough permission to stop tagging!")
        return
    
    chat_data = MemoryDB.data_center.get(chat.id)
    tagging_running = chat_data.get("tagging_running")

    if tagging_running:
        MemoryDB.insert("data_center", chat.id, {"stop_tagging": True})
    else:
        await message.reply_text("All user tagging isn't running.")
        return
    
    await message.reply_text(f"User tagging stopped by: {user.mention}")
