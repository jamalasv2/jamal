import asyncio

from pyrogram.types import ChatPermissions

from Jamal.config import DEVS
from Jamal.core.helpers.class_emoji import get_emo
from .. import *
from langs import bhs, get_bhs

__MODULE__ = "admin"
__HELP__ = get_bhs("admins_cmd")


@PY.UBOT("kick|dkick", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    kt = bhs("kick")
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(bhs("admins_gagal").format(em.gagal, kt))
    if user_id == (await client.get_me()).id:
        return await message.reply_text(
            bhs("admins_self").format(em.gagal, kt)
        )
    if user_id == DEVS:
        return await message.reply_text(bhs("admins_devs").format(em.gagal, kt))

    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    if user_id in (await list_admins(message)):
        return await message.reply_text(
            bhs("admins_staff").format(em.gagal, mention, kt)
        )
    titit = reason if reason else "—"
    msg = bhs("admins_succes").format(em.berhasil, kt, em.mention, mention, em.keterangan, titit)
    try:
        if message.command[0] == "dkick":
            await message.reply_to_message.delete()
        await message.chat.ban_member(user_id)
        await message.reply(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except Exception as error:
        await message.reply(error)


@PY.UBOT("ban|dban", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    kt = bhs("ban")
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(bhs("admins_gagal").format(em.gagal, kt))
    if user_id == (await client.get_me()).id:
        return await message.reply_text(
            bhs("admins_self").format(em.gagal, kt)
        )
    if user_id == DEVS:
        return await message.reply_text(
            bhs("admins_devs").format(em.gagal, kt)
        )
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    if user_id in (await list_admins(message)):
        return await message.reply(
            bhs("admins_staff").format(em.gagal, mention, kt)
        )
    titit = reason if reason else "—"
    msg = bhs("admins_succes").format(em.berhasil, kt, em.mention, mention, em.keterangan, titit)
    try:
        if message.command[0] == "dban":
            await message.reply_to_message.delete()
        await message.chat.ban_member(user_id)
        await message.reply(msg)
    except Exception as error:
        await message.reply(error)


@PY.UBOT("mute|dmute", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    kt = bhs("mute")
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(bhs("admins_gagal").format(em.gagal, kt))
    if user_id == (await client.get_me()).id:
        return await message.reply_text(
            bhs("admins_self").format(em.gagal, kt)
        )
    if user_id == DEVS:
        return await message.reply_text(bhs("admins_devs").format(em.gagal, kt))
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    if user_id in (await list_admins(message)):
        return await message.reply_text(
            bhs("admins_staff").format(em.gagal, mention, kt)
        )
    titit = reason if reason else "—"
    msg = bhs("admins_succes").format(em.berhasil, kt, em.mention, mention, em.keterangan, titit)
    try:
        if message.command[0] == "dmute":
            await message.reply_to_message.delete()
        await message.chat.restrict_member(user_id, ChatPermissions())
        await message.reply(msg)
    except Exception as error:
        await message.reply(error)


@PY.UBOT("unmute", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    kt = bhs("mute")
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(bhs("admins_gagal").format(em.gagal, kt))
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    try:
        await message.chat.unban_member(user_id)
        await message.reply(bhs("admins_un").format(em.berhasil, kt, em.mention, mention))
    except Exception as error:
        await message.reply(error)


@PY.UBOT("unban", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    kt = bhs("ban")
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(bhs("admins_gagal").format(em.gagal, kt))
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    try:
        await message.chat.unban_member(user_id)
        await message.reply(bhs("admins_un").format(em.berhasil, kt, em.mention, mention))
    except Exception as error:
        await message.reply(error)


@PY.UBOT("zombies")
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    Tm = await message.reply(bhs("text_proses").format(em.proses))
    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                banned_users += 1
                await message.chat.ban_member(deleted_user)
                await asyncio.sleep(2)
                await message.chat.unban_member(deleted_user)
            except Exception:
                pass
        await Tm.delete()
        return await message.reply(bhs("admins_zombie").format(em.berhasil, banned_users))
    else:
        await Tm.edit(bhs("admins_zombie2").format(em.gagal))
