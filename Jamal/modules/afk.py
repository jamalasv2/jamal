from time import time

from Jamal import *
from Jamal.core.helpers._client import PY
from langs import bhs, get_bhs


__MODULE__ = "afk"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀғᴋ 』</b>

<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}afk</code> [ᴀʟᴀsᴀɴ]
 <i>ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋᴛɪғᴋᴀɴ ᴀғᴋ</i>

<b>❏ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}unafk</code>
 <i>ᴜɴᴛᴜᴋ ᴍᴇɴᴏɴᴀᴋᴛɪғᴋᴀɴ ᴀғᴋ</i>
"""


@PY.UBOT("afk")
async def _(client, message):
    reason = get_arg(message)
    db_afk = {"time": time(), "reason": reason}
    emot_1 = await get_vars(client.me.id, "EMOJI_AFK")
    emot_2 = await get_vars(client.me.id, "EMOJI_REASON")
    emot_afk = emot_1 if emot_1 else "5467890025217661107"
    emot_reason = emot_2 if emot_2 else "5334882760735598374"
    if client.me.is_premium:
        msg_afk = (
            f"<b><emoji id={emot_afk}>‼️</emoji>sᴇᴅᴀɴɢ ᴀғᴋ\n<emoji id={emot_reason}>📝</emoji>ᴀʟᴀsᴀɴ: {reason}</b>"
            if reason
            else f"<b><emoji id={emot_afk}>‼️</emoji>sᴇᴅᴀɴɢ ᴀғᴋ</b>"
        )
    else:
        msg_afk = (
            f"<b>sᴇᴅᴀɴɢ ᴀғᴋ\nᴀʟᴀsᴀɴ: {reason}</b>"
            if reason
            else "<b>sᴇᴅᴀɴɢ ᴀғᴋ</b>"
        )
    await set_vars(client.me.id, "AFK", db_afk)
    return await message.reply(msg_afk)



@PY.AFK()
async def _(client, message):
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        emot_1 = await get_vars(client.me.id, "EMOJI_AFK")
        emot_2 = await get_vars(client.me.id, "EMOJI_REASON")
        emot_3 = await get_vars(client.me.id, "EMOJI_WAKTU")
        emot_afk = emot_1 if emot_1 else "5467890025217661107"
        emot_reason = emot_2 if emot_2 else "5334882760735598374"
        emot_waktu = emot_3 if emot_3 else "5316615057939897832"
        if client.me.is_premium:
            afk_text = (
                f"<b><emoji id={emot_afk}>‼️</emoji>sᴇᴅᴀɴɢ ᴀғᴋ\n<emoji id={emot_waktu}>⏰</emoji>ᴡᴀᴋᴛᴜ: {afk_runtime}\n<emoji id={emot_reason}>🏓</emoji>ᴀʟᴀsᴀɴ: {afk_reason}</b>"
                if afk_reason
                else f"<b><emoji id={emot_afk}>‼️</emoji>sᴇᴅᴀɴɢ ᴀғᴋ\n<emoji id={emot_waktu}>⏰</emoji>ᴡᴀᴋᴛᴜ: {afk_runtime}</b>"
            )
        else:
            afk_text = (
                f"<b>sᴇᴅᴀɴɢ ᴀғᴋ\nᴡᴀᴋᴛᴜ: {afk_runtime}\nᴀʟᴀsᴀɴ: {afk_reason}</b>"
                if afk_reason
                else f"<b>sᴇᴅᴀɴɢ ᴀғᴋ\nᴡᴀᴋᴛᴜ: {afk_runtime}</b>"
            )
        return await message.reply(afk_text)


@PY.UBOT("unafk")
@PY.TOP_CMD
async def _(client, message):
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_runtime = await get_time(time() - afk_time)
        emot_1 = await get_vars(client.me.id, "EMOJI_AFK")
        emot_2 = await get_vars(client.me.id, "EMOJI_WAKTU")
        emot_afk = emot_1 if emot_1 else "5467890025217661107"
        emot_waktu = emot_2 if emot_2 else "5316615057939897832"
        if client.me.is_premium:
            afk_text = f"<b><emoji id={emot_afk}>‼️</emoji>ᴋᴇᴍʙᴀʟɪ ᴏɴʟɪɴᴇ\n<emoji id={emot_waktu}>⏰</emoji>ᴀғᴋ sᴇʟᴀᴍᴀ: {afk_runtime}</b>"
        else:
            afk_text = f"<b>ᴋᴇᴍʙᴀʟɪ ᴏɴʟɪɴᴇ\nᴀғᴋ sᴇʟᴀᴍᴀ: {afk_runtime}</b>"
        await message.reply(afk_text)
        return await remove_vars(client.me.id, "AFK")
