import asyncio

from pyrogram.errors.exceptions import FloodWait
from pyrogram.enums import ChatType

from Jamal import *
from langs import bhs, get_bhs

__MODULE__ = "archive"
__HELP__ = get_bhs("arsip_cmd")

@PY.UBOT("arsip")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"**{prs} memproses**")

    if len(message.command) < 2:
        return await msg.edit(f"**{ggl} perintah salah\nberikan queri untuk memasukkan pesan kedalam arsip**")

    command, query = message.command[:2]
    chat = await get_global_id(client, query)

    if query.lower() == "all":
        try:
            await client.archive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan (group, personal, saluran & bot) kedalam arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.archive_chats(chat)
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan (group, personal, saluran & bot) kedalam arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "gc":
        try:
            await client.archive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan group kedalam arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.archive_chats(chat)
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan group kedalam arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "pc":
        try:
            await client.archive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan personal kedalam arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.archive_chats(chat)
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan personal kedalam arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "bot":
        try:
            await client.archive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} pesan bot kedalam arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.archive_chats(chat)
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "ch":
        try:
            await client.archive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} saluran kedalam arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.archive_chats(chat)
            return await message.reply(
                f"**{brhsl} berhasil memasukkan {len(chat)} saluran kedalam arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )


@PY.UBOT("unarsip")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    msg = await message.reply(f"**{prs} memproses**")

    if len(message.command) < 2:
        return await msg.edit(f"**{ggl} perintah salah\n berikan queri untuk mengeluarkan pesan dari arsip**")

    command, query = message.command[:2]
    chat = await get_global_id(client, query)

    if query.lower() == "all":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan (group, personal, saluran & bot) berhasil dikeluarkan dari folder arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan (group, personal, saluran & bot) berhasil dikeluarkan dari folder arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "gc":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan group berhasil dikeluarkan dari folder arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan group berhasil dikeluarkan dari folder arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "pc":
        try:
            await client.umarchive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan personal berhasil dikeluarkan dari folder arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan personal berhasil dikeluarkan dari folder arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "bot":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} {len(chat)} pesan bot berhasil dikeluarkan dari folder arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
    elif query.lower() == "ch":
        try:
            await client.unarchive_chats(chat)
            await msg.delete()
            return await message.reply(
                f"**{brhsl} {len(chat)} saluran berhasil dikeluarkan dari folder arsip**"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.unarchive_chats(chat)
            return await message.reply(
                f"**{brhsl} {len(chat)} saluran berhasil dikeluarkan dari folder arsip**"
            )
        except Exception as e:
            return await msg.edit(
                f"**{ggl}ERROR**:\n{e}"
            )
