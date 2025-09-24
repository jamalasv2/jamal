import string
from math import ceil
from time import time

from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

from Jamal.core.helpers.font_tool import Fonts


async def extract_userid(message, text):
    def is_int(text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    entity = entities[1 if message.text.startswith("/") else 0]
    if entity.type == enums.MessageEntityType.MENTION:
        return (await app.get_users(text)).id
    if entity.type == enums.MessageEntityType.TEXT_MENTION:
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


admins_in_chat = {}


async def list_admins(message):
    global admins_in_chat
    if message.chat.id in admins_in_chat:
        interval = time() - admins_in_chat[message.chat.id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[message.chat.id]["data"]

    admins_in_chat[message.chat.id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in message._client.get_chat_members(
                message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[message.chat.id]["data"]


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix):
    if not module_dict:
        return [[EqInlineKeyboardButton("❌ No modules", callback_data="noop")]]

    modules = [
        EqInlineKeyboardButton(
            Fonts.smallcap(x.__MODULE__.lower()),
            callback_data=f"{prefix}_module({page_n},{x.__MODULE__.replace(' ', '_')})",
        )
        for x in module_dict.values()
    ]

    line = 4
    pairs = [list(pair) for pair in zip(modules[::2], modules[1::2])]
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])

    max_num_pages = ceil(len(pairs) / line) if pairs else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > line:
        pairs = pairs[modulo_page * line : line * (modulo_page + 1)]
        pairs.append([
            EqInlineKeyboardButton("◄", callback_data=f"{prefix}_prev({modulo_page})"),
            EqInlineKeyboardButton("►", callback_data=f"{prefix}_next({modulo_page})"),
        ])

    return pairs
