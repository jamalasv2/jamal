from time import time

from Jamal import *
from Jamal.core.helpers._client import PY
from langs import bhs, get_bhs


__MODULE__ = "afk"
__HELP__ = get_bhs("filters_cmd")


@PY.UBOT("afk")
async def _(client, message):
    reason = get_arg(message)
    db_afk = {"time": time(), "reason": reason}
    em = get_emo(client)
    tks = reason if reason else "—"
    teks = bhs("filters_afk").format(em.afk, em.keterangan, tks)
    await set_vars(client.me.id, "AFK", db_afk)
    return await message.reply(msg_afk)



@PY.AFK()
async def _(client, message):
    em = get_emo(client)
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        text = bhs("filters_afkaktif").format(em.afk, em.menunggu, afk_runtime, em.keterangan, afk_reason)
        return await message.reply(text)


@PY.UBOT("unafk")
async def _(client, message):
    em = get_emo(client)
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_runtime = await get_time(time() - afk_time)
        teks = bhs("filters_unafk").format(em.afk, em.menunggu, em.keterangan, afk_runtime)
        await message.reply(text)
        return await remove_vars(client.me.id, "AFK")
