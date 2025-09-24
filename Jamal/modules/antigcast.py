import asyncio 
from pyrogram import filters
from Jamal import *
from langs import bhs, get_bhs

from .. import *

__MODULE__ = "antigcast"
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
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    gc = await EMO.BL_GROUP(client)
    msg = await message.reply(f"<b>{prs}memproses</b>")
    if len(message.command) <2:
        return await msg.edit(
          f"<b>{ggl}ʜᴀʀᴀᴘ ɢᴜɴᴀᴋᴀɴ ᴏᴘsɪ ᴏɴ ᴀᴛᴀᴜ ᴏғғ</b>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()
  
    if command not in query:
        return await msg.edit(
          f"<b>{ggl}ɢᴜɴᴀᴋᴀɴ ᴏᴘsɪ ᴏɴ ᴀᴛᴀᴜ ᴏғғ</b>"
        )

    value = query[command]
    text = "ᴅɪᴀᴋᴛɪғᴋᴀɴ" if value else "ᴅɪɴᴏɴᴀᴋᴛɪғᴋᴀɴ"
  
    await set_vars(client.me.id, f"chat_{message.chat.id}", value)
    await msg.delete()
    return await message.reply(
        f"<b>{brhsl}ᴀɴᴛɪɢᴄᴀsᴛ {text}\n{gc}ɢʀᴏᴜᴘ:{message.chat.title}</b>"
    )


@PY.UBOT("bl")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"<b>{prs}memproses</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{ggl}ʙᴇʀɪᴋᴀɴ ᴜsᴇʀɴᴀᴍᴇ ᴀᴛᴀᴜ ʀᴇᴘʟʏ ᴄʜᴀᴛ</b>"
        )
  
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl}ERROR:\n{error}")
  
    blacklist_users = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
  
    if user.id in blacklist_users:
        return await msg.edit(
            f"<b>{ggl}ᴜsᴇʀ sᴜᴅᴀʜ ᴅɪʙʟᴀᴄᴋʟɪsᴛ</b>"
        )

    try:
        await add_to_vars(client.me.id, "BL_USERS", user.id, "DB_ANKES")
        return await msg.edit(
            f"<b>{brhsl}ᴜsᴇʀ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ʙʟᴀᴄᴋʟɪsᴛ</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("delbl")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{ggl}ʙᴇʀɪᴋᴀɴ ᴜsᴇʀɴᴀᴍᴇ ᴀᴛᴀᴜ ᴜsᴇʀɪᴅ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    blacklist_users = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
  
    if user.id not in blacklist_users:
        return await msg.edit(
            f"<b>{ggl}[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) ᴛɪᴅᴀᴋ ᴅᴀʟᴀᴍ ʙʟᴀᴄᴋʟɪsᴛ</b>"
        )

    try:
        await remove_from_vars(client.me.id, user.id, "BL_USERS", user.id, "DB_ANKES")
        return await msg.edit(
            f"<b>{brhsl}[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("ralluser")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"{prs}memproses")
    get_usr = await get_list_from_vars(client.me.id, "BL_USERS", "DB_ANKES")
    if len(get_usr) == 0:
        return await msg.edit(f"{ggl}tidak ada pengguna dalam dafyar hitam")
    for X in get_usr:
        await remove_from_vars(client.me.id, "BL_USERS", X, "DB_ANKES")
    await msg.edit(f"{brhsl}berhasil menghapus semua pengguna dari daftar hitam")


@PY.UBOT("userlist")
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    Sh = await message.reply(f"<b>{prs}memproses</b>")
    bl_user = await get_ankes(client.me.id)
    msg = f"<b>total pengguna dalam daftar hitam: {len(bl_user)}</b>\n\n"

    if not bl_user:
        return await Sh.edit(f"{ggl}tidak ada pengguna dalam daftar hitam")

    for user_id in bl_user:
        try:
            user = await client.get_users(int(user_id))
            msg += f"├ {user.first_name} {user.last_name or ''} | <code>{user.id}</code>\n"
        except:
            msg += f"├ <code>{user_id}</code>\n"
    await Sh.delete()
    return await message.reply(f"<BLOCKQUOTE>{msg}</BLOCKQUOTE>")
