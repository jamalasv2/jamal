from importlib import import_module

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Jamal import bot
from Jamal.config import SUPPORT, OWNER_ID
from Jamal.core.helpers import PY
from Jamal.modules import loadModule
from Jamal.database import *

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"Jamal.modules.{mod}")
        module_name = getattr(imported_module, "__MODULE__", "").replace(" ", "_").lower()
        if module_name:
            HELP_COMMANDS[module_name] = imported_module
    print(f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]")


@PY.CALLBACK("0_cls")
async def _(client, callback_query):
    await callback_query.message.delete()
