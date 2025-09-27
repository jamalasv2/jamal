from time import time

from pyrogram import filters

from Jamal import *
from Jamal.core.helpers._client import PY
from langs import bhs, get_bhs
from Jamal.database.filters import (
    save_filter,
    get_filter,
    rm_filter,
    all_filters,
    rm_all_filters,
)


__MODULE__ = "filters"
__HELP__ = get_bhs("filters_cmd")


@PY.UBOT("afk")
async def _(client, message):
    reason = get_arg(message)
    db_afk = {"time": time(), "reason": reason}
    em = await get_emo(client)
    tks = reason if reason else "—"
    teks = bhs("filters_afk").format(em.peringatan, em.keterangan, tks)
    await set_vars(client.me.id, "AFK", db_afk)
    return await message.reply(teks)



@PY.AFK()
async def _(client, message):
    em = await get_emo(client)
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        text = bhs("filters_afkaktif").format(em.peringatan, em.waktu, afk_runtime, em.keterangan, afk_reason)
        return await message.reply(text)


@PY.UBOT("unafk")
async def _(client, message):
    em = await get_emo(client)
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_runtime = await get_time(time() - afk_time)
        teks = bhs("filters_unafk").format(em.peringatan, em.waktu, afk_runtime)
        await message.reply(teks)
        return await remove_vars(client.me.id, "AFK")


@ubot.on_message(filters.text | filters.caption & filters.group & filters.incoming, group=5)
async def filter_trigger(client, message):
    if message.from_user and message.from_user.id == client.me.id:
        return
    if message.outgoing:
        return

    is_active = await get_vars(client.me.id, "FILTERS")
    if not is_active:
        return

    text = message.text.lower()
    filters_data = await all_filters(client.me.id)

    if not filters_data:
        return

    for keyword, value in filters_data.items():
        if keyword in text:
            ftype = value.get("type")

            if ftype == "text":
                return await message.reply(value.get("data"))

            msg_id = value.get("message_id")
            if not msg_id:
                continue

            try:
                return await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=client.me.id,
                    message_id=msg_id,
                    reply_to_message_id=message.id
                )
            except Exception as e:
                print(f"Error filter trigger: {e}")
                return


@PY.UBOT("filter", sudo=True)
@PY.GROUP
async def _(client, message):
    em = get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))

    if len(message.command) < 2:
        return await msg.edit(bhs("filters_ops").format(em.gagal))

    command = message.command[1].lower()

    query_map = {"on": True, "off": False}

    if command not in query_map:
        return await msg.edit(bhs("filters_ops").format(em.gagal))

    value = query_map[command]
    text = bhs("filters_on") if value else bhs("filters_off")

    current = await get_vars(client.me.id, "FILTERS")

    if current == value:
        return await msg.edit(bhs("filters_done").format(em.gagal, text))

    await set_vars(client.me.id, "FILTERS", value)
    await msg.delete()
    return await message.reply(
        bhs("filters_stat").format(em.berhasil, text, message.chat.title)
    )


@PY.UBOT("addfilter", sudo=True)
async def _(client, message):
    em = get_emo(client)
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(bhs("filters_addfail").format(em.gagal, 'addfilter'))

    keyword = message.command[1].lower()
    existing = await get_filter(client.me.id, keyword)
    if existing:
        return await message.reply(bhs("filters_exist").format(em.gagal, keyword))

    reply = message.reply_to_message
    value = None

    if len(message.command) > 2 and not reply:
        reply_text = " ".join(message.command[2:])
        value = {"type": "text", "data": reply_text}
    elif reply:
        if reply.text:
            value = {"type": "text", "data": reply.text}
        elif reply.photo:
            copy = await reply.copy(client.me.id)
            value = {"type": "photo", "message_id": copy.id}
        elif reply.sticker:
            copy = await reply.copy(client.me.id)
            value = {"type": "sticker", "message_id": copy.id}
        elif reply.video:
            copy = await reply.copy(client.me.id)
            value = {"type": "video", "message_id": copy.id}
        elif reply.voice:
            copy = await reply.copy(client.me.id)
            value = {"type": "voice", "message_id": copy.id}
        elif reply.audio:
            copy = await reply.copy(client.me.id)
            value = {"type": "audio", "message_id": copy.id}
        elif reply.animation:
            copy = await reply.copy(client.me.id)
            value = {"type": "animation", "message_id": copy.id}

    if not value:
        return await message.reply(bhs("filters_nvalue").format(em.gagal))

    await save_filter(client.me.id, keyword, value)
    await message.reply(bhs("filters_succes").format(em.berhasil, keyword))



