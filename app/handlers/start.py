from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from app import app
from app.helpers import BuildKeyboard
from app.modules.database import MemoryDB, MongoDB

@app.on_message(filters.command("start", ["/", "-", "!", "."]))
async def func_start(client: Client, message: Message):
    user = message.from_user
    chat = message.chat

    sent_message = await message.reply_text("⌛")
    # getting bot
    bot = await app.get_me()

    # database entry
    if chat.type != ChatType.PRIVATE:
        chat_data = MemoryDB.chats_data.get(chat.id)
        if not chat_data:
            chat_data = MongoDB.find_one("chats_data", "chat_id", chat.id)
            if not chat_data:
                chat_data = {
                    "chat_id": chat.id,
                    "title": chat.title
                }

                MongoDB.insert("chats_data", chat_data)
            MemoryDB.insert("chats_data", "chat_id", chat_data)
        
        keyboard = [{"Start in PM 😉": f"https://t.me/{bot.username}?start=start"}]
        
        await sent_message.edit_text("Hey, please start me in PM to chat with me 😊!", reply_markup=keyboard)
    else:
        user_data = MemoryDB.users_data.get(user.id)
        if not user_data:
            user_data = MongoDB.find_one("users_data", "user_id", user.id)
            if not user_data:
                user_data = {
                    "user_id": user.id,
                    "name": user.first_name
                }

                MongoDB.insert("users_data", user_data)
            MemoryDB.insert("users_data", "user_id", user_data)

    # for private chat [PM]
    text = (
        f"Hi 👋, myself {bot.first_name} 🥰!\n"
        f"Nice to meet you, {user.first_name}\n\n"

        "I'm just a simple bot with some cool features 😊."
    )

    keyboard_data = [
        {"Help Menu 🐳": "help_menu", "Add me ➕": f"https://t.me/{bot.username}?startgroup=help"},
        {"Developer 🧑‍💻": "https://t.me/bishalqx680/22", "Source Code 📝": "https://github.com/bishalqx980/Melina"},
        {"Close ✖️": "help_close"}
    ]

    keyboard = BuildKeyboard.cbutton(keyboard_data)

    await sent_message.edit_text(text, reply_markup=keyboard)
