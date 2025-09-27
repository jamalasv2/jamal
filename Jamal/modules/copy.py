import asyncio
import os
import time

from gc import get_objects
from time import time

from pyrogram.types import *
from pyrogram.raw.functions.messages import DeleteHistory

from PyroUbot import *

__MODULE__ = "copy"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴏᴘʏ 』</b>

<BLOCKQUOTE>❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}copy</code> [ʟɪɴᴋ_ᴋᴏɴᴛᴇɴ_ᴛᴇʟᴇɢʀᴀᴍ]</BLOCKQUOTE>
<BLOCKQUOTE>ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴍʙɪʟ ᴘᴇsᴀɴ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇʟᴀʟᴜɪ ʟɪɴᴋ ᴍᴇʀᴇᴋᴀ</BLOCKQUOTE>

<BLOCKQUOTE>❏ ᴘᴇʀɪɴᴛᴀʜ: <code>{0}curi</code></BLOCKQUOTE>
<BLOCKQUOTE>ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴍʙɪʟ ᴍᴇᴅɪᴀ sᴇᴋᴀʟɪ ʟɪʜᴀᴛ ᴀᴛᴀᴜ ᴛɪᴍᴇʀ ᴅᴀɴ ᴍᴇɴʏɪᴍᴘᴀɴɴʏᴀ ᴅɪ ᴘᴇsᴀɴ ᴛᴇʀsɪᴍᴘᴀɴ</BLOCKQUOTE>

  """


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "ᴋʙ", 2: "ᴍʙ", 3: "ɢʙ", 4: "ᴛʙ"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}"


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} ʜᴀʀɪ, " if days else "")
        + (f"{str(hours)} ᴊᴀᴍ, " if hours else "")
        + (f"{str(minutes)} ᴍᴇɴɪᴛ, " if minutes else "")
        + (f"{str(seconds)} ᴅᴇᴛɪᴋ, " if seconds else "")
        + (f"{str(milliseconds)} ᴍɪᴋʀᴏᴅᴇᴛɪᴋ, " if milliseconds else "")
    )
    return tmp[:-2]


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("•" for _ in range(math.floor(percentage / 10))),
            "".join("~" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nᴇsᴛɪᴍᴀsɪ: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    f"""
<BLOCKQUOTE><b>{type_of_ps}</b>

<b>ғɪʟᴇ_ɪᴅ:</b> <code>{file_name}</code>

