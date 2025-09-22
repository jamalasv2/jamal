from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Jamal import OWNER_ID, bot, get_expired_date, ubot


class MSG:
    def DEAK(X):
        return f"""
<b>ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>
<b>ᴀᴋᴜɴ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ɪᴅ:</b> <code>{X.me.id}</code>
<b>ʀᴇᴀsᴏɴ:</b> <code>ᴅɪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴛᴇʟᴇɢʀᴀᴍ</code>
"""
            
    def EXPIRED_MSG_BOT(X):
        return f"""
<BLOCKQUOTE><b>ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>
<b>ᴀᴋᴜɴ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ɪᴅ:</b> <code>{X.me.id}</code>
<b>ᴇxᴘɪʀᴇᴅ: ᴛᴇʟᴀʜ ʜᴀʙɪs</b></BLOCKQUOTE>
"""

    
    def START(message):
        return f"""
<BLOCKQUOTE><b>ʜᴀʟᴏ <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

<b>{bot.me.mention}</b> ᴀᴅᴀʟᴀʜ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ʙᴇʙᴇʀᴀᴘᴀ ғɪᴛᴜʀ ʏᴀɴɢ ᴀᴋᴀɴ ᴍᴇᴍᴜᴅᴀʜᴋᴀɴ sᴇʙᴀɢɪᴀɴ ᴋᴇʙᴜᴛᴜʜᴀɴᴍᴜ ᴅɪ ᴛᴇʟᴇɢʀᴀᴍ sᴇᴘᴇʀᴛɪ: ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀsᴛ, ᴏᴘᴇɴᴀɪ, ᴅᴏᴡɴʟᴏᴀᴅᴇʀ, ᴄᴀᴛᴀᴛᴀɴ, ᴅsʙ. ᴜsᴇʀʙᴏᴛ ɪɴɪ ʙɪsᴀ ᴋᴀʟɪᴀɴ ʙᴜᴀᴛ ᴅᴀɴ ᴋᴀʟɪᴀɴ ɢᴜɴᴀᴋᴀɴ ᴅᴇɴɢᴀɴ sᴀɴɢᴀᴛ ᴍᴜᴅᴀʜ.</BLOCKQUOTE>
"""

    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<BLOCKQUOTE><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

<b>🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: {harga}.000</b>

<b>💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:</b>
 <b>├──• ᴅᴀɴᴀ </b>
 <b>├─• <code>‪085603220147</code></b>
 <b>└──• <a href=https://link.dana.id/qr/c7g8ia1o>ᴋʟɪᴋ ᴅɪsɪɴɪ</a></b>

<b>🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: ʀᴘ {total}.000</b>
<b>🗓️ ᴛᴏᴛᴀʟ ʙᴜʟᴀɴ: {bulan}</b> 

<b>✅ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜɴᴛᴜᴋ ᴋɪʀɪᴍ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ</b></BLOCKQUOTE>
"""

    async def USERBOT(count):
        return f"""
<b>ᴜsᴇʀʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>ᴀᴋᴜɴ:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b>ɪᴅ:</b> <code>{ubot._ubot[int(count)].me.id}</code>
"""

    def POLICY():
        return """
<BLOCKQUOTE>↪️ ᴋᴇʙɪᴊᴀᴋᴀɴ ᴘᴇɴɢᴇᴍʙᴀʟɪᴀɴ

✅ sᴇᴛᴇʟᴀʜ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ, ᴊɪᴋᴀ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍᴘᴇʀᴏʟᴇʜ/
ᴍᴇɴᴇʀɪᴍᴀ ᴍᴀɴꜰᴀᴀᴛ ᴅᴀʀɪ ᴘᴇᴍʙᴇʟɪᴀɴ, 
ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʜᴀᴋ ᴘᴇɴɢɢᴀɴᴛɪᴀɴ ᴅᴀʟᴀᴍ ᴡᴀᴋᴛᴜ 2 ʜᴀʀɪ sᴇᴛᴇʟᴀʜ ᴘᴇᴍʙᴇʟɪᴀɴ. ɴᴀᴍᴜɴ, ᴊɪᴋᴀ 
ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ/ᴍᴇɴᴇʀɪᴍᴀ sᴀʟᴀʜ sᴀᴛᴜ ᴍᴀɴꜰᴀᴀᴛ ᴅᴀʀɪ 
ᴘᴇᴍʙᴇʟɪᴀɴ, ᴛᴇʀᴍᴀsᴜᴋ ᴀᴋsᴇs ᴋᴇ ꜰɪᴛᴜʀ ᴘᴇᴍʙᴜᴀᴛᴀɴ ᴜsᴇʀʙᴏᴛ, ᴍᴀᴋᴀ 
ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʟᴀɢɪ ʙᴇʀʜᴀᴋ ᴀᴛᴀs ᴘᴇɴɢᴇᴍʙᴀʟɪᴀɴ ᴅᴀɴᴀ.

🆘 ᴅᴜᴋᴜɴɢᴀɴ
ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴅᴜᴋᴜɴɢᴀɴ, ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ:
• ᴍᴇɴɢʜᴜʙᴜɴɢɪ ᴀᴅᴍɪɴ : roronoajamalsv2.t.me
• sᴜᴘᴘᴏʀᴛ jamalsupportt.t.me ᴅɪ ᴛᴇʟᴇɢʀᴀᴍ

👉🏻 ᴛᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ʟᴀɴᴊᴜᴛᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴʏᴀᴛᴀᴋᴀɴ ʙᴀʜᴡᴀ ᴀɴᴅᴀ ᴛᴇʟᴀʜ 
ᴍᴇᴍʙᴀᴄᴀ ᴅᴀɴ ᴍᴇɴᴇʀɪᴍᴀ ᴋᴇᴛᴇɴᴛᴜᴀɴ ɪɴɪ ᴅᴀɴ ᴍᴇʟᴀɴᴊᴜᴛᴋᴀɴ 
ᴘᴇᴍʙᴇʟɪᴀɴ. ᴊɪᴋᴀ ᴛɪᴅᴀᴋ, ᴛᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ʙᴀᴛᴀʟᴋᴀɴ.</BLOCKQUOTE>
"""


async def sending_user(user_id):
        await bot.send_message(
            user_id,
            "💬 sɪʟᴀʜᴋᴀɴ ʙᴜᴀᴛ ᴜʟᴀɴɢ ᴜsᴇʀʙᴏᴛ ᴀɴᴅᴀ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔥 ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ 🔥",
                            callback_data="bahan",
                        )
                    ],
                ]
            ),
            disable_web_page_preview=True,
        )
