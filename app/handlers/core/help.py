from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from app import bot
from app.helpers import BuildKeyboard

class HelpMenuData:
    TEXT = (
        "<blockquote>Help Menu</blockquote>\n\n"
        "• /id - See user/chat ID\n"
        "• /info - See user info\n"
        "• /tagall - Tag all chat members\n"
        "• /stoptagall - Stop tagging chat members\n"
        "• /log - [debug] (owner only)\n"
    )

    BUTTONS = [{"Close ✖️": "help_close"}]


@bot.on_message(filters.command("help", ["/", "-", "!", "."]))
async def func_help(client, message: Message):
    keyboard = BuildKeyboard.cbutton(HelpMenuData.BUTTONS)
    await message.reply_text(HelpMenuData.TEXT, reply_markup=keyboard)
