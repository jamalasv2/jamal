from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType

from Jamal import *
from Jamal.config import OWNER_ID



async def check_afk_user(client):
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        return True


class PY:
    @staticmethod
    def ADMIN(func):
        async def function(client, message):
            user = message.from_user
            admin_id = await get_list_from_vars(client.me.id, "ADMIN_USERS")
            if user.id not in admin_id:
                return
            return await func(client, message)

        return function

    @staticmethod
    def SELLER(func):
        async def function(client, message):
            user = message.from_user
            seller_id = await get_list_from_vars(client.me.id, "SELER_USERS")
            if user.id not in seller_id:
                return
            return await func(client, message)

        return function
        
    @staticmethod
    def PROTECT():
        def wrapper(func):
            protect_check = (
                filters.group
                & ~filters.bot
                & ~filters.me
            )

            @ubot.on_message(protect_check, group=76)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def ANKES():
        def wrapper(func):
            ankes_check = (
                filters.group
                & ~filters.bot
                & ~filters.me
                & filters.incoming
            )

            @ubot.on_message(ankes_check, group=80)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def AFK():
        def wrapper(func):
            afk_check = (
                 (filters.mentioned | filters.private)
                & ~filters.bot
                & ~filters.me
                & filters.incoming
            )

            @ubot.on_message(afk_check, group=77)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def BOT(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def UBOT(command, sudo=False):
        def wrapper(func):
            sudo_filrers = (
                ubot.cmd_prefix(command)
                if sudo
                else ubot.cmd_prefix(command) & filters.me
            )
            
            @ubot.on_message(sudo_filrers)
            async def wrapped_func(client, message):
                if sudo:
                    sudo_id = await get_list_from_vars(
                        client.me.id, "SUDO_USERS", "DB_SUDO"
                    )
                    user = message.from_user if message.from_user else message.sender_chat
                    if client.me.id not in sudo_id:
                        sudo_id.append(client.me.id)
                    if user.id in sudo_id:
                        return await func(client, message)
                else:
                    return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def INLINE(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def PRIVATE(func):
        async def function(client, message):
            if not message.chat.type == ChatType.PRIVATE:
                return 
            return await func(client, message)

        return function

    @staticmethod
    def GROUP(func):
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                return 
            return await func(client, message)

        return function

    @staticmethod
    def LOGS_PRIVATE():
        def wrapper(func):
            @ubot.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.service, group=78
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def LOGS_GROUP():
        def wrapper(func):
            @ubot.on_message(
                filters.group & filters.incoming & filters.mentioned & ~filters.bot, group=79
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def OWNER(func):
        async def function(client, message):
            user = message.from_user
            if user.id != OWNER_ID:
                return 
            return await func(client, message)

        return function

    @staticmethod
    def DEV(func):
        async def function(client, message):
            user = message.from_user
            if user.id != DEVS:
                return
            return await func(client, message)

        return function

    @staticmethod
    def PMPERMIT():
        def wrapper(func):
            @ubot.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.via_bot
                & ~filters.service,
                group=69,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def TOP_CMD(func):
        async def function(client, message):
            cmd = message.command[0].lower()
            top = await get_vars(bot.me.id, cmd, "modules")
            get = int(top) + 1 if top else 1
            await set_vars(bot.me.id, cmd, get, "modules")
            return await func(client, message)

        return function

    @staticmethod
    def START(func):
        async def function(client, message):
            seved_users = await get_list_from_vars(client.me.id, "SAVED_USERS")
            user_id = message.from_user.id
            if user_id != OWNER_ID:
                if user_id not in seved_users:
                    await add_to_vars(client.me.id, "SAVED_USERS", user_id)
            return await func(client, message)

        return function