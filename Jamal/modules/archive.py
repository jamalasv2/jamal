import asyncio

from pyrogram.errors.exceptions import FloodWait
from pyrogram.enums import ChatType

from Jamal import *
from Jamal.core.helpers import PY, get_global_id
from langs import bhs, get_bhs

__MODULE__ = "archive"
__HELP__ = get_bhs("arsip_cmd")


@PY.UBOT("arsip")
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if len(message.command) < 2:
        return await msg.edit(bhs("arsip_ggl").format(em.gagal))

    done = 0
    command, query = message.command[:2]
    chats = await get_global_id(client, query)

    if query not in ["all", "bot", "channel", "group", "personal"]:
        return await msg.edit(bhs("arsip_ggl").format(em.gagal))

    for chat_id in chats:
        try:
            await client.archive_chats(chat_id)
            await msg.delete()
            return await message.reply(bhs("arsip_sukses").format(em.berhasil, em.total, len(chats), em.keterangan, query))
        except Exception as error:
            return await msg.edit(bhs("text_error").format(em.peringatan, error))


@PY.UBOT("unarsip")
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if len(message.command) < 2:
        return await msg.edit(bhs("arsip_ggl").format(em.gagal))

    done = 0
    command, query = message.command[:2]
    chats = await get_global_id(client, query)

    if query not in ["all", "bot", "channel", "personal"]:
        return await msg.edit(bhs("arsip_ggl").format(em.gagal))

    for chat_id in chats:
        try:
            await client.unarchive_chats(chat_id)
            await msg.delete()
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chats), em.keterangan, query))
        except Exception as error:
            return await msg.edit(bhs("text_error").format(em.gagal, error))