<b>{tmp}</b></BLOCKQUOTE>
"""
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(f"{type_of_ps}\n{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


async def download_media(get, client, info, message):
    msg = message.reply_to_message or message
    text = get.caption or ""

    if get.photo:
        media = await client.download_media(
            get,
            progress=progress,
            progress_args=(
                info,
                time(),
                "download photo",
                get.photo.file_id,
            ),
        )
        await client.send_photo(
            message.chat.id,
            photo=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
        await info.delete()
        os.remove(media)

    elif get.animation:
        media = await client.download_media(
            get,
            progress=progress,
            progress_args=(
                info,
                time(),
                "download animation",
                get.animation.file_id,
            ),
        )
        await client.send_animation(
            message.chat.id,
            animation=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
        await info.delete()
        os.remove(media)

    elif get.audio:
        media = await client.download_media(
            get,
            progress=progress,
            progress_args=(
                info,
                time(),
                "download audio",
                get.audio.file_id,
            ),
        )
        thumbnail = await client.download_media(get.audio.thumbs[-1] or None)
        await client.send_audio(
            message.chat.id,
            audio=media,
            duration=get.audio.duration,
            caption=text,
            thumb=thumbnail,
            reply_to_message_id=msg.id,
        )
        await info.delete()
        os.remove(media)
        os.remove(thumbnail)

    elif get.voice:
        media = await client.download_media(
            get,
            progress=progress,
            progress_args=(
                info,
                time(),
                "download voice",
                get.voice.file_id,
            ),
        )
        await client.send_voice(
            message.chat.id,
            voice=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
        await info.delete()
        os.remove(media)

    elif get.document:
        media = await client.download_media(
            get,
            progress=progress,
            progress_args=(
                info,
                time(),
                "download document",
                get.document.file_id,
            ),
        )
        await client.send_document(
            message.chat.id,
            document=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
        await info.delete()
        os.remove(media)

    elif get.video:
        media = await client.download_media(
            get,
            progress=progress,
            progress_args=(
                info,
                time(),
                "download video",
                get.video.file_id,
            ),
        )
        thumbnail = await client.download_media(get.video.thumbs[-1]) or None
        await client.send_video(
            message.chat.id,
            video=media,
            duration=get.video.duration,
            caption=text,
            thumb=thumbnail,
            reply_to_message_id=msg.id,
        )
        await info.delete()
        os.remove(media)
        os.remove(thumbnail)
        del COPY_ID[client.me.id]


COPY_ID = {}

@PY.UBOT("copy", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = message.reply_to_message or message
    info = await message.reply(f"{prs}ᴍᴇᴍᴘʀᴏsᴇs")
    link = get_arg(message)
    if not link:
        return await info.edit(
            f"<b><code>{ggl}{message.text}</code> [ʟɪɴᴋ_ᴋᴏɴᴛᴇɴ_ᴛᴇʟᴇɢʀᴀᴍ]</b>"
        )
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            chat = int("-100" + str(link.split("/")[-2]))
            try:
                get = await client.get_messages(chat, msg_id)
                try:
                    await get.copy(message.chat.id, reply_to_message_id=msg.id)
                    await info.delete()
                except Exception:
                    await download_media(get, client, info, message)
            except Exception as e:
                await info.edit(f"{str(e)}")
        else:
            chat = str(link.split("/")[-2])
            try:
                get = await client.get_messages(chat, msg_id)
                try:
                    await get.copy(message.chat.id, reply_to_message_id=msg.id)
                    await info.delete()
                except Exception:
                    await download_media(get, client, info, message)
            except Exception as e:
                await info.edit(f"{str(e)}")

    else:
        await info.edit(f"{ggl} link yang anda masukkan tidak valid")


@PY.UBOT("curi")
@PY.PRIVATE
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    dia = message.reply_to_message
    if not dia:
        return await message.reply(f"{ggl}ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴍᴇᴅɪᴀ")
    titit = dia.caption or ""
    if dia.photo:
        if dia.photo.file_size > 100000000:
            return await message.reply(f"{ggl}ꜰɪʟᴇ ᴅɪ ᴀᴛᴀs 100ᴍʙ ᴛɪᴅᴀᴋ ᴅɪ ɪᴢɪɴᴋᴀɴ")
        tetek = await client.download_media(dia)
        await message.delete()
        return await client.send_photo(client.me.id, tetek, titit)
        os.remove(tetek)
    if dia.video:
        if dia.video.file_size > 100000000:
            return await message.reply(f"{ggl}ꜰɪʟᴇ ᴅɪ ᴀᴛᴀs 100ᴍʙ ᴛɪᴅᴀᴋ ᴅɪ ɪᴢɪɴᴋᴀɴ")
        nenen = await client.download_media(dia)
        await message.delete()
        return await client.send_video(client.me.id, nenen, titit)
        os.remove(nenen)
    if dia.audio:
        if dia.audio.file_size > 100000000:
            return await message.reply(f"{ggl}ꜰɪʟᴇ ᴅɪ ᴀᴛᴀs 100ᴍʙ ᴛɪᴅᴀᴋ ᴅɪ ɪᴢɪɴᴋᴀɴ")
        nenen = await client.download_media(dia)
        await message.delete()
        return await client.send_audio(client.me.id, nenen, titit)
        os.remove(nenen)
    if dia.voice:
        if dia.voice.file_size > 100000000:
            return await message.reply(f"{ggl}ꜰɪʟᴇ ᴅɪ ᴀᴛᴀs 100ᴍʙ ᴛɪᴅᴀᴋ ᴅɪ ɪᴢɪɴᴋᴀɴ")
        nenen = await client.download_media(dia)
        await message.delete()
        return await client.send_voice(client.me.id, nenen, titit)
        os.remove(nenen)
    if dia.document:
        if dia.document.file_size > 100000000:
            return await message.reply(f"{ggl}ꜰɪʟᴇ ᴅɪ ᴀᴛᴀs 100ᴍʙ ᴛɪᴅᴀᴋ ᴅɪ ɪᴢɪɴᴋᴀɴ")
        nenen = await client.download_media(dia)
        await message.delete()
        return await client.send_document(client.me.id, nenen, titit)
        os.remove(nenen)
    else:
        return await message.reply(f"{ggl}sᴇᴘᴇʀᴛɪɴʏᴀ ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ")
