from time import time
from datetime import timedelta

from pyrogram import filters
from pyrogram.types import Message

from app import bot, logger
from app.modules import RESITA
from app.modules.utils import Utils

async def progress(current, total, message: Message, message_text="", startTime=None):
    """
    :param current: Bytes transferred so far
    :param total: Total bytes
    :param message: Message class
    :param message_text: info text (e.g. "Downloading" or "Uploading")
    :param startTime: Progress start timestamp (time.time())
    """
    try:
        if startTime is None:
            startTime = time()
        
        percent = current * 100 / total
        elapsedTime = time() - startTime
        elapsed = timedelta(seconds=int(elapsedTime))

        # Speed in MB/s (bytes -> MB)
        currentSpeed = current / elapsedTime / (1024 * 1024)

        # Remaining time
        remainingSeconds = (total - current) / (currentSpeed * 1024 * 1024)
        remaining = timedelta(seconds=int(remainingSeconds))

        text = (
            f"**{message_text}**\n"
            f"**Speed:** `{currentSpeed:.2f}MB/s`\n"
            f"**Elapsed:** `{elapsed}`\n"
            f"**ETA:** `{remaining}`\n"
            f"**Progress:** `{Utils.createProgressBar(int(percent))}` `{percent:.2f}%`"
        )

        await message.edit_text(text)
    except Exception as e:
        logger.error(e)

@bot.on_message(filters.command("ytdl", ["/", "-", "!", "."]))
async def func_ytdl(_, message: Message):
    for p in ["/", "-", "!", "."]:
        if message.text.startswith(p):
            link = message.text.removeprefix(f"{p}{message.command[0]}").strip()
            break
    
    if not link:
        await message.reply_text("Example: `-ytdl link`")
        return
    
    sent_message = await message.reply_text("Please wait!")
    
    res = await RESITA.sendGetReq("/downloader/ytmp3", {"link": link})
    if not res:
        await sent_message.edit_text("Something went Wrong!")
        return
    
    await sent_message.edit_text("Uploading...")

    audio = res["data"]["dlink"]
    title = res["data"]["title"]
    thumb = res["data"]["thumbnail"]
    size = f"{int(res['data']['size']) / 1024 / 1024}MB"

    startTime = time()
    await sent_message.reply_audio(
        res["data"]["dlink"],
        caption=title,
        title=title,
        thumb=thumb,
        progress=progress,
        progress_args=[sent_message, "Uploading...", startTime]
    )

    await sent_message.edit_text("Upload completed!")
