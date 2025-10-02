import asyncio

from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant, UserAlreadyParticipant

from Jamal.core.helpers.class_emoji import get_emo
from Jamal.config import BLACKLIST_CHAT, SUDO
from Jamal import ubot

from langs import bhs, get_bhs

__MODULE__ = "leaveall"
__HELP__ = get_bhs("invite_cmd")


@PY.UBOT("join", sudo=True)
@ubot.on_message(filters.command(["join"], "C") & filters.user(SUDO))
async def _(client, message):
    em = await get_emo(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply_text(bhs("text_proses").format(em.proses))
    try:
        moh = await client.get_chat(Man)
        await client.join_chat(Man)
        return await xxnx.edit(bhs("leave_join").format(em.berhasil, moh.title))
    except UserAlreadyParticipant:
        return await xxnx.edit(bhs("leave_joined").format(em.gagal, moh.title))
    except Exception as ex:
        return await xxnx.edit_text(bhs("text_error").format(em.peringatan, ex))


@PY.UBOT("leave|kickme", sudo=True)
@ubot.on_message(filters.command(["leave|kickme"], "C") & filters.user(SUDO))
async def _(client, message):
    em = await get_emo(client)
    man = message.command[1] if len(message.command) > 1 else message.chat.id
    xx = await message.reply(bhs("text_proses").format(em.proses))
    if man in BLACKLIST_CHAT:
        return await xx.edit(bhs("leave_sp").format(em.gagal))

    try:
        moh = await client.get_chat(man)
        member = await client.get_chat_member(man, "me")
        if member.status in ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER:
            return await xx.edit(bhs("leave_admin").format(em.gagal, moh.title))

        else:
            await xx.edit(bhs("leave_leave").format(em.berhasil, moh.title))
            await client.leave_chat(man)
            return
    except UserNotParticipant:
        return await xx.edit(bhs("leave_leaved").format(em.gagal, man))
    except Exception as error:
        return xx.edit(bhs("text_error").format(em.gagal, error))


@PY.UBOT("leaveall", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if len(message.command) < 2:
        return await msg.edit(bhs("leave_noqueri").format(em.gagal))

    command, query = message.command[:2]
    done = 0

    if query.lower() == "channel":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ChatType.CHANNEL:
                chat = dialog.chat.id
                try:
                    member = await client.get_chat_member(chat, "me")
                    if member.status not in ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER:
                        done += 1
                        await client.leave_chat(chat)
                        await msg.delete()
                        return await message.reply(bhs("leave_all").format(em.berhasil, done, 'channel'))

                    if len(done) == 0:
                        return await msg.edit(bhs("leave_novalue").format(em.gagal, 'channel'))
                except Exception as error:
                    return await msg.edit(bhs("text_error").format(em.peringatan, error))

    elif query.lower() == "group":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ChatType.GROUP, ChatType.SUPERGROUP:
                chat = dialog.chat.id
                try:
                    member = await client.get_chat_member(chat, "me")
                    if member.status not in ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER:
                        done += 1
                        await client.leave_chat(chat)
                        await asyncio.sleep(1)
                        await msg.delete()
                        return await message.reply(bhs("leave_all").format(em.berhasil, done, 'group'))

                    if len(done) == 0:
                        return await msg.edit(bhs("leave_novalue").format(em.gagal, 'group'))

                except Exception as error:
                    return await msg.edit(bhs("text_error").format(em.peringatan, error))



@PY.UBOT("leavech")
async def _(client, message):
    
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
