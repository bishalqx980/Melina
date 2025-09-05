import json
from time import time
from datetime import timedelta

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from app import bot, logger
from app.modules import RESITA
from app.modules.utils import Utils
from app.helpers import BuildKeyboard
from app.utils.database import MemoryDB, DBConstants

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

@bot.on_message(filters.command("download", ["/", "-", "!", "."]))
async def func_downloader(_, message: Message):
    user = message.from_user

    for p in ["/", "-", "!", "."]:
        if message.text.startswith(p):
            link = message.text.removeprefix(f"{p}{message.command[0]}").strip()
            break
    
    if not link:
        await message.reply_text(f"Example: `-{message.command[0]} link`")
        return
    
    with open("app/handlers/downloaders.json", "r") as f:
        downloaders = json.load(f)
    
    BUTTONS = []
    
    for downloaderType in downloaders:
        counter = 0
        temp = {}
        allkeyboardData = downloaders[downloaderType]

        for keyboardName in allkeyboardData:
            keyboardData = allkeyboardData[keyboardName]
            temp.update({keyboardName: keyboardData["data"]})
            counter += 1

            if counter >= 4:
                BUTTONS.append(temp)
                temp = {}
                counter = 0
        
        BUTTONS.append(temp)
    
    btn = BuildKeyboard.cbutton(BUTTONS)
    await message.reply_text(
        f"**Link:** `{link}`\n\n"
        "*Choose which one you want to download!*",
        reply_markup=btn
    )

    MemoryDB.insert(DBConstants.DATA_CENTER, user.id, {"link": link})


@bot.on_callback_query(filters.regex(r"download_*"))
async def func_start_download(_, query: CallbackQuery):
    message = query.message
    user = query.from_user
    query_data = query.data.removeprefix("download_")

    await message.delete()

    user_data = MemoryDB.data_center.get(user.id)
    if not user_data:
        try:
            await message.delete()
        except:
            pass
        return
    
    link = user_data.get("link")
    if not link:
        await message.reply_text("Something went wrong! Link wasn't found!")
        return
    
    sent_message = await message.reply_text("Please wait! Downloading...")

    res = await RESITA.sendGetReq(f"/downloader/{query_data}", {"link": link})
    if not res:
        return
    
    if res["status"] != 200:
        await sent_message.edit_text(res.get(message) or "Something went wrong!")
        return
    
    await sent_message.edit_text("Uploading...")

    result_data = {
        "ytmp3": {
            "title": res.get("data", {}).get("title", ""),
            "thumbnail": res.get("data", {}).get("thumbnail", ""),
            "size": res.get("data", {}).get("size", ""),
            "duration": res.get("data", {}).get("duration", ""),
            "link": res.get("data", {}).get("dlink", "")
        },
        "applemusic": {
            "title": res.get("result", {}).get("name", ""),
            "thumbnail": res.get("result", {}).get("thumb", ""),
            "size": 0,
            "duration": res.get("result", {}).get("duration", ""),
            "link": res.get("result", {}).get("dlink", "")
        },
        "soundcloud": {
            "title": res.get("result", {}).get("title", ""),
            "thumbnail": res.get("result", {}).get("thumbnail", ""),
            "size": 0,
            "duration": "~",
            "link": res.get("result", {}).get("downloadUrl", "")
        },
        "spotify": {
            "title": res.get("data", {}).get("title", ""),
            "thumbnail": res.get("result", {}).get("thumbnail", ""),
            "size": 0,
            "duration": "~",
            "link": res.get("result", {}).get("download", "")
        }
    }

    content_info = result_data[query_data]

    audio = content_info["link"]
    title = content_info["title"]
    thumb = content_info["thumbnail"]
    size = f"{int(content_info["size"]) / 1024 / 1024}MB"
    duration = content_info["duration"]

    caption = (
        f"**Name:** `{title}`\n"
        f"**Size:** `{size}`\n"
        f"**Duration:** `{duration}`"
    )

    startTime = time()
    await sent_message.reply_audio(
        audio,
        caption=caption,
        title=title,
        thumb=thumb,
        progress=progress,
        progress_args=[sent_message, "Uploading...", startTime]
    )

    await sent_message.edit_text("Upload completed!")
