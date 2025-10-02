import asyncio

from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant, UserAlreadyParticipant

from PyroUbot.core.helpers.class_emoji import *
from PyroUbot.config import BLACKLIST_CHAT
from PyroUbot import *

__MODULE__ = "leaveall"
__HELP__ = """
<BLOCKQUOTE><b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴊᴏɪɴʟᴇᴀᴠᴇ 』</b>

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}kickme/leave</code>
 ᴜɴᴛᴜᴋ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ɢʀᴜᴘ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}join</code> [ʟɪɴᴋ ɢʀᴏᴜᴘ ᴄʜᴀᴛ]
 ᴜɴᴛᴜᴋ ᴊᴏɪɴ ᴋᴇ ɢʀᴜᴘ ᴍᴇʟᴀʟᴜɪ ʟɪɴᴋ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}leavegc</code>
 ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ꜱᴇᴍᴜᴀ ɢʀᴜᴘ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}leavech</code>
 ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ꜱᴇᴍᴜᴀ ᴄʜᴀɴɴᴇʟ

❏ᴘᴇʀɪɴᴛᴀʜ: <code>{0}leavemute</code>
 ᴜɴᴛᴜᴋ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ʏᴀɴɢ ᴍᴇᴍʙᴀᴛᴀsɪ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ</BLOCKQUOTE>
"""


@PY.UBOT("join", sudo=True)
@ubot.on_message(filters.command(["join"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply_text(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    try:
        moh = await client.get_chat(Man)
        titit = moh.title
        await client.join_chat(Man)
        return await xxnx.edit(f"<BLOCKQUOTE><b>{brhsl}ʙᴇʀʜᴀsɪʟ ʙᴇʀɢᴀʙᴜɴɢ\n{gc}ᴄʜᴀᴛ: {titit}</b></BLOCKQUOTE>")
    except UserAlreadyParticipant:
        return await xxnx.edit(f"<BLOCKQUOTE>{ggl}ᴀᴋᴜɴᴍᴜ sᴜᴅᴀʜ ʙᴇʀɢᴀʙᴜɴɢ ᴅɪ {titit}</BLOCKQUOTE>")
    except Exception as ex:
        return await xxnx.edit_text(f"<b>{ggl}ERROR:\n\n{str(ex)}</b>")


@PY.UBOT("leave|kickme", sudo=True)
@ubot.on_message(filters.command(["leave|kickme"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    if Man in BLACKLIST_CHAT:
        return await xxnx.edit(
            f"<b>{ggl}kamu tidak bisa keluar dari group ini</b>"
        )
    try:
        moh = await client.get_chat(Man)
        titit = moh.title
        member = await client.get_chat_member(Man, "me")
        if member.status in (
            enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR,
        ):
            return await xxnx.edit(f"<BLOCKQUOTE>{ggl} ᴋᴀᴍᴜ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ {titit} ᴋᴀʀɴᴀ ᴋᴀᴍᴜ ᴀᴅᴀʟᴀʜ ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ</BLOCKQUOTE>")
        else:
            await xxnx.edit(f"<b>{brhsl}ʙᴇʀʜᴀsɪʟ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ {titit}</b>")
            await client.leave_chat(Man)
    except UserNotParticipant:
        return await xxnx.edit(f"<b>{ggl}ᴋᴀᴍᴜ ᴛɪᴅᴀᴋ ʙᴇʀɢᴀʙᴜɴɢ ᴅᴇɴɢᴀɴ {titit}</b>")
    except Exception as e:
        await xxnx.edit(f"<b>{ggl}ERROR: {str(e)}</b>")


@PY.UBOT("leavech")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    msg = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    done = 0
    er = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.CHANNEL:
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                stt = member.status
                if stt not in (
                    ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR,
                ):
                    done += 1
                    await client.leave_chat(chat)
            except BaseException:
                er += 1
    await msg.delete()
    return await message.reply(
        f"<b>{brhsl}ʙᴇʀʜᴀsɪʟ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ {done} ᴄʜᴀɴɴᴇʟ</b>"
    )

  
@PY.UBOT("leavegc")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    bcs = await EMO.BROADCAST(client)
    msg = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    done = 0
    er = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                stt = member.status
                if member not in BLACKLIST_CHAT and stt not in (
                    ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR,
                ):
                    done += 1
                    await client.leave_chat(chat)
            except BaseException:
                er += 1
    await msg.delete()
    return await message.reply(
        f"<b>{brhsl}ʙᴇʀʜᴀsɪʟ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ {done} ɢʀᴏᴜᴘ</b>"
    )


@PY.UBOT("leavemute")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    done += 1
                    await client.leave_chat(chat)
            except Exception:
                pass
    await msg.delete()
    return await message.reply(f"<BLOCKQUOTE>{brhsl}ʙᴇʀʜᴀsɪʟ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ {done} ɢʀᴏᴜᴘ ʏᴀɴɢ ᴍᴇᴍʙᴀᴛᴀsɪ</BLOCKQUOTE>")