@PY.UBOT("updatefilter", sudo=True)
async def updatefilter_handler(client, message: Message):
    em = get_emo(client)
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(bhs("filters_addfail").format(em.gagal, 'updatefilter'))

    keyword = message.command[1].lower()
    existing = await get_filter(client.me.id, keyword)
    if not existing:
        return await message.reply(bhs("filters_noexist").format(em.gagal, keyword))

    reply = message.reply_to_message
    value = None

    if len(message.command) > 2 and not reply:
        reply_text = " ".join(message.command[2:])
        value = {"type": "text", "data": reply_text}
    elif reply:
        if reply.text:
            value = {"type": "text", "data": reply.text}
        elif reply.photo:
            copy = await reply.copy(client.me.id)
            value = {"type": "photo", "message_id": copy.id}
        elif reply.sticker:
            copy = await reply.copy(client.me.id)
            value = {"type": "sticker", "message_id": copy.id}
        elif reply.video:
            copy = await reply.copy(client.me.id)
            value = {"type": "video", "message_id": copy.id}
        elif reply.voice:
            copy = await reply.copy(client.me.id)
            value = {"type": "voice", "message_id": copy.id}
        elif reply.audio:
            copy = await reply.copy(client.me.id)
            value = {"type": "audio", "message_id": copy.id}
        elif reply.animation:
            copy = await reply.copy(client.me.id)
            value = {"type": "animation", "message_id": copy.id}

    if not value:
        return await message.reply(bhs("filters_nvalue").format(em.gagal))

    await save_filter(client.me.id, keyword, value)
    await message.reply(bhs("filters_update").format(em.berhasil, keyword))



@PY.UBOT("delfilter", sudo=True)
async def delfilter_handler(client, message: Message):
    em = get_emo(client)
    if len(message.command) < 2:
        return await message.reply(bhs("filters_delfail").format(em.gagal, 'delfilter'))

    keyword = message.command[1].lower()
    await rm_filter(client.me.id, keyword)
    await message.reply(bhs("filters_delsucces").format(em.berhasil))



@PY.UBOT("clearfilters", sudo=True)
async def clearfilters_handler(client, message: Message):
    em = get_emo(client)
    data = await all_filters(client.me.id)
    if not data:
        return await message.reply(bhs("filters_zero").format(em.gagal))

    await rm_all_filters(client.me.id)
    await message.reply(bhs("filters_clear").format(em.berhasil, len(data)))



@PY.UBOT("listfilters", sudo=True)
async def listfilters_handler(client, message: Message):
    em = get_emo(client)
    data = await all_filters(client.me.id)
    if not data:
        return await message.reply(bhs("filters_zero").format(em.gagal))

    text = bhs("filters_list").format(em.keterangan)
    for key in data:
        text += f"— `{key}`\n"
    await message.reply(text)



@PY.UBOT("infofilter", sudo=True)
async def filterinfo_handler(client, message: Message):
    em = get_emo(client)
    if len(message.command) < 2:
        return await message.reply(bhs("filters_info").format(em.gagal))

    keyword = message.command[1].lower()
    value = await get_filter(client.me.id, keyword)

    if not value:
        return await message.reply(bhs("filters_noexist").format(em.gagal, keyword))

    if value["type"] == "text":
        return await message.reply(bhs("filters_text").format(keyword, value['data']))
    else:
        await message.reply(bhs("filters_media").format(keyword, value['type']))
        try:
            await client.copy_message(
                message.chat.id,
                client.me.id,
                value["message_id"],
                reply_to_message_id=message.id,
            )
        except Exception as e:
            await message.reply(bhs("filters_previewerr").format(em.gagal, e))
