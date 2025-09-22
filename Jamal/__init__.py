import uvloop
uvloop.install()

import logging
import os
import re
import sys

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pyromod import listen
from pytgcalls import GroupCallFactory
from Jamal.config import *

# Simple reconnect handler (ke-paranoidan kamu sebelumnya)
class ConnectionHandler(logging.Handler):
    def emit(self, record):
        msg = record.getMessage()
        for error_type in ("OSErro", "TimeoutError"):
            if error_type in msg:
                os.execl(sys.executable, sys.executable, "-m", "PyroUbot")

logging.basicConfig(
    level=logging.ERROR,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[ConnectionHandler()],
)

console = logging.StreamHandler()
console.setLevel(logging.ERROR)
console.setFormatter(
    logging.Formatter("%(filename)s:%(lineno)s %(levelname)s: %(message)s")
)
logging.getLogger("").addHandler(console)

aiosession = ClientSession()


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


class Ubot(Client):
    # shared containers for multi-client
    _ubot = []
    _prefix = {}
    _get_my_id = []
    _translate = {}
    _get_my_peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="ʜɪɢᴀɴʙᴀɴᴀ ᴘʀᴇᴍɪᴜᴍ")
        try:
            self.group_call = GroupCallFactory(self).get_file_group_call()
        except Exception:
            self.group_call = None

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            # attach handler to all running ubots for consistent behavior
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["." ])

    def cmd_prefix(self, cmd):
        command_re = re.compile(r'([\"\\\'])(.*?)(?<!\\)\1|(\S+)')

        async def func(_, client, message):
            if not message.text:
                return False
            text = message.text.strip()
            username = client.me.username or ""
            prefixes = await self.get_prefix(client.me.id)
            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue
                without_prefix = text[len(prefix):]
                for command in cmd.split("|"):
                    if not re.match(rf'^(?:{command}(?:@?{username})?)(?:\s|$)', without_prefix, flags=re.IGNORECASE|re.UNICODE):
                        continue
                    without_command = re.sub(
                        rf'{command}(?:@?{username})?\s?', '', without_prefix, count=1, flags=re.IGNORECASE|re.UNICODE
                    )
                    message.command = [command] + [
                        re.sub(r'\\([\"\\\'])', r'\1', m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]
                    return True
            return False

        return filters.create(func)

    async def start(self):
        await super().start()
        # try to get prefix from database helper if present
        try:
            from Jamal.database import get_pref
            handler = await get_pref(self.me.id)
        except Exception:
            handler = None
        self._prefix[self.me.id] = handler if handler else ["."]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = "id"
        print(f"[INFO] - ({self.me.id}) - STARTED")


# main bot (bot account) - keep token login as before
bot = Bot(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ubot placeholder; actual ubots are loaded from DB in __main__.py
ubot = None

# convenience imports (your project's modules)
from Jamal.database import *
from Jamal.core.function import *
from Jamal.core.helpers import *