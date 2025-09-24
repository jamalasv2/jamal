import re

from pyrogram.types import *

from Jamal import *
from Jamal.core.helpers import *
from langs import *


@PY.UBOT("help", sudo=True)
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(bot.me.username, "user_help")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await message.reply(error)

user_pages = {}

@PY.INLINE("^user_help")
@INLINE.QUERY
async def user_help(client, inline_query):
    SH = await ubot.get_prefix(inline_query.from_user.id)
    user_id = inline_query.from_user.id
    msg = bhs("help_text").format(' '.join(SH))

    user_pages[user_id] = 0  # simpan halaman default

    results = [
        InlineQueryResultArticle(
            title="Help Menu!",
            input_message_content=InputTextMessageContent(msg),
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELP_COMMANDS, "help")
            ),
        )
    ]

    await client.answer_inline_query(inline_query.id, results=results, cache_time=0)


@PY.CALLBACK("help_(.*?)")
async def _(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    SH = await ubot.get_prefix(user_id)
    top_text = bhs("help_text").format(' '.join(SH))

    mod_match = re.match(r"help_module\((\d+),(.+)\)", data)
    prev_match = re.match(r"help_prev\((\d+)\)", data)
    next_match = re.match(r"help_next\((\d+)\)", data)
    back_match = re.match(r"help_back", data)

    if mod_match:
        page = int(mod_match.group(1))
        module_name = mod_match.group(2).replace("_", " ").lower()
        user_pages[user_id] = page  # simpan halaman terakhir

        module = next((mod for mod in HELP_COMMANDS.values() if mod.__MODULE__.lower() == module_name), None)
        if not module:
            return await callback_query.answer("Modul tidak ditemukan.", show_alert=True)

        text = module.__HELP__.format(next((p for p in SH)))
        buttons = [[InlineKeyboardButton(bhs("text_back"), callback_data="help_back")]]
        return await callback_query.edit_message_text(
            text=text + "\n<b>© [jamalas](tg://user?id=6425078161)</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )

    elif prev_match:
        page = int(prev_match.group(1)) - 1
        user_pages[user_id] = page
        return await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(page, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )

    elif next_match:
        page = int(next_match.group(1)) + 1
        user_pages[user_id] = page
        return await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(page, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )

    elif back_match:
        page = user_pages.get(user_id, 0)
        return await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(page, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )
