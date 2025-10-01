import asyncio

from pyrogram.enums import UserStatus

from Jamal.core.helpers.class_emoji import get_emo
from Jamal.core.helpers._client import PY
from langs import bhs, get_bhs


__MODULE__ = "invite"
__HELP__ = get_bhs("invite_cmd")


@PY.UBOT("invite", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    mg = await message.reply(bhs("text_proses".format(em.proses))
    if len(message.command) < 2:
        return await mg.edit(bhs("invite_nolen").format(em.gagal))

    user_to_add = message.text.split(" ", 1)[1]
    if not user_to_add:
        return await mg.edit(bhs("invite_nolen").format(em.gagal))
    user_list = user_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except Exception as e:
        return await mg.edit(bhs("text_error").format(em.gagal, e)
    await mg.edit(bhs("invite_sukses").format(em.berhasil, len(user_list), message.chat.title))


invite_id = []


@PY.UBOT("inviteall", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    Tm = await message.reply(bhs("text_proses").format(em.proses))
    if len(message.command) < 3:
        await message.delete()
        return await Tm.delete()
    try:
        chat = await client.get_chat(message.command[1])
    except Exception as error:
        return await Tm.edit(error)
    if message.chat.id in invite_id:
        return await Tm.edit_text(
            f"sᴇᴅᴀɴɢ ᴍᴇɴɢɪɴᴠɪᴛᴇ ᴍᴇᴍʙᴇʀ sɪʟᴀʜᴋᴀɴ ᴄᴏʙᴀ ʟᴀɢɪ ɴᴀɴᴛɪ ᴀᴛᴀᴜ ɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ: <code>{PREFIX[0]}cancel</code>"
        )
    else:
        done = 0
        failed = 0
        invite_id.append(message.chat.id)
        await Tm.edit_text(f"ᴍᴇɴɢᴜɴᴅᴀɴɢ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ {chat.title}")
        async for member in client.get_chat_members(chat.id):
            stats = [
                UserStatus.ONLINE,
                UserStatus.OFFLINE,
                UserStatus.RECENTLY,
                UserStatus.LAST_WEEK,
            ]
            if member.user.status in stats:
                try:
                    await client.add_chat_members(message.chat.id, member.user.id)
                    done = done + 1
                    await asyncio.sleep(int(message.command[2]))
                except Exception:
                    failed = failed + 1
                    await asyncio.sleep(int(message.command[2]))
        invite_id.remove(message.chat.id)
        await Tm.delete()
        return await message.reply(
            f"""
<b><code>{done}</code> ᴀɴɢɢᴏᴛᴀ ʏᴀɴɢ ʙᴇʀʜᴀsɪʟ ᴅɪᴜɴᴅᴀɴɢ</b>
<b><code>{failed}</code> ᴀɴɢɢᴏᴛᴀ ʏᴀɴɢ ɢᴀɢᴀʟ ᴅɪᴜɴᴅᴀɴɢ</b>
"""
        )


@PY.UBOT("cancel", sudo=True)
@PY.GROUP
@PY.TOP_CMD
async def _(client, message):
    if message.chat.id not in invite_id:
        return await message.reply_text(
            f"sᴇᴅᴀɴɢ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀɪɴᴛᴀʜ: <code>{PREFIX[0]}inviteall</code> ʏᴀɴɢ ᴅɪɢᴜɴᴀᴋᴀɴ"
        )
    try:
        invite_id.remove(message.chat.id)
        await message.reply_text("ok inviteall berhasil dibatalkan")
    except Exception as e:
        await message.reply_text(e)
