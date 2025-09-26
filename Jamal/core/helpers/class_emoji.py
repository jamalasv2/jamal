from Jamal.database import get_vars
from Jamal import *

import asyncio


class emoji:
    def __init__(self):
        # fallback default (emoji biasa, tanpa premium)
        self.ping = "🏓"
        self.mention = "👤"
        self.ubot = "🤖"
        self.proses = "⌛️"
        self.berhasil = "✅"
        self.gagal = "❌"
        self.broadcast = "📊"
        self.bl_group = "🗂"
        self.bl_keterangan = "📝"
        self.menunggu = "⏰"

    def initialize(self, client):
        try:
            loop = asyncio.get_running_loop()
            future = asyncio.run_coroutine_threadsafe(
                self._initialize_async(client), loop
            )
            future.result()
        except RuntimeError:
            asyncio.run(self._initialize_async(client))

    async def _initialize_async(self, client):
        # Ambil dari DB (kalau ada), fallback ke ID default
        ping_id   = await get_vars(client.me.id, "EMOJI_PING")        or "5999035921905749785"
        mention_id= await get_vars(client.me.id, "EMOJI_MENTION")     or "5998830540864622070"
        ubot_id   = await get_vars(client.me.id, "EMOJI_USERBOT")     or "6001409398142930455"
        proses_id = await get_vars(client.me.id, "EMOJI_PROSES")      or "5451732530048802485"
        berhasil_id=await get_vars(client.me.id, "EMOJI_BERHASIL")    or "5427009714745517609"
        gagal_id  = await get_vars(client.me.id, "EMOJI_GAGAL")       or "5465665476971471368"
        bc_id     = await get_vars(client.me.id, "EMOJI_BROADCAST")   or "5431577498364158238"
        bl_group_id=await get_vars(client.me.id, "EMOJI_GROUP")       or "5431736674147114227"
        bl_ket_id = await get_vars(client.me.id, "EMOJI_KETERANGAN")  or "5334882760735598374"
        menunggu_id=await get_vars(client.me.id, "EMOJI_MENUNGGU")    or "5413704112220949842"

        if client.me.is_premium:
            self.ping           = f"<emoji id={ping_id}>🏓</emoji>"
            self.mention        = f"<emoji id={mention_id}>👤</emoji>"
            self.ubot           = f"<emoji id={ubot_id}>🤖</emoji>"
            self.proses         = f"<emoji id={proses_id}>⌛️</emoji>"
            self.berhasil       = f"<emoji id={berhasil_id}>✅</emoji>"
            self.gagal          = f"<emoji id={gagal_id}>❌</emoji>"
            self.broadcast      = f"<emoji id={bc_id}>📊</emoji>"
            self.bl_group       = f"<emoji id={bl_group_id}>🗂</emoji>"
            self.bl_keterangan  = f"<emoji id={bl_ket_id}>📝</emoji>"
            self.menunggu       = f"<emoji id={menunggu_id}>⏰</emoji>"
        else:
            # fallback: sudah diisi default di __init__
            pass
