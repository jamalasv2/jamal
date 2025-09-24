import asyncio

from pyrogram.errors.exceptions import FloodWait
from pyrogram.enums import ChatType

from PyroUbot import *

__MODULE__ = "archive"
__HELP__ = """
    <b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀʀᴄʜɪᴠᴇ  』</b>

<BLOCKQUOTE><b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}arsipgc</code>
 ᴜɴᴛᴜᴋ ᴍᴇᴍᴀsᴜᴋᴋᴀɴ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴋᴇ ғᴏʟᴅᴇʀ ᴀʀsɪᴘ

<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}unarsipgc</code>
 ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴅᴀʀɪ ғᴏʟᴅᴇʀ ᴀʀsɪᴘ</BLOCKQUOTE>

<BLOCKQUOTE><b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}arsipchat</code>
 ᴍᴇᴍᴀsᴜᴋᴋᴀɴ sᴇᴍᴜᴀ ᴄʜᴀᴛ ᴋᴇᴅᴀʟᴀᴍ ғᴏʟᴅᴇʀ ᴀʀsɪᴘ
 
<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}unarsipchat</code>
 ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ sᴡᴍᴜᴀ ᴄʜᴀᴛ ᴅᴀʀɪ ғᴏʟᴅᴇʀ ᴀʀsɪᴘ</BLOCKQUOTE>
 
<BLOCKQUOTE><b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}arsipall</code>
 ᴜɴᴛᴜᴋ ᴍᴇᴍᴀsᴜᴋᴋᴀɴ sᴇᴍᴜᴀ ᴄʜᴀᴛ(ɢʀᴏᴜᴘ, ʙᴏᴛ, ᴄʜᴀɴɴᴇʟ, ᴘᴇʀsᴏɴᴀʟ) ᴋᴇ ғᴏʟᴅᴇʀ ᴀʀsɪᴘ</BLOCKQUOTE>
"""

@PY.UBOT("arsipgc")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"{prs}ᴍᴇᴍᴘʀᴏsᴇs")

    done = 0
    failed = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.archive_chats(chat)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.archive_chats(chat)
                done += 1
            except BaseException:
                failed += 1
    await msg.edit(
        f"{gc}ᴀʀsɪᴘ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ\n{brhsl}ʙᴇʀʜᴀsɪʟ: {done} ɢʀᴏᴜᴘ\n{ggl}ɢᴀɢᴀʟ: {failed} ɢʀᴏᴜᴘ"
    )


@PY.UBOT("unarsipgc")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"{prs}ᴍᴇᴍᴘʀᴏsᴇs")

    done = 0
    failed = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.unarchive_chats(chat)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.unarchive_chats(chat)
                done += 1
            except BaseException:
                failed += 1
    await msg.edit(
        f"{gc} ᴜɴᴀʀsɪᴘ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ\n{brhsl}ʙᴇʀʜᴀsɪʟ: {done} ɢʀᴏᴜᴘ\n{ggl}ɢᴀɢᴀʟ: {failed} ɢʀᴏᴜᴘ"
    )


@PY.UBOT("arsipchat")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"{prs}ᴍᴇᴍᴘʀᴏsᴇs")

    done = 0
    failed = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            chat = dialog.chat.id
            try:
                done += 1
                await client.archive_chats(chat)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                return await client.archive_chats(chat)
                done += 1
            except BaseException:
                failed += 1
    await msg.edit(
        f"{gc}ᴀʀsɪᴘ ᴄʜᴀᴛ\n{brhsl}ʙᴇʀʜᴀsɪʟ: {done} ᴄʜᴀᴛs\n{ggl}ɢᴀɢᴀʟ: {failed} ᴄʜᴀᴛs"
    )


@PY.UBOT("unarsipchat")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"{prs}ᴍᴇᴍᴘʀᴏsᴇs")

    done = 0
    failed = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            chat = dialog.chat.id
            try:
                done += 1
                await client.unarchive_chats(chat)
            except BaseException:
                failed += 1
    await msg.edit(
        f"{gc}ᴜɴᴀʀsɪᴘ ᴄʜᴀᴛs\n{brhsl}ʙᴇʀʜᴀsɪʟ: {done} ᴄʜᴀᴛs\n{ggl}ɢᴀɢᴀʟ: {failed} ᴄʜᴀᴛs"
    )


@PY.UBOT("arsipall")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"{prs}ᴍᴇᴍᴘʀᴏsᴇs")

    done = 0
    failed = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.PRIVATE, enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL, enums.ChatType.BOT):
            chat = dialog.chat.id
            try:
                done += 1
                await client.archive_chats(chat)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.archive_chats(chat)
                done += 1
            except BaseException:
                failed += 1
    await msg.edit(
        f"{gc}ᴀʀsɪᴘᴋᴀɴ sᴇᴍᴜᴀ ᴄʜᴀᴛs\n{brhsl}ʙᴇʀʜᴀsɪʟ: {done}\n{ggl}ɢᴀɢᴀʟ: {failed}"
    )
