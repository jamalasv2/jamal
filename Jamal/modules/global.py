import asyncio

from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.errors import *
from pyrogram.types import *

from Jamal import *
from langs import bhs, get_bhs


__MODULE__ = "global"
__HELP__ = get_bhs("global_cmd")


@PY.UBOT("gban", sudo=True)
@ubot.on_message(filters.command(["gban"], "C") & filters.user(SUDO))
async def _(client, message):
    em = await get_emo(client)
    user_id = await extract_user(message)
    Tm = await message.reply(bhs("text_proses").format(em.proses))
    if not user_id:
        return await Tm.edit(bhs("global_nfound").format(em.gagal, 'banned'))
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_global_id(client, "global")
    for dialog in global_id:
        if user.id in DEVS or user.id in SUDO:
            return await Tm.edit(bhs("global_dev").format(em.gagal, 'banned'))
        try:
            await client.ban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)

        except Exception:
            failed += 1

    await Tm.delete()
	return await message.reply(bhs("global_sukses").format(em.berhasil, 'banned', em.mention, user.mention, em.total, done))


@PY.UBOT("ungban", sudo=True)
@ubot.on_message(filters.command(["ungban"], "C") & filters.user(SUDO))
async def _(client, message):
    em = await get_emo(client)
    user_id = await extract_user(message)
    Tm = await message.reply(bhs("text_proses").format(em.proses))
    if not user_id:
        return await Tm.edit(bhs("global_nfound").format(em.gagal, 'unbanned'))
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

    await Tm.delete()
	return await message.reply(bhs("global_sukses").format(em.berhasil, 'unbanned', em.mention, user.mention, em.total, done))


@PY.UBOT("gmute", sudo=True)
@ubot.on_message(filters.command(["gmute"], "C") & filters.user(SUDO))
async def _(client, message):
	em = await get_emo(client)
	user_id = await extract_user(message)
	Tm = await message.reply(bhs("text_proses").format(em.proses))
	if not user_id:
		return await Tm.edit(bhs("global_nfound").format(em.gagal, 'mute'))
	try:
		user = await client.get_users(user_id)
	except Exception as error:
		return await Tm.edit(error)
	done = 0
	failed = 0
	global_id = await get_global_id(client, "group")
	for dialog in global_id:
		if user.id in DEVS or user.id in SUDO:
			return await Tm.edit(bhs("global_dev").format(em.gagal, 'mute'))
		try:
			await client.restrict_chat_member(dialog, user.id, ChatPermissions())
			done += 1
			await asyncio.sleep(0.1)

		except Exception:
			failed += 1
			await asyncio.sleep(0.1)

    await Tm.delete()
	return await message.reply(bhs("global_sukses").format(em.berhasil, 'mute', em.mention, user.mention, em.total, done))


@PY.UBOT("ungmute", sudo=True)
@ubot.on_message(filters.command(["ungmute"], "C") & filters.user(SUDO))
async def _(client, message):
	em = await get_emo(client)
	user_id = await extract_user(message)
	Tm = await message.reply(bhs("text_proses").format(em.proses))
	if not user_id:
		return await Tm.edit(bhs("global_nfound").format(em.gagal, 'unmute'))
	try:
		user = await client.get_users(user_id)
	except Exception as error:
		return await Tm.edit(error)
	done = 0
	failed = 0
	global_id = await get_global_id(client, "group")
	for dialog in global_id:
		try:
			await client.unban_chat_member(dialog, user.id)
			done += 1
			await asyncio.sleep(0.1)

		except Exception:
			failed += 1
			await asyncio.sleep(0.1)

    await Tm.delete()
	return await message.reply(bhs("global_sukses").format(em.berhasil, 'unmute', em.mention, user.mention, em.total, done))
