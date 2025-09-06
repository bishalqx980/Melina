import json
from time import time

from pyrogram import Client, __version__ as __pyroVersion__
from pyrogram.types import LinkPreviewOptions
from pyrogram.enums import ClientPlatform

from .utils.logger import setup_logging
from config import CONFIG

# constants
__version__ = json.load(open("version.json", "rb"))["__version__"] # major.minor.patch.commits
BOT_UPTIME = time()

# logger
logger = setup_logging()

# Main Client function
bot = Client(
    name="Melina_2.0",
    api_id=CONFIG.API_ID,
    api_hash=CONFIG.API_HASH,
    app_version=f"{__pyroVersion__} x64",
    device_model="Desktop",
    system_version="Windows 11 x64",
    bot_token=CONFIG.BOT_TOKEN,
    workdir="sys",
    client_platform=ClientPlatform.DESKTOP,
    link_preview_options=LinkPreviewOptions(is_disabled=True)
)

logger.info(f"""
Developed by
 ______     __     ______     __  __     ______     __        
/\  == \   /\ \   /\  ___\   /\ \_\ \   /\  __ \   /\ \       
\ \  __<   \ \ \  \ \___  \  \ \  __ \  \ \  __ \  \ \ \____  
 \ \_____\  \ \_\  \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/ 
   
    Version: {__version__}
    Library: kurigram {__pyroVersion__}
    GitHub: https://github.com/bishalqx980
""")
