import asyncio
import signal
import tornado.ioloop
import tornado.platform.asyncio

from pyrogram import idle
from pyrogram.errors import UserDeactivated

from Jamal import bot, Ubot
from Jamal.database.userbot import get_userbots, remove_ubot
from Jamal.core.function import loadPlugins, installPeer, expiredUserbots  # assume these exist

# keep track of running ubot instances so they can be stopped cleanly
running_ubots = []

async def shutdown(sig, loop):
    print(f"[INFO] Received exit signal {sig.name}...")
    # stop all running ubots
    for ub in list(running_ubots):
        try:
            await ub.stop()
            print(f"[INFO] Stopped ubot {getattr(ub, 'me', {}).id if getattr(ub, 'me', None) else 'unknown'}")
        except Exception as e:
            print(f"[ERROR] Stopping ubot: {e}")
    # stop main bot
    try:
        await bot.stop()
    except Exception:
        pass
    # cancel remaining tasks and stop loop
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():
    await bot.start()

    # load ubots from DB
    _userbots = await get_userbots() or []
    for _ubot in _userbots:
        try:
            client = Ubot(
                name=str(_ubot["user_id"]),
                api_id=_ubot["api_id"],
                api_hash=_ubot["api_hash"],
                session_string=_ubot["session_string"],
                in_memory=True,
            )
            await asyncio.wait_for(client.start(), timeout=20)
            running_ubots.append(client)
            # try join chat but ignore errors
            try:
                await client.join_chat("newhiganbana")
            except Exception:
                pass
            print(f"[INFO] Loaded ubot { _ubot['user_id'] }")
        except asyncio.TimeoutError:
            print(f"[INFO] {_ubot['user_id']} did not respond (timeout)")
        except UserDeactivated:
            await remove_ubot(int(_ubot["user_id"]))
            print(f"[INFO] {_ubot['user_id']} account deactivated; removed from DB")
        except Exception as e:
            print(f"[ERROR] Cannot start ubot {_ubot.get('user_id')}: {e}")
            try:
                await remove_ubot(int(_ubot["user_id"]))
            except Exception:
                pass

    # start background tasks (plugins/peers/expiry)
    try:
        await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), return_exceptions=True)
    except Exception as e:
        print(f"[WARN] background tasks error: {e}")

    # register signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda sig=s: asyncio.create_task(shutdown(sig, loop)))

    # idle until signalled
    print("[MAIN] Bot is running. Press Ctrl+C to stop.")
    try:
        await idle()
    finally:
        # final cleanup
        await shutdown(signal.Signals.SIGTERM, loop)

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())