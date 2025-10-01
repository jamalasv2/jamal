import asyncio
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping

from Jamal.core.helpers._client import PY
from Jamal.helpers.class_emoji import get_emo
from Jamal import ubot
from Jamal.config import SUDO
from Jamal bhs, get_bhs


@PY.UBOT("ping|p", sudo=True)
@ubot.on_message(filters.command(["ping"], "C") & filters.user(DEVS))
async def _(client, message):
    em = get_emo(client)
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping, 2)
    _ping = f"""
<BLOCKQUOTE><b>{ping}ᴘᴏɴɢ ~ </b> <code>{delta_ping} ms</code>
<b>{tion}ᴜsᴇʀ ~ </b> <b>{client.me.mention}</b></BLOCKQUOTE>
"""
    return await message.reply(_ping)


