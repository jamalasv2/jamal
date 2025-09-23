import asyncio
import importlib
from datetime import datetime
from time import time

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from Jamal.core.helpers._client import PY
from Jamal import *
from langs import *


@PY.CALLBACK("memek")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_installed"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_limit"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_list_from_vars(client.me.id, "PREM_USERS"):
        buttons = [
            [InlineKeyboardButton(bhs("text_buy"), callback_data="bahan")],
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_noacces"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton(bhs("text_continue"), callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            bhs("text_install"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("bahan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("text_installed"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("text_limit"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_list_from_vars(client.me.id, "PREM_USERS"):
        buttons = [
            [InlineKeyboardButton(bhs("text_continue"), callback_data="bayar_dulu")],
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("text_attention"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton(bhs("text_continue"), callback_data="memek")]]
        return await callback_query.edit_message_text(
            bhs("text_acces"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.plus_minus(1, user_id)
    return await callback_query.edit_message_text(
        bhs("text_payment").format(20, 20, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("add_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton(bhs("text_contact"), request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    try:
        phone = await bot.ask(
            user_id,
            bhs("text_share"),
            timeout=300,
            reply_markup=keyboard
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, bhs("text_rto"))
    ph = phone.contact
    phone_number = ph.phone_number
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
    )
    get_otp = await bot.send_message(user_id, bhs("text_sendotp"), reply_markup=ReplyKeyboardRemove())
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as AID:
        await get_otp.delete()
        return await bot.send_message(user_id, AID)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    try:
        sent_code = {
            SentCodeType.APP: bhs("text_otptype1").format(f"<a href=tg://openmessage?user_id=777000>ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ</a> ʀᴇsᴍɪ"),
            SentCodeType.SMS: bhs("text_otptype2"),
            SentCodeType.CALL: bhs("text_otptype3"),
            SentCodeType.FLASH_CALL: bhs("text_otptype4"),
            SentCodeType.FRAGMENT_SMS: bhs("text_otptype5"),
            SentCodeType.EMAIL_CODE: bhs("text_otptype6"),
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                bhs("text_askotp")
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, bhs("text_rto"))
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number,
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except BadRequest as error:
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                bhs("text_askv2l"),
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, bhs("text_rto"))
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
            await set_two_factor(user_id, new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = True
    bot_msg = await bot.send_message(
        user_id,
        bhs("text_proses"),
        disable_web_page_preview=True,
    )
    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        await rem_two_factor(new_client.me.id)
        return await bot_msg.edit(
            bhs("text_wrong")
        )
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    await set_vars(client.me.id, "UPTIME", time())
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"Jamal.modules.{mod}"))
    SH = await ubot.get_prefix(new_client.me.id)
    buttons = [
            [InlineKeyboardButton(bhs("text_back"), callback_data=f"home {user_id}")],
        ]
    text_done = bhs("text_activated").format(f"<a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>", new_client.me.id, ''.join(sh)), 
    await bot_msg.edit(text_done, disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))
    await install_my_peer(new_client)
    try:
        await new_client.join_chat("newhiganbana")
    except UserAlreadyParticipant:
        pass
    

async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, bhs("text_cancelled")
        )
        return True
    return False
