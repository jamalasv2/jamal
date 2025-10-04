import asyncio

from pyrogram.errors.exceptions import FloodWait
from pyrogram.enums import ChatType

from Jamal import *
from Jamal.core.helpers import PY, get_global_id, extract_type_and_msg
from langs import bhs, get_bhs

__MODULE__ = "archive"
__HELP__ = get_bhs("arsip_cmd")


@PY.UBOT("arsip")
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    command, query = message.command[:2]

    chats = await get_global_id(client, query)
    done = 0

    if query not in ["all", "bot", "channel", "group", "personal"]:
        return await msg.edit(bhs("arsip_ggl").format(em.gagal))

    for chat_id in chats:
        try:
            await client.archive_chats(chat_id)
            await msg.delete()
            return await message.reply(bhs("arsip_sukses").format(em.berhasil, em.total, len(chats), em.keterangan, command))
        except Exception as error:
            return await msg.edit(bhs("text_error").format(em.peringatan, error))


@PY.UBOT("unarsip")
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if len(message.command) < 2:
        return await msg.edit(bhs("arsip_ggl").format(em.gagal))

    command, query = message.command[:2]
    chat = await get_global_id(client, query)
    done = 0

    if query.lower() == "all":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'all'))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'all'))
        except Exception as e:
            return await msg.edit(bhs("text_error").format(em.gagal, e))
    elif query.lower() == "gc":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'group'))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'group'))
        except Exception as e:
            return await msg.edit(bhs("text_error").format(em.gagal, e))
    elif query.lower() == "pc":
        try:
            await client.unarchive_chats(chat)
            done += 1
            await msg.delete()
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'personal'))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'personal'))
        except Exception as e:
            return await msg.edit(bhs("text_error").format(em.gagal, e))
    elif query.lower() == "bot":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'bot'))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            done += 1
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'bot'))
        except Exception as e:
            return await msg.edit(bhs("text_error").format(em.gagal, e))
    elif query.lower() == "ch":
        try:
            await client.unarchive_chats(chat)
            done += 1
            await msg.delete()
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'channel'))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(bhs("arsip_out").format(em.berhasil, em.total, len(chat), em.keterangan, 'channel'))
        except Exception as e:
            return await msg.edit(bhs("text_error").format(em.gagal, e))
