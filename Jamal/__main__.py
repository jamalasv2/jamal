import asyncio
import logging
import os
import sys

from rich.logging import RichHandler

from Jamal.config import API_ID, API_HASH
from Jamal import bot, ubot
from Jamal.database.userbot import get_userbots
from Jamal.core.function import loadPlugins, expiredUserbots, install_my_peer


# ========== Logging Setup ==========
class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for error_type in ["OSErro", "TimeoutError"]:
            if error_type in record.getMessage():
                os.execl(sys.executable, sys.executable, "-m", "Jamal")


logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler(), ConnectionHandler()],
)

logger = logging.getLogger(__name__)


# ========== Main Runner ==========
async def main():
    # start bot utama
    await bot.start()

    # load semua plugins
    loadPlugins()

    # ambil userbot dari db
    userbots = await get_userbots()
    if not userbots:
        logger.warning("Tidak ada userbot di database!")
    else:
        for data in userbots:
            try:
                client = ubot.__class__(
                    name=data["name"],
                    api_id=data["api_id"],
                    api_hash=data["api_hash"],
                    session_string=data["session_string"],
                )
                await client.start()
                await install_my_peer(client)
                logger.info(f"Userbot {client.me.id} berhasil dijalankan ✅")
            except Exception as e:
                logger.error(f"Gagal start userbot {data['name']}: {e}")

    # jalanin expired checker
    asyncio.create_task(expiredUserbots(bot))

    logger.info("Bot dan semua userbot sudah berjalan 🚀")

    # biar tetap jalan
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown... sampai jumpa 👋")