# Copyright (c) 2026 khithlainhtet
# Licensed under the MIT License.
# This file is part of PANDA

import time
import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

__version__ = "3.0.1"

# ၂။ Config နဲ့ Directory Setup
from config import Config
config = Config()
config.check()
tasks = []
boot = time.time()

from PANDA.core.dir import ensure_dirs
ensure_dirs()

from PANDA.core.mongo import MongoDB
db = MongoDB()

from PANDA.core.bot import Bot
app = Bot()

from PANDA.core.lang import Language
lang = Language()

from PANDA.core.telegram import Telegram
from PANDA.core.youtube import YouTube
tg = Telegram()
yt = YouTube()

from PANDA.helpers import Queue
queue = Queue()

from PANDA.core.calls import TgCall
anon = TgCall()

from PANDA.core.userbot import Userbot
userbot = Userbot()

async def stop() -> None:
    logger.info("Stopping...")
    for task in tasks:
        task.cancel()
        try:
            await task
        except:
            pass

    await app.exit()
    await userbot.exit()
    
    try:
        await db.close()
    except:
        pass

    logger.info("Stopped.\n")
