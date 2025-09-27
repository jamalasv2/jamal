import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from PyroUbot import *


__MODULE__ = "global"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɢʟᴏʙᴀʟ 』</b>

<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}gban</ᴄᴏᴅᴇ> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ]
 <i> ᴜɴᴛᴜᴋ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ</i>

<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}ungban</code> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ]
 <i> ᴜɴᴛᴜᴋ ᴜɴʙᴀɴɴᴇᴅ ᴜsᴇʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ</i>
 
<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}gmute</code> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ]
 <i>ᴜɴᴛᴜᴋ ᴍᴜᴛᴇ ᴜsᴇʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ</i>

<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}ungmute</code> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ]
 <i>ᴜɴᴛᴜᴋ ᴜɴᴍᴜᴛᴇ ᴜsᴇʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ</i>
"""


@PY.UBOT("gban", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["gban"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    xtion = await EMO.MENTION(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    if not user_id:
        return await Tm.edit(f"<b>{ggl}ᴜsᴇʀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_global_id(client, "global")
    for dialog in global_id:
        if user.id == DEVS:
            return await Tm.edit(f"<b>{ggl}ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ɢʙᴀɴ ᴅɪᴀ ᴋᴀʀᴇɴᴀ ᴅɪᴀ ᴘᴇᴍʙᴜᴀᴛ sᴀʏᴀ</b>")
        try:
            await client.ban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(f"<b>{brhsl}ᴘᴇʀɪɴᴛᴀʜ ʙᴇʀʜᴀsɪʟ!</b>\n\n{gc}ᴊᴜᴍʟᴀʜ: {done} ᴄʜᴀᴛ\n{ggl}ɢᴀɢᴀʟ: {failed} ᴄʜᴀᴛ\n{xtion}ᴜsᴇʀ: {user.mention}\n{ktrg}ᴋᴇᴛ: ɢʟᴏʙᴀʟ ʙᴀɴɴᴇᴅ</b>")
    return await Tm.delete()


@PY.UBOT("ungban", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["ungban"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    xtion = await EMO.MENTION(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs..</b>")
    if not user_id:
        return await Tm.edit("f<b>{ggl}ᴜsᴇʀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_global_id(client, "global")
    for dialog in global_id:
        try:
            await client.unban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(f"<b>{brhsl}ᴘᴇʀɪɴᴛᴀʜ ʙᴇʀʜᴀsɪʟ\n\n{gc}ᴊᴜᴍʟᴀʜ: {done} ᴄʜᴀᴛ\n{ggl}ɢᴀɢᴀʟ: {failed} ᴄʜᴀᴛ\n{xtion}ᴜsᴇʀ: {user.mention}\n{ktrg}ᴋᴇᴛ: ɢʟᴏʙᴀʟ ᴜɴʙᴀɴɴᴇᴅ</b>")
    return await Tm.delete()


@PY.UBOT("gmute", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["gmute"], "C") & filters.user(DEVS))
async def _(client, message):
	prs = await EMO.PROSES(client)
	brhsl = await EMO.BERHASIL(client)
	ggl = await EMO.GAGAL(client)
	xtion = await EMO.MENTION(client)
	gc = await EMO.BL_GROUP(client)
	ktrg = await EMO.BL_KETERANGAN(client)
	user_id = await extract_user(message)
	Tm = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
	if not user_id:
		return await Tm.edit(f"<b>{ggl}ᴜsᴇʀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
	try:
		user = await client.get_users(user_id)
	except Exception as error:
		return await Tm.edit(error)
	done = 0
	failed = 0
	global_id = await get_global_id(client, "global")
	for dialog in global_id:
		if user.id == DEVS:
			return await Tm.edit(f"<b>{ggl}ᴋᴀᴜ ɢᴀᴋ ʙɪsᴀ ɢᴍᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ ʙᴏᴛᴍᴜ</b>")
		try:
			await client.restrict_chat_member(dialog, user.id, ChatPermissions())
			done += 1
			await asyncio.sleep(0.1)
		except Exception:
			failed += 1
			await asyncio.sleep(0.1)
	await message.reply(f"<b>{brhsl}ᴘᴇʀɪɴᴛᴀʜ ʙᴇʀʜᴀsɪʟ!\n\n{gc}ᴊᴜᴍʟᴀʜ: {done} ᴄʜᴀᴛ\n{ggl}ɢᴀɢᴀʟ: {failed} ᴄʜᴀᴛ\n{xtion}ᴜsᴇʀ: {user.mention}\n{ktrg}ᴋᴇᴛ: ɢʟᴏʙᴀʟ ᴍᴜᴛᴇ</b>")
	return await Tm.delete()


@PY.UBOT("ungmute", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["ungmute"], "C") & filters.user(DEVS))
async def _(client, message):
	prs = await EMO.PROSES(client)
	brhsl = await EMO.BERHASIL(client)
	ggl = await EMO.GAGAL(client)
	gc = await EMO.BL_GROUP(client)
	ktrg = await EMO.BL_KETERANGAN(client)
	xtion = await EMO.MENTION(client)
	user_id = await extract_user(message)
	Tm = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
	if not user_id:
		return await Tm.edit(f"<b>{ggl}ᴜsᴇʀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ")
	try:
		user = await client.get_users(user_id)
	except Exception as error:
		return await Tm.edit(error)
	done = 0
	failed = 0
	global_id = await get_global_id(client, "global")
	for dialog in global_id:
		try:
			await client.unban_chat_member(dialog, user.id)
			done += 1
			await asyncio.sleep(0.1)
		except Exception:
			failed += 1
			await asyncio.sleep(0.1)
	await message.reply(f"<b>{brhsl}ᴘᴇʀɪɴᴛᴀʜ ʙᴇʀʜᴀsɪʟ!\n\n{gc}ᴊᴜᴍʟᴀʜ: {done} ᴄʜᴀᴛ\n{ggl}ɢᴀɢᴀʟ: {failed} ᴄʜᴀᴛ\n{xtion}ᴜsᴇʀ: {user.mention}\n{ktrg}ᴋᴇᴛ: ɢʟᴏʙᴀʟ ᴜɴᴍᴜᴛᴇ</b>")
	return await Tm.delete()
			

