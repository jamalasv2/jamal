import asyncio

from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant, UserAlreadyParticipant

from Jamal.core.helpers.class_emoji import get_emo
from Jamal.config import BLACKLIST_CHAT, SUDO
from Jamal import ubot

from langs import bhs, get_bhs

__MODULE__ = "leaveall"
__HELP__ = get_bhs("leave_cmd")


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
        if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
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
                    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
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
            if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                chat = dialog.chat.id
                try:
                    member = await client.get_chat_member(chat, "me")
                    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                        done += 1
                        await client.leave_chat(chat)
                        await asyncio.sleep(1)
                        await msg.delete()
                        return await message.reply(bhs("leave_all").format(em.berhasil, done, 'group'))

                    if len(done) == 0:
                        return await msg.edit(bhs("leave_novalue").format(em.gagal, 'group'))

                except Exception as error:
                    return await msg.edit(bhs("text_error").format(em.peringatan, error))

    elif query.lower() == "mute":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                chat = dialog.chat.id
                try:
                    member = await client.get_chat(chat, "me")
                    if member.status in ChatMemberStatus.RESTRICTED:
                        done += 1
                        await client.leave_chat(chat)
                        await asyncio.sleep(1)
                        await msg.delete()
                        return await message.reply(bhs("leave_mute").format(em.berhasil, done))
                    else:
                        return await msg.edit(bhs("leave_no").format(em.gagal))

                except Exception as error:
                    return await msg.edit(bhs("text_error").format(em.peringatan, error))

