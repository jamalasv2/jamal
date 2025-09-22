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


@PY.CALLBACK("pler")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton(
                bhs("cb_inline1"),
                callback_data=f"home {user_id}")],
        ]
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        return await callback_query.edit_message_text(
            f"""
<b>sᴛᴀᴛᴜs :</b> <code>ᴘʀᴇᴍɪᴜᴍ</code>
<b>ᴘʀᴇғɪxᴇs :</b> <code>{prefix[0]}</code>
<b>ʙᴏᴛ_ᴜᴘᴛɪᴍᴇ :</b> <code>-</code>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton(" ʙᴇʟɪ ᴜsᴇʀʙᴏᴛ", callback_data=f"bahan")],
            [InlineKeyboardButton("⬅️ ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""o
<b>‼️ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍɪʟɪᴋɪ ᴜsᴇʀʙᴏᴛ ɪɴɪ</b>
<b> sɪʟᴀʜᴋᴀɴ ʙᴇʟɪ ᴜsᴇʀʙᴏᴛ ɴʏᴀ</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("memek")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton(bhs("cb_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_installed"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton(bhs("cb_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_limit"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_list_from_vars(client.me.id, "PREM_USERS"):
        buttons = [
            [InlineKeyboardButton(bhs("cb_buy"), callback_data="bahan")],
            [InlineKeyboardButton(bhs("cb_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_noacces"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        return await callback_data="add_ubot"


@PY.CALLBACK("bahan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton(bhs("cb_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_installed"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton(bhs("cb_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("cb_limit"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_list_from_vars(client.me.id, "PREM_USERS"):
        buttons = [
            [InlineKeyboardButton(bhs("cb_continue"), callback_data="bayar_dulu")],
            [InlineKeyboardButton(bhs("cb_back"), callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            bhs("start_2"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton(bhs("cb_continue"), callback_data="memek")]]
        return await callback_query.edit_message_text(
            bhs("cb_acces"),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.plus_minus(1, user_id)
    return await callback_query.edit_message_text(
        bhs("pay_text").format(20, 20, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("add_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("Bagikan Kontak", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    try:
        phone = await bot.ask(
            user_id,
            (
                "klik bagikan contact untuk melanjutkan proses pembuatan userbot"
            ),
            timeout=300,
            reply_markup=keyboard
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs")
    ph = phone.contact
    phone_number = ph.phone_number
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
    )
    get_otp = await bot.send_message(user_id, "<b>mengirim kode otp</b>", reply_markup=ReplyKeyboardRemove())
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
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ</a> ʀᴇsᴍɪ",
            SentCodeType.SMS: "sᴍs ᴀɴᴅᴀ",
            SentCodeType.CALL: "ᴘᴀɴɢɢɪʟᴀɴ ᴛᴇʟᴘᴏɴ",
            SentCodeType.FLASH_CALL: "ᴘᴀɴɢɢɪʟᴀɴ ᴋɪʟᴀᴛ ᴛᴇʟᴇᴘᴏɴ",
            SentCodeType.FRAGMENT_SMS: "ꜰʀᴀɢᴍᴇɴᴛ sᴍs",
            SentCodeType.EMAIL_CODE: "ᴇᴍᴀɪʟ ᴀɴᴅᴀ",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                f"<b>sɪʟᴀᴋᴀɴ ᴘᴇʀɪᴋsᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴅᴀʀɪ {sent_code[code.type]}. ᴋɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ ᴋᴇ sɪɴɪ sᴇᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴄᴀ ꜰᴏʀᴍᴀᴛ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ.</b>\n"
                "\nᴊɪᴋᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴀᴅᴀʟᴀʜ <ᴄᴏᴅᴇ>12345</ᴄᴏᴅᴇ> ᴛᴏʟᴏɴɢ <b>[ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴘᴀsɪ ]</b> ᴋɪʀɪᴍᴋᴀɴ sᴇᴘᴇʀᴛɪ ɪɴɪ <code>1 2 3 4 5</code>\n"
                "\n<b>ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "ᴡᴀᴋᴛᴜ ᴛᴇʟᴀʜ ʜᴀʙɪs")
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
                "<b>ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴠᴇʀɪꜰɪᴋᴀsɪ ᴅᴜᴀ ʟᴀɴɢᴋᴀʜ. sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ᴘᴀssᴡᴏʀᴅɴʏᴀ.\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs")
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
        "sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs....\n\nsɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ",
        disable_web_page_preview=True,
    )
    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        await rem_two_factor(new_client.me.id)
        return await bot_msg.edit(
            "<b>ʜᴀʀᴀᴘ ɢᴜɴᴀᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅɪ ᴀᴋᴜɴ ᴀɴᴅᴀ sᴀᴀᴛ ɪɴɪ ᴅᴀɴ ʙᴜᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴀʀɪ ᴀᴋᴜɴ ʟᴀɪɴ</>"
        )
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    await set_vars(client.me.id, "UPTIME", time())
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))
    SH = await ubot.get_prefix(new_client.me.id)
    buttons = [
            [InlineKeyboardButton("⬅️ ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
    text_done = f"""
<b> ᴜsᴇʀʙᴏᴛ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ɴᴀᴍᴇ :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
<b> ɪᴅ :</b> <code>{new_client.me.id}</code>
<b> ᴘʀᴇғɪxᴇs :</b> <code>{' '.join(SH)}</code>
<b> ᴇxᴘɪʀᴇᴅ :</b>
        """
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
            callback_query.from_user.id, "<b>ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs!</b>"
        )
        return True
    return False
