from time import time

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
    em = get_emo(client)
    tks = reason if reason else "—"
    teks = bhs("filters_afk").format(em.afk, em.keterangan, tks)
    await set_vars(client.me.id, "AFK", db_afk)
    return await message.reply(teks)



@PY.AFK()
async def _(client, message):
    em = get_emo(client)
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        text = bhs("filters_afkaktif").format(em.afk, em.menunggu, afk_runtime, em.keterangan, afk_reason)
        return await message.reply(text)


@PY.UBOT("unafk")
async def _(client, message):
    em = get_emo(client)
    vars = await get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_runtime = await get_time(time() - afk_time)
        teks = bhs("filters_unafk").format(em.afk, em.menunggu, afk_runtime)
        await message.reply(teks)
        return await remove_vars(client.me.id, "AFK")


@PY.UBOT("filter", sudo=True)
@PY.GROUP
async def _(client, message):
    em = get_emo(client)
    vars = await get_vars(client.me.id, "FILTERS", value)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    if len(message.command) <2:
        return await msg.edit("filters_ops").format(em.gagal)
    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await msg.edit(bhs("filters_ops").format(em.gagal))

    value = query[command]
    text = bhs("filters_on") if value else bhs("filters_off")
    if value in vars:
        return await msg.edit(bhs("filters_done").format(em.gagal, text))
    else:
        await set_vars(client.me.id, "FILTERS", value)
        await msg.delete()
        return await message.reply(bhs("filters_stat").format(em.berhasil, value, message.chat.title))

# Tambah filter
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


# Update filter
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


# Hapus filter 1 keyword
@PY.UBOT("delfilter", sudo=True)
async def delfilter_handler(client, message: Message):
    em = get_emo(client)
    if len(message.command) < 2:
        return await message.reply(bhs("filters_delfail").format(em.gagal, 'delfilter'))

    keyword = message.command[1].lower()
    await rm_filter(client.me.id, keyword)
    await message.reply(bhs("filters_delsucces").format(em.berhasil))


# Hapus semua filter
@PY.UBOT("clearfilters", sudo=True)
async def clearfilters_handler(client, message: Message):
    em = get_emo(client)
    data = await all_filters(client.me.id)
    if not data:
        return await message.reply(bhs("filters_zero").format(em.gagal))

    await rm_all_filters(client.me.id)
    await message.reply(bhs("filters_clear").format(em.berhasil, len(data)))


# Lihat semua filter
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


# Lihat isi filter (baru)
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
