from pyrogram import *

from Jamal.database.saved import *
from Jamal.core.helpers.class_emoji import *
from Jamal import *

__MODULE__ = ""
__HELP__ = """
<BLOCKQUOTE><b> 『 bantuan untuk blacklist 』</b>

**❏ perintah:** <code>{0}addbl</code>
— untuk menambahkan grup ke daftar hitam

**❏ perintah:** <code>{0}unbl</code>
— untuk menghapus grup dari daftar hitam

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}listbl</code>
ᴜɴᴛᴜᴋ ᴍᴇᴍᴇʀɪᴋsᴀ ʙʟᴀᴄᴋʟɪsᴛ ɢʀᴏᴜᴘ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}rallbl</code>
ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs sᴇᴍᴜᴀ ʙʟᴀᴄᴋʟɪsᴛ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}blucast</code>
 ᴜɴᴛᴜᴋ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴜsᴇʀ ᴋᴇᴅᴀʟᴀᴍ ʙʟᴀᴄᴋʟɪsᴛ ᴜᴄᴀsᴛ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}delucast</code>
  ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ᴜsᴇʀ ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ

❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}listucast</code>
 ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ᴜsᴇʀ ʏᴀɴɢ ᴅɪʙʟᴀᴄᴋʟɪsᴛ</BLOCKQUOTE>
"""


@PY.UBOT("addbl", sudo=True)
@PY.GROUP
@ubot.on_message(filters.command(["addbl"], "C") & filters.user(DEVS))
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    titit = await client.get_chat(per)
    Tm = await message.reply(f"<b>{prs} memproses...</b>")
    blacklist = await get_chat(client.me.id)
    if per in blacklist:
        return await Tm.edit(f"<BLOCKQUOTE><b>{ggl} grup ini sudah ada didaftar hitam broadcast!</b></BLOCKQUOTE>")
    add_blacklist = await add_chat(client.me.id, per)
    if add_blacklist:
        await Tm.edit(f"<BLOCKQUOTE><b>{brhsl} ditambahkan ke daftar hitam broadcast\n{gc} group: {titit.title}</b></BLOCKQUOTE>")
    else:
        await Tm.edit(f"<BLOCKQUOTE>{ggl} ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</BLOCKQUOTE>")
    await asyncio.sleep(1)
    await message.delete()
    return await Tm.delete()
    


@PY.UBOT("unbl", sudo=True)
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    gc = await EMO.BL_GROUP(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    titit = await client.get_chat(per)
    Tm = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs..</b>")
    blacklist = await get_chat(client.me.id)
    if per not in blacklist:
        return await Tm.edit(
            f"<BLOCKQUOTE>{ggl} grup {titit.title} tidak ada di daftar hitam broadcast</BLOCKQUOTE>"
        )
    try:
        await remove_chat(client.me.id, titit.id)
        return await Tm.edit(
            f"<BLOCKQUOTE><b>{brhsl} dihapus dari daftar hitam broadcast\n{gc} grup: {titit.title}</b></BLOCKQUOTE>"
        )
    except Exception:
        await remove_chat(client.me.id, titit.id)
        return await Tm.edit(
            f"<BLOCKQUOTE><b>{brhsl} dihapus dari daftar hitam broadcast</b></BLOCKQUOTE>"
        )
    except Exception as error:
        return await Tm.edit(f"<blockquote>{ggl} ERROR\n{error}</blockquote>")


@PY.UBOT("rallbl", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"{prs}<b>ᴍᴇᴍᴘʀᴏsᴇs..</b>")
    get_bls = await get_chat(client.me.id)
    if len(get_bls) == 0:
        return await msg.edit(f"{ggl} daftar hitam broadcast anda kosong")
    for X in get_bls:
        await remove_chat(client.me.id, X)
    await msg.edit(f"<BLOCKQUOTE>{brhsl} daftar hitam broadcast berhasil dihapus</BLOCKQUOTE>")


@PY.UBOT("listbl", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    Tm = await message.reply(f"<b>ᴍᴇᴍᴘʀᴏsᴇs..</b>")
    msg = f"<b>❏ total grup yang berada didaftar hitam: {len(await get_chat(client.me.id))}</b>\n\n"
    for X in await get_chat(client.me.id):
        try:
            get = await client.get_chat(X)
            msg += f"<b>├ {get.title}</b> | <code>{get.id}</code>\n"
        except:
            msg += f"├<code> {X}</code>\n"
    await Tm.delete()
    await message.reply(f"<BLOCKQUOTE>{msg}</BLOCKQUOTE>")


@PY.UBOT("blucast", sudo=True)
@PY.PRIVATE
@ubot.on_message(filters.command(["blucast"], "C") & filters.user(DEVS))
async def _(client, message):
    brhsl = EMO.BERHASIL(client)
    ggl = EMO.GAGAL(client)
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
    except Exception as e:
        return await message.reply(f"{ggl}{e}")
    blacklist = await get_list_from_vars(client.me.id, "BLUCAST", "DB_UCAST")
    if chat_id in blacklist:
        return await message.reply(
            f"{ggl}pengguna sudah berada dalam daftar hitam"
        )
    else:
        await add_to_vars(client.me.id, "BLUCAST", chat_id, "DB_UCAST")
        return await message.reply(
            f"{brhsl}pengguna berhasil ditambahkan ke daftar hitam ucast"
        )


@PY.UBOT("delucast")
@PY.PRIVATE
async def _(client, message):
    brhsl = EMO.BERHASIL(client)
    ggl = EMO.GAGAL(client)
    tion = EMO.MENTION(client)
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
    except Exception as e:
        return await message.reply(f"{e}")
    blacklist = await get_list_from_vars(client.me.id, "BLUCAST", "DB_UCAST")
    if chat_id not in blacklist:
        return await message.reply(
            f"{ggl} pengguna tidak berada dalam daftar hitam"
        )
    else:
        await remove_from_vars(client.me.id, "BLUCAST", chat_id, "DB_UCAST")
        return await message.reply(
            f"{brhsl}pengguna berhasil dihapus dari daftar hitam ucast"
        )


@PY.UBOT("listucast")
async def _(client, message):
    msg = await message.reply("memproses")
    ucast = await get_list_from_vars(client.me.id, "BLUCAST", "DB_UCAST")
    Tm = f"<b>❏ daftar hitam ucast</b>\n\n"
    if not ucast:
        return await msg.edit(f"daftar hitam kosong")

    for user_id in ucast:
        try:
            get = await client.get_users(user_id)
            Tm += f"├ {get.first_name} {get.last_name or ''} | <code>{get.id}</code>\n"
        except:
            Tm += f"├ <code>{user_id}</code>\n"
    await msg.delete()
    return await message.reply(f"<BLOCKQUOTE>{Tm}</BLOCKQUOTE>")
