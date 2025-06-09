from app import app
from app.helpers import BuildKeyboard

async def pm_error(chat_id):
    """`chat_id` where you want to send this message"""
    bot = await app.get_me()
    btn = BuildKeyboard.ubutton([{"Add me ➕": f"https://t.me/{bot.username}?startgroup=help"}])
    await app.send_message(chat_id, "This command is made to be used in group chats, not in pm!", reply_markup=btn)
