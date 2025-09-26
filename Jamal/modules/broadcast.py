import asyncio

from gc import get_objects

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors.exceptions import FloodWait, UserDeactivated, UserIsBlocked

from Jamal.core import *
from Jamal.database import *
from Jamal.config import DEVS, BLACKLIST_CHAT
from Jamal import *


__MODULE__ = "broadcast"
__HELP__ = get_bhs("broadcast_cmd")


@PY.UBOT("gcast", sudo=True)
@ubot.on_message(filters.command(["gcast"], "C") & filters.user(DEVS))
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    text = get_message(message)

    if not text:
        return await msg.edit(bhs("broadcast_noteks").format(em.gagal))

    chat = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)
    done = 0
    fail = 0

    for chat_id in chat:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except FloodWait as e:
            await msg.edit(bhs("broadcast_flood").format(em.peringatan, e.value))
            await asyncio.sleep(e.value)
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except Exception as e:
            fail += 1
            pass
    await msg.delete()
    return await message.reply(bhs("broadcast_sukses").format(em.broadcast, em.berhasil, done, em.gagal, failed, em.keterangan, 'group'))


@PY.UBOT("gucast", sudo=True)
@ubot.on_message(filters.command(["gucast"], "C") & filters.user(DEVS))
async def _(client, message):
    em = get_emo(client)
    text = get_message(message)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if not text:
        return await msg.edit(bhs("broadcast_noteks").format(em.gagal))

    chat = await get_broadcast_id(client, "users")
    blacklist = await get_list_from_vars(client.me.id, "BLUCAST", "DB_UCAST")
    done = 0
    fail = 0

    for chat_id in chat:
        if chat_id in blacklist or chat_id == DEVS or chat_id == client.me.id:
            continue
        try:
            await (text.copy(chat_id, text) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except FloodWait as e:
            await msg.edit(bhs("broadcast_flood").format(em.peringatan, e.value))
            await asyncio.sleep(e.value)
            await (text.copy(chat_id, text) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except Exception:
            fail += 1
            pass
    await msg.delete()
    return await message.reply(bhs("broadcast_sukses").format(em.broadcast, em.berhasil, done, em.gagal, failed, em.keterangan, 'users'))


@PY.BOT("broadcast")
@PY.OWNER
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    send = get_message(message)
    if not send:
        return await msg.edit(bhs("broadcast_noteks").format(em.gagal))
    susers = await get_list_from_vars(client.me.id, "SAVED_USERS")
    done = 0
    failed = 0
    deleted = 0
    blocked = 0
    for chat_id in susers:
        try:
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except UserDeactivated:
            await remove_from_vars(bot.me.id, "SAVED_USERS", chat_id)
            deleted += 1
        except UserIsBlocked:
            blocked += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except Exception:
            pass
            failed += 1
        except Exception as e:
            await msg.delete()
            return await message.reply(f"ERROR:\n<blockquote>{e}</blockquote>")
    stat = f"<blockquote>Ω pesan siaran terkirim\n√ berhasil: {done}\n🧟 akun terhapus: {deleted}\n🚫 bot diblokir: {blocked}\n❌ gagal: {failed}</blockquote>"
    await msg.delete()
    return await message.reply(stat)
            
