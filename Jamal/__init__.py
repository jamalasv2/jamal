import uvloop

uvloop.install()

import logging
import os
import re
import sys
import asyncio

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyromod import listen
from rich.logging import RichHandler
from pytgcalls import GroupCallFactory

from Jamal.config import API_ID, API_HASH, BOT_TOKEN


# ========== Logging Handler ==========
class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for error_type in ["OSErro", "TimeoutError"]:
            if error_type in record.getMessage():
                os.execl(sys.executable, sys.executable, "-m", "Jamal")


logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler(), ConnectionHandler()],
)

logger = logging.getLogger(__name__)

# aiohttp global session
aiosession = ClientSession()


# ========== Bot Utama ==========
class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="ʜɪɢᴀɴʙᴀɴᴀ ᴘʀᴇᴍɪᴜᴍ")

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func
        return decorator


# ========== Userbot (multi client) ==========
class Ubot(Client):
    _ubot = []
    _prefix = {}
    _get_my_id = []
    _translate = {}
    _get_my_peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="ʜɪɢᴀɴʙᴀɴᴀ ᴘʀᴇᴍɪᴜᴍ")
        self.group_call = GroupCallFactory(self).get_file_group_call()

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    def cmd_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = await self.get_prefix(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix):]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True
                return False

        return filters.create(func)

    async def start(self):
        await super().start()
        self._prefix[self.me.id] = ["."]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = "id"
        print(f"[𝐈𝐍𝐅𝐎] - ({self.me.id}) - 𝐒𝐓𝐀𝐑𝐓𝐄𝐃")


# ========== Inisialisasi Instance ==========
bot = Bot(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

ubot = Ubot(name="ubot")


# Import helper, database, dll setelah client siap
from Jamal.database import *
from Jamal.core.function import *
from Jamal.core.helpers import *