from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from app import app
from app.helpers import BuildKeyboard

@app.on_callback_query(filters.regex("help_[A-Za-z0-9]+"))
async def helpmenu_query_handler(client: Client, query: CallbackQuery):
    query_data = query.data.removeprefix("help_")

    if query_data == "menu":
        text = (
            "<blockquote>Help Menu</blockquote>\n\n"
            "• /id - Show user/chat ID\n"
            "• /tagall - Tag all chat members\n"
            "• /stoptagall - Stop tagging chat members\n"
            "• /log - [debug] (owner only)\n"
        )

        keyboard_data = [{"Close ✖️": "help_close"}]

    elif query_data == "close":
        await query.message.delete()
        return
    
    keyboard = BuildKeyboard.cbutton(keyboard_data)
    
    await query.edit_message_text(text, reply_markup=keyboard)
