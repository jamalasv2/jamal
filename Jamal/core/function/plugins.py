from importlib import import_module

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from PyroUbot import bot
from PyroUbot.config import SUPPORT, OWNER_ID
from PyroUbot.core.helpers import PY
from PyroUbot.modules import loadModule
from PyroUbot.core.database import *

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"PyroUbot.modules.{mod}")
        module_name = getattr(imported_module, "__MODULE__", "").replace(" ", "_").lower()
        if module_name:
            HELP_COMMANDS[module_name] = imported_module
    print(f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]")


@PY.CALLBACK("0_cls")
async def _(client, callback_query):
    await callback_query.message.delete()
