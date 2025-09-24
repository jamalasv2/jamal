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


# Tambah filter
@PY.UBOT("addfilter", sudo=True)
async def _(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(
            f"Gunakan format:\n"
            f"- <code>.addfilter [keyword] [balasan]</code>\n"
            f"- atau reply pesan dengan <code>.addfilter [keyword]</code>"
        )

    keyword = message.command[1].lower()
    existing = await get_filter(client.me.id, keyword)
    if existing:
        return await message.reply(
            f"⚠️ Filter <code>{keyword}</code> sudah ada di database."
        )

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
        return await message.reply("❌ Balas teks/media atau sertakan teks balasan.")

    await save_filter(client.me.id, keyword, value)
    await message.reply(f"✅ Filter <code>{keyword}</code> berhasil ditambahkan.")


# Update filter
@PY.UBOT("updatefilter", sudo=True)
async def updatefilter_handler(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(
            f"Gunakan format:\n"
            f"- <code>.updatefilter [keyword] [balasan baru]</code>\n"
            f"- atau reply pesan dengan <code>.updatefilter [keyword]</code>"
        )

    keyword = message.command[1].lower()
    existing = await get_filter(client.me.id, keyword)
    if not existing:
        return await message.reply(
            f"❌ Filter <code>{keyword}</code> tidak ditemukan di database."
        )

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
        return await message.reply("❌ Balas teks/media atau sertakan teks balasan.")

    await save_filter(client.me.id, keyword, value)
    await message.reply(f"♻️ Filter <code>{keyword}</code> berhasil diperbarui.")


# Hapus filter 1 keyword
@PY.UBOT("delfilter", sudo=True)
async def delfilter_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Gunakan format: <code>.delfilter [keyword]</code>")

    keyword = message.command[1].lower()
    await rm_filter(client.me.id, keyword)
    await message.reply(f"🗑 Filter <code>{keyword}</code> berhasil dihapus.")


# Hapus semua filter
@PY.UBOT("clearfilters", sudo=True)
async def clearfilters_handler(client, message: Message):
    data = await all_filters(client.me.id)
    if not data:
        return await message.reply("❌ Tidak ada filter untuk dihapus.")

    await rm_all_filters(client.me.id)
    await message.reply(f"🧹 Semua filter berhasil dihapus ({len(data)} total).")


# Lihat semua filter
@PY.UBOT("filters", sudo=True)
async def listfilters_handler(client, message: Message):
    data = await all_filters(client.me.id)
    if not data:
        return await message.reply("❌ Tidak ada filter yang tersimpan.")

    text = "**📌 Filters tersedia:**\n"
    for key in data:
        text += f"- `{key}`\n"
    await message.reply(text)


# Lihat isi filter (baru)
@PY.UBOT("filterinfo", sudo=True)
async def filterinfo_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Gunakan format: <code>.filterinfo [keyword]</code>")

    keyword = message.command[1].lower()
    value = await get_filter(client.me.id, keyword)

    if not value:
        return await message.reply(f"❌ Filter <code>{keyword}</code> tidak ditemukan.")

    if value["type"] == "text":
        return await message.reply(
            f"**📖 Info Filter:**\n\n"
            f"🔑 Keyword: <code>{keyword}</code>\n"
            f"📝 Balasan (teks):\n\n{value['data']}"
        )
    else:
        await message.reply(
            f"**📖 Info Filter:**\n\n"
            f"🔑 Keyword: <code>{keyword}</code>\n"
            f"🖼 Jenis: <b>{value['type']}</b>\n"
            f"📌 Preview di bawah 👇"
        )
        try:
            await client.copy_message(
                message.chat.id,
                client.me.id,
                value["message_id"],
                reply_to_message_id=message.id,
            )
        except Exception as e:
            await message.reply(f"⚠️ Gagal menampilkan preview.\n<code>{e}</code>")
