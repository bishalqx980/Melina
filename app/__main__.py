import asyncio
from pyrogram import idle
from pyrogram.errors import FloodWait
from app import app, logger
from app.handlers import *
from config import CONFIG

async def app_init():
    logger.info("BOT STARTED...!")
    await app.send_message(CONFIG.OWNER_ID, "Bot Started!")
    await idle()


async def main():
    try:
        await app.start()
        await app_init()
    except FloodWait as e:
        logger.info(f"FloodWait: {e}")
        await asyncio.sleep(e.value)
        await main()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
