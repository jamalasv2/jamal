import random
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import (InlineKeyboardMarkup, InlineQueryResultArticle,
                            InputTextMessageContent)

from PyroUbot.core import *
from PyroUbot.core.database import *
from PyroUbot import *


@PY.UBOT("alive", sudo=True)
async def _(client, message):
    x = await client.get_inline_bot_results(
        bot.me.username, f"alive {message.id} {client.me.id}"
    )
    await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)


@PY.INLINE("^alive")
@INLINE.QUERY
async def _(client, inline_query):
    get_id = inline_query.query.split()
    for my in ubot._ubot:
        if int(get_id[2]) == my.me.id:
            try:
                peer = my._get_my_peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await get_expired_date(my.me.id)
            exp = get_exp.strftime("%d-%m-%Y")
            if my.me.id == OWNER_ID:
                status = "<code>[ғᴏᴜɴᴅᴇʀ]</code>"
            elif my.me.id in await get_list_from_vars(client.me.id, "SELER_USERS"):
                status = "<code>[sᴇʟʟᴇʀ]</code>"
            else:
                status = "[ᴜsᴇʀ]"
            button = Button.alive(get_id)
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            msg = f"""
<BLOCKQUOTE><b><a href=tg://user?id={my.me.id}>{my.me.first_name} {my.me.last_name or ''}</a>
sᴛᴀᴛᴜs: {status} 
 ᴇxᴘɪʀᴇᴅ_ᴏɴ: <code>{exp}</code> 
 ᴅᴄ_ɪᴅ: <code>{my.me.dc_id}</code>
 ᴘɪɴɢ_ᴅᴄ: <code>{ping} ᴍs</code>
 ᴘᴇᴇʀ_ᴜsᴇʀs: <code>{users} ᴜsᴇʀs</code>
 ᴘᴇᴇʀ_ɢʀᴏᴜᴘ: <code>{group} ɢʀᴏᴜᴘ</code>
 sᴛᴀʀᴛ_ᴜᴘᴛɪᴍᴇ: <code>{uptime}</code></b></BLOCKQUOTE>
"""
            await client.answer_inline_query(
                inline_query.id,
                cache_time=300,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="💬",
                            reply_markup=InlineKeyboardMarkup(button),
                            input_message_content=InputTextMessageContent(msg),
                        )
                    )
                ],
            )


@PY.CALLBACK("alv_cls")
@INLINE.DATA
async def _(client, callback_query):
    get_id = callback_query.data.split()
    my_id = []
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for my in ubot._ubot:
        my_id.append(my.me.id)
    if callback_query.from_user.id in my_id:
        await my.delete_messages(
            unPacked.chat_id, unPacked.message_id
        )
