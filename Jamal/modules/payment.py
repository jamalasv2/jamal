import asyncio
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from Jamal import *
from Jamal.database import *
from langs import bhs

CONFIRM_PAYMENT = []


@PY.CALLBACK("^confirm")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    CONFIRM_PAYMENT.append(get.id)
    try:
        button = [[InlineKeyboardButton(bhs("cb_cancel"), callback_data=f"home {user_id}")]]
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            bhs("pay_bukti"),
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError as out:
        if get.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get.id)
            buttonx = [[InlineKeyboardButton(bhs("cb_cls"), callback_data=f"0_cls")]]
            await pesan.request.edit(
                bhs("pay_bukti"),
                reply_markup=InlineKeyboardMarkup(buttonx),
            )
            return await bot.send_message(get.id, bhs("pay_cancel"))
    if get.id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            buttons = [[InlineKeyboardButton(bhs("cb_confirm"), callback_data="confirm")]]
            return await bot.send_message(
                bhs("pay_invalid"),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif pesan.photo:
            buttons = Button.button_add_expired(get.id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(get.id)
            buttonz = [[InlineKeyboardButton(bhs("cb_cls"), callback_data=f"0_cls")]]
            await pesan.request.edit(
                bhs("pay_bukti"),
                reply_markup=InlineKeyboardMarkup(buttonz),
            )
            return await bot.send_message(
                user_id,
                bhs("pay_proses")
            )


@PY.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 20
    QUERY = callback_query.data.split()[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
                TOTAL_HARGA = HARGA * BULAN
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
                TOTAL_HARGA = HARGA * BULAN
        buttons = Button.plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.edit_text(
            MSG.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except:
        pass


@PY.CALLBACK("^(success|failed|home)")
async def _(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton(bhs("cb_install"), callback_data="memek")],
        ]
        await bot.send_message(
            get_user.id,
            bhs("pay_valid"),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton(bhs("cb_cls"), callback_data=f"0_cls")
            ],
        ]
        await add_to_vars(client.me.id, "PREM_USERS", get_user.id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(query[2]))
        await set_expired_date(get_user.id, expired)
        return await callback_query.edit_message_text(
            f"""
<b>✅ {get_user.first_name} {get_user.last_name or ''} ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴɢɢᴏᴛᴀ ᴘʀᴇᴍɪᴜᴍ</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_success),
        )
    if query[0] == "failed":
        buttons = [
            [
                InlineKeyboardButton(
                    bhs("pay"), callback_data="bayar_dulu"
                )
            ],
        ]
        await bot.send_message(
            get_user.id,
            bhs("pay_invalid"),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton(bhs("cb_cls"), callback_data=f"0_cls")
            ],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>❌ {get_user.first_name} {get_user.last_name or ''} ᴛɪᴅᴀᴋ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴɢɢᴏᴛᴀ ᴘʀᴇᴍɪᴜᴍ</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_failed),
        )
    if query[0] == "home":
        if get_user.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get_user.id)
            buttons_home = Button.start(callback_query)
            return await callback_query.edit_message_text(
                bhs("start_1"),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
        else:
            buttons_home = Button.start(callback_query)
            return await callback_query.edit_message_text(
                bhs("start_1"),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
