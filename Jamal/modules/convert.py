import asyncio
import os
import io

import cv2
import requests

from pyrogram.enums import MessageMediaType, MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import InputMediaPhoto

from PyroUbot import *

__MODULE__ = "convert"
__HELP__ = """
<BLOCKQUOTE><b>『 bantuan untuk convert 』</b>

❏ perintah : <code>{0}toanime</code> [ balas foto/stiker/gif ]
— untuk merubah foto/stiker/gif menjadi gambar anime

❏ perintah : <code>{0}toimg</code> [ balas stiker / gif ]
— untuk mengubah stiker/gif menjadi foto

❏ perintah : <code>{0}tosticker</code> [ balas foto ]
— untuk mengubah foto menjadi stiker

❏ perintah : <code>{0}togif</code> [ balas ke stiker ]
— untuk mengubah stiker menjadi gif

❏ perintah : <code>{0}toaudio</code> [ balas ke video ]
— untuk mengubah video menjadi audio

❏ perintah : <code>{0}rbg<code/> [ balas ke foto ]
— untuk menghapus latar belakang gambar
  
❏ perintah : <code>{0}blur</code> [ balas ke foto ]
— untuk memberikan efek blur ke gambar
 
❏ perintah : <code>{0}mirror</code> [ balas ke foto ]
— untuk memberikan efek cermin ke gambar
 
❏ perintah : <code>{0}negative</code> [ balas ke foto ]
— untuk memberikan efek negatif ke gambar

❏ perintah : <code>{0}thumb</code> [ balas ke video ]
— untuk mengambil thumbnail dari sebuah video </BLOCKQUOTE>
"""


@PY.UBOT("toanime", sudo=True)
async def _(client, message):
    Tm = await message.reply("<b>memproses...</b>")
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                file = "foto"
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                file = "sticker"
                get_photo = await dl_pic(client, message.reply_to_message)
            elif message.reply_to_message.animation:
                file = "gift"
                get_photo = await dl_pic(client, message.reply_to_message)
            else:
                return await Tm.edit(
                    "<b>mohon balas ke </b> <code>foto/stiker/gif</code>"
                )
        else:
            if message.command[1] in ["foto", "profil", "photo"]:
                chat = (
                    message.reply_to_message.from_user
                    or message.reply_to_message.sender_chat
                )
                file = "foto profil"
                get = await client.get_chat(chat.id)
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
    else:
        if len(message.command) < 2:
            return await Tm.edit(
                "ʙᴀʟᴀs ᴋᴇ ꜰᴏᴛᴏ ᴅᴀɴ sᴀʏᴀ ᴀᴋᴀɴ ᴍᴇʀᴜʙᴀʜ ꜰᴏᴛᴏ ᴀɴᴅᴀ ᴍᴇɴᴊᴀᴅɪ ᴀɴɪᴍᴇ"
            )
        else:
            try:
                file = "foto"
                get = await client.get_chat(message.command[1])
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
            except Exception as error:
                return await Tm.edit(error)
    await Tm.edit("<b>sᴇᴅᴀɴɢ ᴅɪᴘʀᴏsᴇs...</b>")
    await client.unblock_user("@qq_neural_anime_bot")
    send_photo = await client.send_photo("@qq_neural_anime_bot", get_photo)
    await asyncio.sleep(30)
    await send_photo.delete()
    await Tm.delete()
    info = await client.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in client.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(
            InputMediaPhoto(
                anime.photo.file_id, caption=f"<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ: {bot.me.mention}</b>"
            )
        )
    if anime_photo:
        await client.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

    else:
        await client.send_message(
            message.chat.id,
            f"<b>ɢᴀɢᴀʟ ᴍᴇʀᴜʙᴀʜ {file} ᴍᴇɴᴊᴀᴅɪ ɢᴀᴍʙᴀʀ ᴀɴɪᴍᴇ</b>",
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@PY.UBOT("toimg", sudo=True)
async def _(client, message):
    try:
        Tm = await message.reply("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ . . .")
        file_io = await dl_pic(client, message.reply_to_message)
        file_io.name = "sticker.png"
        await client.send_photo(
            message.chat.id,
            file_io,
            reply_to_message_id=message.id,
        )
        await Tm.delete()
    except Exception as e:
        await Tm.delete()
        return await client.send_message(
            message.chat.id,
            e,
            reply_to_message_id=message.id,
        )


@PY.UBOT("thumb")
async def _(client, message):
    msg = message.reply_to_message
    Tm = await message.reply(f"memproses")
    if not msg or not msg.video:
        return await Tm.edit("balas ke media untuk mendownload thumbnail")
    thumbnail = await client.download_media(msg.video.thumbs[-1])
    await client.send_photo(
        message.chat.id,
        photo=thumbnail,
        caption="thumbnail",
        reply_to_message_id=msg.id,
    )
    await Tm.delete()
    os.remove(thumbnail)
    return


@PY.UBOT("tosticker", sudo=True)
async def _(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text("ʀᴇᴘʟʏ ᴋᴇ ꜰᴏᴛᴏ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ᴋᴇ sᴛɪᴄᴋᴇʀ")
        sticker = await client.download_media(
            message.reply_to_message.photo.file_id,
            f"sticker_{message.from_user.id}.webp",
        )
        await message.reply_sticker(sticker)
        os.remove(sticker)
    except Exception as e:
        await message.reply_text(str(e))


@PY.UBOT("togif", sudo=True)
async def _(client, message):
    TM = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    if not message.reply_to_message.sticker:
        return await TM.edit("<b>ʙᴀʟᴀs ᴋᴇ sᴛɪᴋᴇʀ...</b>")
    await TM.edit("<b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ sᴛɪᴄᴋᴇʀ. . .</b>")
    file = await client.download_media(
        message.reply_to_message,
        f"Gift_{message.from_user.id}.mp4",
    )
    try:
        await client.send_animation(
            message.chat.id, file, reply_to_message_id=message.id
        )
        os.remove(file)
        await TM.delete()
    except Exception as error:
        await TM.edit(error)


@PY.UBOT("toaudio", sudo=True)
async def _(client, message):
    replied = message.reply_to_message
    Tm = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
    if not replied:
        return await Tm.edit("<b>ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴠɪᴅᴇᴏ</b>")
    if replied.media == MessageMediaType.VIDEO:
        await Tm.edit("<b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ . . ..</b>")
        file = await client.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await Tm.edit("<b>ᴍᴇɴᴄᴏʙᴀ ᴇᴋsᴛʀᴀᴋ ᴀᴜᴅɪᴏ. ..</b>")
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await run_cmd(cmd)
            await Tm.edit("<b>ᴜᴘʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ . . .</b>")
            await client.send_voice(
                message.chat.id,
                voice=out_file,
                reply_to_message_id=message.id,
            )
            os.remove(file)
            await Tm.delete()
        except Exception as error:
            await Tm.edit(error)
    else:
        return await Tm.edit("<b>ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴠɪᴅᴇᴏ</b>")
