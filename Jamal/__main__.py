import asyncio
import signal

import tornado.ioloop
import tornado.platform.asyncio

from pyrogram import idle
from pyrogram.errors import UserDeactivated

from Jamal import *
from Jamal.core.helpers.class_emoji import *
import os
import glob

# --- AUTO CLEANER SESSION ---
def clean_sessions():
    session_files = glob.glob("*.session*")
    if session_files:
        print(f"[CLEANER] Menghapus sisa session: {session_files}")
        for f in session_files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"[CLEANER] Gagal hapus {f}: {e}")
    else:
        print("[CLEANER] Tidak ada file .session tersisa")

clean_sessions()


async def main():
    await bot.start()
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        em = Emojik(int(_ubot["name"])
        try:
            await asyncio.wait_for(ubot_.start(), timeout=10)
            await ubot_.join_chat("newhiganbana")
            await em.initialize()
        except asyncio.TimeoutError:
            print(f"[𝗜𝗡𝗙𝗢]: {int(_ubot['name'])} 𝗧𝗜𝗗𝗔𝗞 𝗗𝗔𝗣𝗔𝗧 𝗠𝗘𝗥𝗘𝗦𝗣𝗢𝗡")
        except Exception as e:
            await remove_ubot(int(_ubot["name"]))
            await rem_expired_date(int(_ubot["name"]))
            print(f"[𝗜𝗡𝗙𝗢]: {int(_ubot['name'])}\n{e}")
        except UserDeactivated:
            await remove_ubot(int(_ubot["name"]))
            await rem_expired_date(int(_ubot["name"]))
            await remove_all_vars(int(_ubot["name"]))
            await remove_from_vars(bot.me.id, "PREM_USERS", int(_ubot["name"]))
            print(f"[ INFO ]: {int(_ubot['name'])} akun terhapus dibersihkan")
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), idle())
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda: asyncio.create_task(shutdown(s, loop)))
    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await bot.stop()

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
