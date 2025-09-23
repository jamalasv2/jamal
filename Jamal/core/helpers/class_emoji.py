from Jamal.database import get_vars
from Jamal import *

import asyncio

class Emojik:
    _cache = {}

    def __init__(self, client):
        self.client = client
        # default emoji (kalau tidak premium / tidak ada var di DB)
        self.ping = "🏓"
        self.mention = "👤"
        self.ubot = "🤖"
        self.proses = "⌛️"
        self.berhasil = "✅"
        self.gagal = "❌"
        self.broadcast = "📊"
        self.group = "🗂"
        self.keterangan = "📝"
        self.menunggu = "⏰"
        self.afk = "‼️"

    async def initialize(self):
        """Ambil emoji dari DB lalu simpan ke cache"""
        vars_map = {
            "ping":       ("EMOJI_PING", "5999035921905749785", "🏓"),
            "mention":    ("EMOJI_MENTION", "5998830540864622070", "👤"),
            "ubot":       ("EMOJI_USERBOT", "6001409398142930455", "🤖"),
            "proses":     ("EMOJI_PROSES", "5451732530048802485", "⌛️"),
            "berhasil":   ("EMOJI_BERHASIL", "5427009714745517609", "✅"),
            "gagal":      ("EMOJI_GAGAL", "5465665476971471368", "❌"),
            "broadcast":  ("EMOJI_BROADCAST", "5431577498364158238", "📊"),
            "group":      ("EMOJI_GROUP", "5431736674147114227", "🗂"),
            "keterangan": ("EMOJI_KETERANGAN", "5334882760735598374", "📝"),
            "menunggu":   ("EMOJI_MENUNGGU", "5413704112220949842", "⏰"),
            "afk": ("EMOJI_AFK", "5467890025217661107", "‼️"),
        }

        for attr, (var_key, fallback_id, fallback_txt) in vars_map.items():
            val = await get_vars(self.client.me.id, var_key)
            if self.client.me.is_premium and val:
                setattr(self, attr, f"<emoji id={val}>{fallback_txt}</emoji>")
            else:
                setattr(self, attr, fallback_txt)

        # cache per client_id
        Emojik._cache[self.client.me.id] = self
        return self

    @classmethod
    def get(cls, client_id: int):
        return cls._cache.get(client_id)


def get_emo(client):
    """
    Ambil instance Emojik dari cache berdasarkan client.me.id
    Jika belum ada di cache, buat default instance.
    """
    em = Emojik.get(client.me.id)
    if not em:
        # fallback: buat instance default tanpa initialize async
        em = Emojik(client)
        # optional: bisa dijalankan initialize di background
        asyncio.create_task(em.initialize())
    return em
