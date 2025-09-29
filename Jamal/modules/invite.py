import asyncio

from pyrogram.enums import UserStatus

from PyroUbot import *

__MODULE__ = "invite"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɪɴᴠɪᴛᴇ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}invite</code> [ᴜsᴇʀɴᴀᴍᴇ] 
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜɴᴅᴀɴɢ ᴀɴɢɢᴏᴛᴀ ᴋᴇ ɢʀᴜᴘ ᴀɴᴅᴀ

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}inviteall</code> [ᴜsᴇʀɴᴀᴍᴇ_ɢʀᴏᴜᴘ - ᴄᴏʟʟᴅᴏᴡɴ=ᴅᴇᴛɪᴋ ᴘᴇʀ ɪɴᴠɪᴛᴇ]
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜɴᴅᴀɴɢ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ᴏʙʀᴏʟᴀɴ ɢʀᴜᴘ ʟᴀɪɴ ᴋᴇ ᴏʙʀᴏʟᴀɴ ɢʀᴜᴘ ᴀɴᴅᴀ

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}cancel</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴᴠɪᴛᴇᴀʟʟ
  """


@PY.UBOT("invite", sudo=True)
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    mg = await message.reply(f"{prs} memproses..")
    if len(message.command) < 2:
        return await mg.edit(f"{ggl} berikan nama pengguna atau id pengguna")

    try:
        chat = await client.get_chat(per)
    except:
        pass
    user_to_add = message.text.split(" ", 1)[1]
    if not user_to_add:
        return await mg.edit(f"{ggl} berikan nama pengguna untuk ditambahkan!")
    user_list = user_to_add.split(" ")
    try:
        await client.add_chat_members(chat, user_list, forward_limit=100)
    except Exception as e:
        return await mg.edit(f"{ggl} ERROR:\n{e}")
    await mg.edit(f"{brhsl} berhasil menambahkan {len(user_list)} ke {chat.title}")


invite_id = []


@PY.UBOT("inviteall", sudo=True)
@PY.GROUP
@PY.TOP_CMD
async def _(client, message):
    Tm = await message.reply("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
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
