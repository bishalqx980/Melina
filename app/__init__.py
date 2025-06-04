from time import time
from pyrogram import Client, __version__ as __pyroVersion__
from .logger import setup_logging
from config import CONFIG

# constants
__version__ = "2.0.0.2" # major.minor.patch.commits
BOT_UPTIME = time()

# logger
logger = setup_logging()

# Main Client function
app = Client(
    name="Melina_2.0",
    api_id=CONFIG.API_ID,
    api_hash=CONFIG.API_HASH,
    bot_token=CONFIG.BOT_TOKEN,
    workdir="sys"
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
