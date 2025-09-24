from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Jamal import *
from langs import bhs

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
        return bhs("pay_text")

    async def USERBOT(count):
        if not ubot._ubot:  # list kosong
            return "<b>Tidak ada userbot yang aktif.</b>"

        if int(count) >= len(ubot._ubot):  # index kelewat panjang
            return f"<b>Index {count} di luar jangkauan. Total userbot: {len(ubot._ubot)}</b>"

        ub = ubot._ubot[int(count)]
        return f"""
<b>ᴜsᴇʀʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>ᴀᴋᴜɴ:</b> <a href=tg://user?id={ub.me.id}>{ub.me.first_name} {ub.me.last_name or ''}</a> 
<b>ɪᴅ:</b> <code>{ub.me.id}</code>
"""

    def POLICY():
        return bhs("start_2")


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
