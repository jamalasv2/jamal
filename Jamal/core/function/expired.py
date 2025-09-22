import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from Jamal import bot, ubot
from Jamal.database import (get_chat, get_expired_date,
                                    rem_expired_date, remove_chat, remove_ubot,
                                    rm_all, remove_all_vars, rem_pref, remove_from_vars)
from Jamal.core.helpers import MSG, Button


async def expiredUserbots():
    while True:
        for X in ubot._ubot:
            try:
                time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
                exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
                if time == exp:
                    await X.unblock_user(bot.me.username)
                    for chat in await get_chat(X.me.id):
                        await remove_chat(X.me.id, chat)
                    await rm_all(X.me.id)
                    await remove_ubot(X.me.id)
                    await rem_pref(X.me.id)
                    await remove_all_vars(X.me.id)
                    await rem_expired_date(X.me.id)
                    await remove_from_vars(bot.me.id, "PREM_USERS", X.me.id)
                    ubot._get_my_id.remove(X.me.id)
                    ubot._ubot.remove(X)
                    await X.log_out()
                    await bot.send_message(
                        X.me.id,
                        MSG.EXPIRED_MSG_BOT(X),
                        reply_markup=InlineKeyboardMarkup(Button.expired_button_bot()),
                    )
            except Exception as e:
                print(f"Error: - {X.me.id} - :{str(e)}")
        await asyncio.sleep(10)
