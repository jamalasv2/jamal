import asyncio
import signal

import tornado.ioloop
import tornado.platform.asyncio

from pyrogram import idle
from pyrogram.errors import UserDeactivated

from Jamal import *

async def main():
    await bot.start()
    for _ubot in await get_userbots():
        ubot_ = Ubot(
            user_id=_ubot["user_id"],
            api_id=_ubot["api_id"],
            api_hash=_ubot["api_hash"],
            session_string=_ubot["session_string"],
        )
        try:
            await asyncio.wait_for(ubot_.start(), timeout=10)
            await ubot_.join_chat("newhiganbana")
        except asyncio.TimeoutError:
            print(f"[INFO]: {int(_ubot['user_id'])} TIDAK DAPAT MERESPON")
        except Exception as e:
            await remove_ubot(int(_ubot["user_id"]))
            await rem_expired_date(int(_ubot["user_id"]))
            print(f"[INFO]: {int(_ubot['user_id'])}\n{e}")
        except UserDeactivated:
            await remove_ubot(int(_ubot["user_id"]))
            await rem_expired_date(int(_ubot["user_id"]))
            await remove_all_vars(int(_ubot["user_id"]))
            await remove_from_vars(bot.me.id, "PREM_USERS", int(_ubot["user_id"]))
            print(f"[ INFO ]: {int(_ubot['user_id'])} akun terhapus dibersihkan")
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
