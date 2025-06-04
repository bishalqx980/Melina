from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from pyrogram.enums import ParseMode
from app import app
from app.helpers import BuildKeyboard

@app.on_callback_query(filters.regex("help_[A-Za-z0-9]+"))
async def helpmenu_query_handler(client: Client, query: CallbackQuery):
    user = query.from_user
    query_data = query.data.removeprefix("help_")

    if query_data == "start":
        bot = await app.get_me()

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

    elif query_data == "menu":
        text = (
            "<blockquote>Help Menu</blockquote>\n\n"
            "• /id - Show user/chat ID"
        )

        keyboard_data = [{"🔙 Back": "help_start", "Close ✖️": "help_close"}]

    elif query_data == "close":
        await query.message.delete()
        return
    
    keyboard = BuildKeyboard.cbutton(keyboard_data)
    
    await query.edit_message_text(text, reply_markup=keyboard)
