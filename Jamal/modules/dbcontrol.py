from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from PyroUbot.core.database import *

from PyroUbot import *


@PY.BOT("prem")
@PY.SELLER
async def _(client, message):
    msg = await message.reply("<b>memproses</b>")
    user_id, get_bulan = await extract_user_and_reason(message)
    chatt = -1002937213790
    thread = 4
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(
            f"<BLOCKQUOTE><b>» nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n» id: {user.id}\n» keterangan: <code>sudah memiliki akses</code></b></BLOCKQUOTE>"
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "PREM_USERS", user.id)
        await msg.edit(
            f"<BLOCKQUOTE><b>» nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n» id: {user.id}\n» keterangan: <code>premium {get_bulan} bulan</code></b>"
        )
        return await bot.send_message(
            chatt,
            f"<b>seller: <a href=tg://openmessage?user_id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\ncustomer: <a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a>\ndurasi: {get_bulan} bulan</b>",
            message_thread_id=thread,
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unprem")
@PY.SELLER
async def _(client, message):
    msg = await message.reply("<b>memproses...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} nama pengguna / id pengguna</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(
            f"<BLOCKQUOTE><b>» nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n» id: {user.id}\n» keterangan: <code>tidak dalam daftar</code></b></BLOCKQUOTE>"
        )

    try:
        await remove_from_vars(bot.me.id, "PREM_USERS", user.id)
        return await msg.edit(
            f"<BLOCKQUOTE><b>» nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n» id: {user.id}\n» keterangan: <code>unpremium</code></b></BLOCKQUOTE>"
        )
    except Exception as error:
        return await msg.edit(error)
        

@PY.BOT("getprem")
@PY.SELLER
async def _(client, message):
    prem = await get_list_from_vars(client.me.id, "PREM_USERS")
    msg = f"<b>total pengguna premium: {len(prem)}</b>\n\n"

    if not prem:
        return await message.reply(f"tidak ada pengguna premium")

    for user_id in prem:
        try:
            user = await client.get_users(user_id)
            msg += f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>\n"
        except:
            msg += f"<code>{user_id}</code>\n"
    return await message.reply(f"<blockquote>{msg}</blockquote>")


@PY.BOT("rallprem")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("memproses...")
    prem = await get_list_from_vars(client.me.id, "PREM_USERS")
    done = 0

    if len(prem) == 0:
        return await message.reply("tidak ada pengguna premium")

    for user_id in prem:
        await remove_from_vars(bot.me.id, "PREM_USERS", user_id)
        done += 1
    await msg.edit(f"berhasil menghapus {done} pengguna premium")


@PY.BOT("seles")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id in sudo_users:
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>sudah seller</code></b>"
        )

    try:
        await add_to_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>seller</code></b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unseles")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>tida dalam daftar</code></b>"
        )

    try:
        await remove_from_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>unseller</code></b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getseles")
@PY.ADMIN
async def _(client, message):
    Sh = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit("<s>ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ ᴋᴏsᴏɴɢ</s>")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f" •> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if seles_list:
        response = (
            "<b>❏ ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ:</b>\n\n"
            + "\n".join(seles_list)
            + f"\n\n<b>❏ ᴛᴏᴛᴀʟ sᴇʟʟᴇʀ:</b> <code>{len(seles_list)}</code>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ</b>")


@PY.BOT("time")
@PY.SELLER
async def _(client, message):
    Tm = await message.reply("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    user_id, get_day = await extract_user_and_reason(message)
    user = await client.get_users(user_id)
    if not user_id:
        return await Tm.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ - ʜᴀʀɪ</b>")
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"•> ɴᴀᴍᴇ: {user.mention}\n•> ɪᴅ: {get_id}\n•> ᴀᴋᴛɪғᴋᴀɴ_sᴇʟᴀᴍᴀ: {get_day} ʜᴀʀɪ")


@PY.BOT("cek")
async def _(client, message):
    Sh = await message.reply("<b>memproses . . .</b>")
    user_id = await extract_user(message)
    get = await get_expired_date(user_id)
    if not user_id:
        return await Sh.edit("pengguna tidak ditemukan")
    try:
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
    if get is None:
        await Sh.edit(f"{user_id} belum diaktifkan.")
    else:
        SH = await ubot.get_prefix(user_id)
        remaining_days = (get - datetime.now()).days
        await Sh.edit(
            f"<BLOCKQUOTE>‣ nama: {sh.mention}\n‣ id: {user_id}\n‣ prefix: {' '.join(SH)}\n‣ waktu tersisa:{remaining_days} hari</BLOCKQUOTE>"
        )


@PY.BOT("untime")
@PY.SELLER
async def _(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("</b>memproses. . .</b>")
    if not user_id:
        return await Tm.edit("<b>pengguna tidak ditemukan</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    await rem_expired_date(user.id)
    return await Tm.edit(f"<b>{user.mention} expired berhasil dihapus</b>")


@PY.BOT("admin")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>sudah admin</code></b>"
        )

    try:
        await add_to_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>admin</code></b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unadmin")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>tida dalam daftar</code></b>"
        )

    try:
        await remove_from_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(
            f"<b>•> ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})\n•> ɪᴅ: {user.id}\n•> ᴋᴇᴛᴇʀᴀɴɢᴀɴ: <code>unadmin</code></b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getadmin")
@PY.OWNER
async def get_admin(client, message):
    Sh = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<s>ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ ᴋᴏsᴏɴɢ</s>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f" •> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if admin_list:
        response = (
            "<b>❏ ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ:</b>\n\n"
            + "\n".join(admin_list)
            + f"\n\n<b>❏ ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴ:</b> <code>{len(admin_list)}</code>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ</b>")

