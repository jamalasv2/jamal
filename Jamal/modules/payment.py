import asyncio
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from Jamal import *
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
            return await bot.send_message(get.id, "ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs")
    if get.id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            buttons = [[InlineKeyboardButton(bhs("cb_confirm"), callback_data="confirm")]]
            return await bot.send_message(
                user_id,
                """
<b>❌ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴅɪᴘʀᴏsᴇs</b>

<b>💬 ʜᴀʀᴀᴘ ᴋɪʀɪᴍᴋᴀɴ sᴄʀᴇᴇɴsʜᴏᴛ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ʏᴀɴɢ ᴠᴀʟɪᴅ</b>

<b>✅ sɪʟᴀʜᴋᴀɴ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜʟᴀɴɢ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ</b>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif pesan.photo:
            buttons = Button.button_add_expired(get.id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(get.id)
            buttonz = [[InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data=f"0_cls")]]
            await pesan.request.edit(
                f"<b>💬 sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ʙᴜᴋᴛɪ sᴄʀᴇᴇɴsʜᴏᴛ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ: {full_name}</b>",
                reply_markup=InlineKeyboardMarkup(buttonz),
            )
            buttons = [
                [InlineKeyboardButton("👮‍♀️ ᴀᴅᴍɪɴ", url="https://t.me/roronoajamals")]
            ]
            return await bot.send_message(
                user_id,
                f"""
<b>💬 ʙᴀɪᴋ {full_name} sɪʟᴀʜᴋᴀɴ ᴅɪᴛᴜɴɢɢᴜ ᴅᴀɴ ᴊᴀɴɢᴀɴ sᴘᴀᴍ ʏᴀ</b>
<b>🏦 ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ᴀᴋᴀɴ ᴅɪᴋᴏɴꜰɪʀᴍᴀsɪ sᴇᴛᴇʟᴀʜ 1-12 ᴊᴀᴍ ᴋᴇʀᴊᴀ</b>
<b>‼️ Jɪᴋᴀ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴅɪ ᴋᴏɴғɪʀᴍᴀsɪ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ ᴀᴅᴍɪɴ</b>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


@PY.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 30
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
            [InlineKeyboardButton("⚒️ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⚒️", callback_data="memek")],
        ]
        await bot.send_message(
            get_user.id,
            f"""
<b>✅ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ʙᴇʀʜᴀsɪʟ ᴅɪᴋᴏɴꜰɪʀᴍᴀsɪ</b>

<b>💬 sᴇᴋᴀʀᴀɴɢ ᴀɴᴅᴀ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data=f"0_cls")
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
                    "💳 ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ 💳", callback_data="bayar_dulu"
                )
            ],
        ]
        await bot.send_message(
            get_user.id,
            """
<b>❌ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴅɪᴋᴏɴꜰɪʀᴍᴀsɪ</b>

<b>💬 sɪʟᴀʜᴋᴀɴ ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴅᴇɴɢᴀɴ ʙᴇɴᴀʀ</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data=f"0_cls")
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
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
        else:
            buttons_home = Button.start(callback_query)
            return await callback_query.edit_message_text(
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
