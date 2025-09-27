import asyncio

from gc import get_objects

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors.exceptions import FloodWait, UserDeactivated, UserIsBlocked

from Jamal.core import *
from Jamal.database import *
from Jamal.config import DEVS, BLACKLIST_CHAT
from Jamal import *

from langs import bhs, get_bhs


__MODULE__ = "broadcast"
__HELP__ = get_bhs("broadcast_cmd")


@PY.UBOT("gcast", sudo=True)
@ubot.on_message(filters.command(["gcast"], "C") & filters.user(DEVS))
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    text = get_message(message)

    if not text:
        return await msg.edit(bhs("broadcast_noteks").format(em.gagal))

    chat = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)
    done = 0
    failed = 0

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
            failed += 1
            pass
    await msg.delete()
    return await message.reply(bhs("broadcast_sukses").format(em.broadcast, em.berhasil, done, em.gagal, failed, em.keterangan, 'group'))


@PY.UBOT("gucast", sudo=True)
@ubot.on_message(filters.command(["gucast"], "C") & filters.user(DEVS))
async def _(client, message):
    em = await get_emo(client)
    text = get_message(message)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if not text:
        return await msg.edit(bhs("broadcast_noteks").format(em.gagal))

    chat = await get_broadcast_id(client, "users")
    blacklist = await get_list_from_vars(client.me.id, "BLUCAST", "DB_UCAST")
    done = 0
    failed = 0

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
            failed += 1
            pass
    await msg.delete()
    return await message.reply(bhs("broadcast_sukses").format(em.broadcast, em.berhasil, done, em.gagal, failed, em.keterangan, 'users'))


@PY.BOT("broadcast")
@PY.OWNER
async def _(client, message):
    em = await get_emo(client)
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
            

@PY.UBOT("addbl", sudo=True)
@ubot.on_message(filters.command(["addbl"], "C") & filters.user(DEVS))
async def _(client, message):
    em = await get_emo(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    tm = await message.reply(bhs("text_proses").format(em.proses))
    if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        blacklist = await get_chat(client.me.id)
        chat = await client.get_chat(per)

        if chat.id in blacklist:
            return await tm.edit(bhs("blacklist_exist").format(em.gagal, 'group'))

        try:
            await add_chat(client.me.id, chat.id)
            await tm.edit(bhs("blacklist_group").format(em.berhasil, chat.title))
            await asyncio.sleep(8)
            await message.delete()
            return await tm.delete()

        except Exception as error:
            return tm.edit(bhs("text_error").format(em.gagal, error))

    if message.chat.type == ChatType.PRIVATE:
        blacklist = await get_list_from_vars(client.me.id, "BL_UCAST", "DB_UCAST")
        try:
            user = await client.get_users(per)
        except Exception as error:
            return await tm.edit(bhs("text_error").format(em.gagal, error))

        if user.id in blacklist:
            return await tm.edit(bhs("blacklist_exist").format(em.gagal, 'user'))

        try:
            await add_to_vars(client.me.id, "BL_UCAST", user.id, "DB_UCAST")
            await tm.edit(bhs("blacklist_group").format(em.berhasil, user.id))
            await asyncio.sleep(8)
            await message.delete()
            return await tm.delete()

        except Exception as error:
            return await tm.edit(bhs("blacklist_failed").format(em.gagal))


@PY.UBOT("unbl", sudo=True)
@ubot.on_message(filters.command(["unbl"], "C") & filters.user(DEVS))
async def _(client, message):
    em = await get_emo(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    tm = await message.reply(bhs("text_proses").format(em.proses))
    if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        blacklist = await get_chat(client.me.id)
        chat = await client.get_chat(per)

        if chat.id not in blacklist:
            return await tm.edit(bhs("blacklist_unfail").format(em.gagal, chat.title))

        try:
            await remove_chat(client.me.id, chat.id)
            await tm.edit(bhs("blacklist_remove").format(em.berhasil, chat.title))
            await asyncio.sleep(7)
            await message.delete()
            return await tm.delete()

        except Exception as error:
            return await tm.edit(bhs("blacklist_failed").format(em.gagal, error))

    if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        blacklist = await get_list_from_vars(client.me.id, "BL_UCAST", "DB_UCAST")
        try:
            user = await client.get_users(per)
        except Exception as error:
            return await tm.edit(bhs("text_error").format(em.gagal, error))

        if user.id not in blacklist:
            return await tm.edit(bhs("blacklist_unfail").format(em.gagal, user.id))

        try:
            await remove_from_vars(client.me.id, "BL_UCAST", user.id, "DB_UCAST")
            await tm.edit(bhs("blacklist_remove").format(em.berhasil, user.id))
            await asyncio.sleep(8)
            return await tm.delete()

        except Exception as error:
            return await tm.edit(bhs("blacklist_failed").format(em.gagal, error))


@PY.UBOT("rallbl", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    get_bls = await get_chat(client.me.id)
    if len(get_bls) == 0:
        return await msg.edit(bhs("blacklist_gczero").format(em.gagal))
    for X in get_bls:
        await remove_chat(client.me.id, X)
        return await msg.edit(bhs("blacklist_clear").format(em.berhasil, 'groups'))


@PY.UBOT("rallucast", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    get_bls = await get_list_from_vars(client.me.id, "BL_UCAST", "DB_UCAST")
    if len(get_bls) == 0:
        return await msg.edit(bhs("blacklist_pczero").format(em.gagal))

    for X in get_bls:
        await remove_from_vars(client.me.id, "BL_UCAST", X, "DB_UCAST")
        await msg.delete()
        return await message.reply(bhs("blacklist_clear").format(em.berhasil, 'users'))


@PY.UBOT("listbl", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    Tm = await message.reply(bhs("text_proses").format(em.proses))
    msg = bhs("blacklist_pc").format(em.keterangan, 'groups')
    if len(await get_chat(client.me.id)) == 0:
           return await Tm.edit(bhs("blacklist_gczero").format(em.gagal))

    for X in await get_chat(client.me.id):
        try:
            get = await client.get_chat(X)
            msg += f"<b>— {get.title}</b> | <code>{get.id}</code>\n"
        except:
            msg += f"— <code>{X}</code>\n"
    await Tm.delete()
    await message.reply(f"<BLOCKQUOTE>{msg}</BLOCKQUOTE>")


@PY.UBOT("listucast")
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    ucast = await get_list_from_vars(client.me.id, "BL_UCAST", "DB_UCAST")
    Tm = bhs("blacklist_pc").format(em.keterangan, 'users')
    if not ucast:
        return await msg.edit(bhs("blacklist_pczero").format(em.gagal))

    for user_id in ucast:
        try:
            get = await client.get_users(user_id)
            Tm += f"— {get.first_name} {get.last_name or ''} | <code>{get.id}</code>\n"
        except:
            Tm += f"— <code>{user_id}</code>\n"
    await msg.delete()
    return await message.reply(f"<BLOCKQUOTE>{Tm}</BLOCKQUOTE>")



