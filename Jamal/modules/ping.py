import asyncio
from datetime import datetime
from time import time

from pyrogram import filters
from pyrogram.raw.functions import Ping

from Jamal.core.helpers._client import PY
from Jamal.helpers.class_emoji import get_emo
from Jamal import ubot, bot
from Jamal.config import SUDO
from langs import bhs, get_bhs


@PY.UBOT("ping|p", sudo=True)
@ubot.on_message(filters.command(["ping"], "C") & filters.user(SUDO))
async def _(client, message):
    em = get_emo(client)
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping, 2)
    return await message.reply(bhs("ping_text").format(em.ping, delta_ping, em.account, client.me.mention, em.ubot, bot.me.mention))


