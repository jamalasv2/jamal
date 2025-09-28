import asyncio
from random import randint

from pyrogram import enums
from pyrogram.errors import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import (
    CreateGroupCall,
    DiscardGroupCall,
    EditGroupCallTitle,
    GetGroupCall,
    GetGroupParticipants,
)
from pyrogram.raw.types import (
    InputGroupCall,
    InputPeerChannel,
    InputPeerChat,
)
from pyrogram.raw.base import InputPeer
    

from pytgcalls import GroupCallFactory
from pytgcalls.exceptions import GroupCallNotFoundError

from Jamal import *
from langs import bhs, get_bhs


__MODULE__ = "joinvc"
__HELP__ = get_bhs("joinvc_cmd")


list_data = []


def remove_list(user_id):
    list_data[:] = [item for item in list_data if item.get("id") != user_id]


def add_list(user_id, text):
    data = {"id": user_id, "nama": text}
    list_data.append(data)


def get_list():
    if not list_data:
        return "<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴜsᴇʀ ᴅɪ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ ᴍᴀɴᴀᴘᴜɴ</b>"

    msg = "\n".join(item["nama"] for item in list_data)
    return msg


async def get_group_call(client, message):
    chat_peer = await client.resolve_peer(message.chat.id)
    
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call

    await message.reply("no group call found")
    return False
    

@PY.UBOT("startvc", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    gc = await EMO.BL_GROUP(client)
    flags = " ".join(message.command[1:])
    msg = await message.reply(f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs</b>")
    vctitle = get_arg(message)
    chat_id = message.chat.title if flags == enums.ChatType.CHANNEL else message.chat.id
    group_call = await get_group_call(client, message)
    if group_call:
        return await msg.edit("obrolan suara sudah aktif")
    
    args = (
        f"<b>{brhsl}ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ ᴀᴋᴛɪғ</b>\n<b>{gc}ᴄʜᴀᴛ:</b> {chat_id}"
    )
    
    try:
      if vctitle:
          args += f"\n<b>ᴛɪᴛʟᴇ: {vctitle}</b> "
          
      await client.invoke(
          CreateGroupCall(
              peer=(await client.resolve_peer(chat_id)),
              random_id=randint(10000, 999999999),
              title=vctitle if vctitle else None,
          )
      )
      await msg.edit(args)
    except Exception as e:
        await msg.edit(f"<b>ɪɴғᴏ:</b> `{e}`")


@PY.UBOT("stopvc", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"{prs} memproses..")
    group_call = await get_group_call(client, message)
    
    if not group_call:
        return await msg.edit(f"{ggl} tidak ada obrolan suara yang aktif")
    
    await client.invoke(DiscardGroupCall(call=group_call))
    await msg.edit(
        f"<b>ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ ᴅɪᴀᴋʜɪʀɪ</b>\n<b>ᴄʜᴀᴛ: {message.chat.title}")


@PY.UBOT("joinvc", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["Jvcs"], "") & filters.user(DEVS))
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    gc = await EMO.BL_GROUP(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    titit = await client.get_chat(per)
    gc_titit = titit.title
    text = f"• <b>[{client.me.first_name} {client.me.last_name or ''}](tg://user?id={client.me.id})</b> |{gc_titit}|<code>{per}</code>"
    try:
        await client.group_call.start(per, join_as=client.me.id)
        await asyncio.sleep(1)
        await client.group_call.set_is_mute(True)
    except Exception as e:
        return await message.reply(f"ERROR: {e}")
    await message.reply(f"<b>{brhsl}ʙᴇʀʜᴀsɪʟ ɴᴀɪᴋ ᴋᴇ ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ\n{gc}ɢʀᴏᴜᴘ: {gc_titit}</b>")
    add_list(client.me.id, text)


@PY.UBOT("leavevc", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["Lvcs"], "") & filters.user(DEVS))
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    try:
        await client.group_call.stop()
    except Exception as e:
        return await message.reply(f"ERROR: {e}")
    remove_list(client.me.id)
    return await message.reply(f"<b>{brhsl}ʙᴇʀʜᴀsɪʟ ᴛᴜʀᴜɴ ᴅᴀʀɪ ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ</b>")


@PY.UBOT("listos")
@PY.OWNER
async def _(client, message):
    await message.reply(get_list())
         

@PY.UBOT("vctitle", sudo=True)
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    titit = get_arg(message)
    msg = await message.reply(f"{prs} memprosess")
    group_call = await get_group_call(client, message)

    if len(message.command) < 2:
        return await msg.edit(f"{ggl} ketik teks untuk mengganti judul pada obrolan suara!")

    if not group_call:
        return await msg.edit(f"<blockquote>{ggl} tidak bisa mengubah judul pada obrolan suara, mohon aktifkan obrolam suara terlebih dahulu!</blockquote>")
    else:
        try:
            await client.invoke(
                EditGroupCallTitle(call=group_call, title=f"{titit}"))
        except Exception as error:
            return await msg.edit(f"ERROR:\n{error}")
        await msg.delete()
        return await message.reply(f"{brhsl} judul obrolan suara diubah menjadi: <code>{titit}</code>")


@PY.UBOT("listener")
async def _(client, message):
    chat_id = message.chat.id
    msg = await message.reply("Memeriksa obrolan suara...")
    text = None
    msg_txt = "<blockquote>daftar peserta pada obrolan suara</blockquote>"

    try:
        peer = await client.resolve_peer(chat_id)
        full_chat = (await client.invoke(GetFullChat(chat_id=peer.chat_id))).full_chat

        if not full_chat.call:
            return await msg.edit("tidak ada obrolan suara yang aktif")

        group_call = InputGroupCall(
            id=full_chat.call.id,
            access_hash=full_chat.call.access_hash,
        )
        participants = await client.invoke(
            GetGroupParticipants(
                call=group_call,
                ids=[],
                sources=["recent"],
                limit=50,
                offset=0
            )
        )
        for p in participants.participants:
            try:
                user = await client.get_users(p.peer.user_id)
                msg_txt += f"— {user.first_name} {user.last_name or ''} | <code>{user.id}</code>\n"
            except:
                msg_txt += f"— <code>{p.peer.user_id}</code>"
        await msg.delete()
        return await message.reply(msg_txt)
    except RPCError as e:
        return await msg.edit(e)
    except Exception as error:
        return await msg.edit(f"<blockquote>ERROR:\n{error}</blockquote>")

