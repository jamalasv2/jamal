import asyncio 
from pyrogram import filters
from Jamal import *
from langs import bhs, get_bhs

from .. import *

__MODULE__ = "antispam"
__HELP__ = get_bhs("ankes_cmd")


@ubot.on_message(filters.group & ~filters.bot & ~filters.me, group=1)
async def ankes_bl(client, message):
    if await get_vars(client.me.id, f"chat_{message.chat.id}"):
        blacklist = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
        user = message.from_user if message.from_user else message.sender_chat
        if user.id in blacklist:
            await client.delete_messages(message.chat.id, message.id)
            msg = await client.send_message(
              message.chat.id,
              f"<BLOCKQUOTE>⚠️ pemberitahuan\npesan dari {user.mention} telah dihapus</BLOCKQUOTE>"
            )
            await asyncio.sleep(5)
            return await msg.delete()


@PY.UBOT("ankes")
@PY.GROUP
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    if len(message.command) <2:
        return await msg.edit(bhs("ankes_onoff").format(em.gagal))

    query = {"on": True, "off": False}
    command = message.command[1].lower()
  
    if command not in query:
        return await msg.edit(bhs("ankes_onoff").format(em.gagal))

    value = query[command]
    text = bhs("ankes_on") if value else bhs("ankes_off")

    current = await get_vars(client.me.id, f"chat_{message.chat.id}")

    if value == current:
        return await msg.edit(bhs("ankes_current").format(em.gagal, text, message.chat.title))
  
    await set_vars(client.me.id, f"chat_{message.chat.id}", value)
    await msg.delete()
    return await message.reply(bhs("ankes_aktif").format(em.berhasil, text, em.group, message.chat.title))


@PY.UBOT("bl")
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(bhs("ankes_blfail").format(em.gagal))
  
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(bhs("ankes_error").format(em.gagal, error))
  
    blacklist_users = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
  
    if user.id in blacklist_users:
        return await msg.edit(bhs("ankes_usrbl").format(em.gagal))

    try:
        await add_to_vars(client.me.id, "BL_USERS", user.id, "DB_ANKES")
        return await msg.edit(bhs("ankes_addbl").format(em.berhasil, user.id))
    except Exception as error:
        return await msg.edit(bhs("ankes_error").format(em.gagal, error))


@PY.UBOT("delbl")
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.gagal))
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(bhs("ankes_delfail").format(em.gagal))

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(bhs("ankes_error").format(em.gagal, error))

    blacklist_users = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
  
    if user.id not in blacklist_users:
        return await msg.edit(bhs("ankes_userdbl").format(em.gagal))

    try:
        await remove_from_vars(client.me.id, user.id, "BL_USERS", user.id, "DB_ANKES")
        return await msg.edit(bhs("ankes_usrremove").format(em.berhasil, user.id))
    except Exception as error:
        return await msg.edit(bhs("ankes_error").format(em.gagal, error))


@PY.UBOT("ralluser")
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    get_usr = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
    if len(get_usr) == 0:
        return await msg.edit(bhs("ankes_zero").format(em.gagal))
    for X in get_usr:
        await remove_from_vars(client.me.id, "BL_USERS", X, "DB_ANKES")
    await msg.edit(bhs("ankes_rmall").format(em.berhasil))


@PY.UBOT("listbl")
async def _(client, message):
    em = get_emo(client)
    Sh = await message.reply(bhs("text_proses").format(em.proses))
    bl_user = await get_ankes(client.me.id)
    msg = bhs("ankes_list").format(em.keterangan))

    if not bl_user:
        return await Sh.edit(bhs("ankes_zero").format(em.gagal))

    for user_id in bl_user:
        try:
            user = await client.get_users(int(user_id))
            msg += f"├ {user.first_name} {user.last_name or ''} | <code>{user.id}</code>\n"
        except:
            msg += f"├ <code>{user_id}</code>\n"
    await Sh.delete()
    return await message.reply(f"<BLOCKQUOTE>{msg}</BLOCKQUOTE>")
