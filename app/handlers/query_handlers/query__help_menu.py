from pyrogram import filters
from pyrogram.types import CallbackQuery
from app import bot
from app.helpers import BuildKeyboard

@bot.on_callback_query(filters.regex("help_[A-Za-z0-9]+"))
async def helpmenu_query_handler(client, query: CallbackQuery):
    query_data = query.data.removeprefix("help_")

    if query_data == "menu":
        pass

    elif query_data == "close":
        await query.message.delete()
        return
    
    # keyboard = BuildKeyboard.cbutton(keyboard_data)
    
    # await query.edit_message_text(text, reply_markup=keyboard)
