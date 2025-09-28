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
JOINED_VC = {}


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
    em = await get_emo(client)
    flags = " ".join(message.command[1:])
    msg = await message.reply(bhs("text_proses").format(em.proses))
    vctitle = get_arg(message)
    chat_id = message.chat.title if flags == enums.ChatType.CHANNEL else message.chat.id
    group_call = await get_group_call(client, message)
    if group_call:
        return await msg.edit(bhs("joinvc_startex").format(em.gagal))
    
    args = bhs("joinvc_start").format(em.berhasil, em.group, chat_id)
    
    try:
      if vctitle:
          args += bhs("joinvc_vctitle").format(em.keterangan, vctitle)
          
      await client.invoke(
          CreateGroupCall(
              peer=(await client.resolve_peer(chat_id)),
              random_id=randint(10000, 999999999),
              title=vctitle if vctitle else None,
          )
      )
      await msg.edit(f"<blockquote>{args}</blockquote>")
    except Exception as e:
        await msg.edit(bhs("text_error").format(em.gagal, e))


@PY.UBOT("stopvc", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    msg = await message.reply(bhs("text_proses").format(em.proses))
    group_call = await get_group_call(client, message)
    
    if not group_call:
        return await msg.edit(bhs("joinvc_nostop").format(em.gagal))
    
    await client.invoke(DiscardGroupCall(call=group_call))
    await msg.edit(bhs("joinvc_stopped").format(em.berhasil))


@PY.UBOT("joinvc", sudo=True)
@PY.TOP_CMD
@ubot.on_message(filters.command(["joinvc"], "C") & filters.user(SUDO))
async def _(client, message):
    em = await get_emo(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    titit = await client.get_chat(per)

    if client.me.id not in JOINED_VC:
        JOINED_VC[client.me.id] = {}

    if titit.id in JOINED_VC[client.me.id]:
        return await message.reply(bhs("joinvc_joined").format(em.gagal, titit.title))

    text = f"— <code>{client.me.id}</code> | {titit.title}"

    try:
        group_call = client.group_call
        await group_call.start(titit.id)
        JOINED_VC[client.me.id][titit.id] = group_call
        await message.reply(bhs("joinvc_join").format(em.berhasil, em.group, titit.title))
        add_list(client.me.id, text)
        await asyncio.sleep(2)
        await group_call.set_is_mute(True)
        return
    except Exception as e:
        return await message.reply(bhs("text_error").format(em.gagal, e))


@PY.UBOT("leavevc", sudo=True)
@ubot.on_message(filters.command(["leavevc"], "C") & filters.user(SUDO))
async def _(client, message):
    em = await get_emo(client)
    per = message.command[1] if len(message.command) > 1 else message.chat.id
    titit = await client.get_chat(per)

    # ambil dan hapus dari dict
    group_call = JOINED_VC.get(client.me.id, {}).pop(titit.id, None)
    if not group_call:
        return await message.reply(bhs("joinvc_nleave").format(em.gagal, titit.title))

    try:
        await group_call.stop()
        remove_list(client.me.id)
        return await message.reply(bhs("joinvc_leave").format(em.berhasil, titit.title))
    except Exception as e:
        return await message.reply(bhs("text_error").format(em.gagal, e))


@PY.UBOT("listos")
@PY.OWNER
async def _(client, message):
    await message.reply(get_list())
         

@PY.UBOT("vctitle", sudo=True)
@PY.GROUP
async def _(client, message):
    em = await get_emo(client)
    titit = get_arg(message)
    per = message.command[2] if len(message.command) > 2 else message.chat.id
    msg = await message.reply(bhs("text_proses").format(em.proses))
    group_call = await get_group_call(client, message)
    tit = await client.get_chat(per)

    if len(message.command) < 2:
        return await msg.edit(bhs("joinvc_noteks").format(em.gagal))

    if not group_call:
        return await msg.edit(bhs("joinvc_nostop").format(em.gagal))
    else:
        try:
            await client.invoke(EditGroupCallTitle(call=group_call, title=f"{titit}"))
            await msg.delete()
            return await message.reply(bhs("joinvc_teks").format(em.berhasil, tit.title, titit))
        except Exception as error:
            return await msg.edit(f"ERROR:\n{error}")


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

