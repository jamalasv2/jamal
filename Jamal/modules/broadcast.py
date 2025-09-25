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
__HELP__ = """
    <blockquote>**『 bantuan untuk broadcast 』**

**❏ perintah:** <code>{0}gcast</code>
— untuk mengirim pesan siaran ke semua grup

**❏ perintah:** <code>{0}gucast</code>
— untuk mengirim pesan siaran ke semua pengguna

**❏ perintah:** <code>{0}addbl</code>
— untuk menambahkan grup ke daftar hitam broadcast

**❏ perintah:** <code>{0}unbl</code>
— untuk menghapus grup dari daftar hitam broadcast

**❏ perintah:** <code>{0}listbl</code>
— untuk menampilkan semua grup yang ada didaftar hitam broadcast

**❏ perintah:** <code>{0}blucast</code>
— untuk menambahkan pengguna ke daftar hitam broadcast

**❏ perintah:** <code>{0}delucast</code>
— untuk menghapus pengguna dari daftar hitam broadcast

**❏ perintah:** <code>{0}listucast</code>
— untuk menampilkan semua pengguna yang ada didaftar hitam</blockquote>
"""


@PY.UBOT("gcast", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["gcast"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"{prs} memproses..")
    text = get_message(message)

    if not text:
        return await msg.edit(f"{ggl} ketik teks atau balas pesan")

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
            await msg.edit(f"<blockquote>{ggl} akun anda terkena **FloodWait**. pesan anda akan otomatis terkirim setelah **{e.value} detik**.\nmohon menunggu hingga pesan selesai terkirim</blockquote>")
            await asyncio.sleep(e.value)
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except Exception as e:
            fail += 1
            pass
    await msg.delete()
    _msg = f"""
<blockquote>**{gc} pesan siaran grup**
**{brhsl} berhasil:** {done}
**{ggl} gagal:** {fail}</blockquote>
"""
    return await message.reply(_msg)


@PY.UBOT("gucast", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["gucast"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    gc = await EMO.BL_GROUP(client)
    text = get_message(message)
    msg = await message.reply(f"{prs} memproses..")

    if not text:
        return await msg.edit(f"{ggl} ketik teks atau balas pesan")

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
            await msg.edit(f"{ggl} akun anda terkena **FloodWait**.\npesan akan otomatis terkirim setelah **{e.value} detik**")
            await asyncio.sleep(e.value)
            await (text.copy(chat_id, text) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except Exception:
            fail += 1
            pass
    await msg.delete()
    _msg = f"""
<blockquote>**{gc} pesan siaran pengguna**
**{brhsl} berhasil:** {done}
**{ggl} gagal:** {fail}</blockquote>
"""
    return await message.reply(_msg)


@PY.BOT("broadcast")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("memproses pesan siaran..")
    send = get_message(message)
    if not send:
        return await msg.edit("mohon balas pesan atau ketik pesan")
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
            
