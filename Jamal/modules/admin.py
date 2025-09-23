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
    em = get_emo(client)
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(bhs("admins_gagal").format(em.gagal, 'kick'))
    if user_id == (await client.get_me()).id:
        return await message.reply_text(
            bhs("admins_self").format(em.gagal, 'kick')
        )
    if user_id == DEVS:
        return await message.reply_text(bhs("admins_devs").format(em.gagal, 'kick'))

    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    if user_id in (await list_admins(message)):
        return await message.reply_text(
            bhs("admins_staff").format(em.gagal, mention, 'remove')
        )
    titit = reason if reason else "—"
    msg = bhs("admins_succes").format(em.berhasil, 'removed', em.mention, mention, em.keterangan, titit)
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
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    xtion = await EMO.MENTION(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(f"<b>{ggl}berikan nama pengguna,id pengguna atau balas pesan untuk memblokir pengguna dari group</b>")
    if user_id == (await client.get_me()).id:
        return await message.reply_text(
            f"<b>{ggl}tidak bisa memblokir diri sendiri</b>"
        )
    if user_id == DEVS:
        return await message.reply_text(
            f"<b>{ggl}tidak bisa memblokir developer botmu</b>"
        )
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    if user_id in (await list_admins(message)):
        return await message.reply(
            f"<b>{ggl} {mention} adalah bagian dari staff group. kamu tidak bisa memblokirnya </b>"
        )
    titit = reason if reason else "—"
    msg = f"<BLOCKQUOTE><b>{brhsl}berhasil diblokir</b>\n{xtion}pengguna : {mention}\n<b>{ktrg}alasan :</b> {titit}</BLOCKQUOTE>"
    try:
        if message.command[0] == "dban":
            await message.reply_to_message.delete()
        await message.chat.ban_member(user_id)
        await message.reply(msg)
    except Exception as error:
        await message.reply(error)


@PY.UBOT("mute|dmute", sudo=True)
@PY.GROUP
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    xtion = await EMO.MENTION(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(f"{ggl}berikan nama pengguna, id pengguna atau balas pesan untuk membisukan pengguna di group ini")
    if user_id == (await client.get_me()).id:
        return await message.reply_text(
            f"{ggl}kamu tidak bisa membisukan diri sendiri"
        )
    if user_id == DEVS:
        return await message.reply_text(f"{ggl}kamu tidak bisa membisukan developer botmu")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    if user_id in (await list_admins(message)):
        return await message.reply_text(
            f"{ggl} {mention} adalah bagian dari staff group. kamu tidak bisa membisukannya"
        )
    titit = reason if reason else "—"
    msg = f"<BLOCKQUOTE><b>{brhsl}berhasil dibisukan</b>\n{xtion}pengguna : {mention}<b>\n<b>{ktrg}alasan :</b> {titit}</BLOCKQUOTE>"
    try:
        if message.command[0] == "dmute":
            await message.reply_to_message.delete()
        await message.chat.restrict_member(user_id, ChatPermissions())
        await message.reply(msg)
    except Exception as error:
        await message.reply(error)


@PY.UBOT("unmute", sudo=True)
@PY.GROUP
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(f"{ggl} berikan nama pengguna, id pengguna atau balas pesan untuk melepas pembisuan pengguna di group")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    try:
        await message.chat.unban_member(user_id)
        await message.reply(f"<b>{brhsl} {mention} sudah tidak dibisukan</b>")
    except Exception as error:
        await message.reply(error)


@PY.UBOT("unban", sudo=True)
@PY.GROUP
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(f"{ggl}berikan nama pengguna, id pengguna atau balas pesan untuk melepas pemblokiran pengguna di group")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    try:
        await message.chat.unban_member(user_id)
        await message.reply(f"<b>{brhsl} {mention} sᴜᴅᴀʜ ʙɪsᴀ ᴊᴏɪɴ ʟᴀɢɪ</b>")
    except Exception as error:
        await message.reply(error)


@PY.UBOT("zombies")
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    Tm = await message.reply(f"<b>{prs}memproses</b>")
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
        return await message.reply(f"<b>{brhsl} {banned_users} akun terhapus berhasil di keluarkan</b>")
    else:
        await Tm.edit(f"<b>{ggl}tidak ada akun terhapus di grup ini</b>")
