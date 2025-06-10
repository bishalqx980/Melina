import os
import asyncio
from pyrogram import idle
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats
from app import app, logger
from config import CONFIG

def load_handlers():
    handlers_dir = "app/handlers"
    for root, dirs, files in os.walk(handlers_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                rel_path = os.path.relpath(root, handlers_dir)
                if rel_path == ".":
                    module_path = f"app.handlers.{filename[:-3]}"
                else:
                    rel_module_path = rel_path.replace(os.sep, ".")
                    module_path = f"app.handlers.{rel_module_path}.{filename[:-3]}"
                __import__(module_path)


async def app_init():
    try:
        await app.delete_bot_commands()
        await app.set_bot_commands([
            BotCommand("start", "start the bot"),
            BotCommand("help", "bot help menu")
        ], BotCommandScopeAllPrivateChats())
    except Exception as e:
        logger.error(e)

    try:
        await app.send_message(CONFIG.OWNER_ID, "Bot Started!")
    except Exception as e:
        logger.error(e)
    
    logger.info("BOT STARTED...!")
    await idle()


async def main():
    # Need to load before app.run()
    load_handlers()

    try:
        await app.start()
        await app_init()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
