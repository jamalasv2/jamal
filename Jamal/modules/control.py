from PyroUbot import *

__MODULE__ = "control"
__HELP__ = """
<blockquote><b>『 bantuan untuk control 』</b>

**❏ perintah:** <code>{0}setprefix</code>
— untuk merubah prefix atau handler perintah

**❏ perintah:** <code>{0}setemoji</code> query - emoji
— untuk mengubah emoji 

queri :
— <code>pong</code>  — <code>proses</code>
— <code>user</code>  — <code>berhasil</code>
— <code>ubot</code>  — <code>gagal</code>

— <code>keterangan</code>
— <code>waktu</code>
— <code>group</code>

**contoh:**
{0}setemoji pong 🗿</blockquote>
 """

@PY.UBOT("setprefix", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    Tm = await message.reply(f"{prs} ᴍᴇᴍᴘʀᴏsᴇs", quote=True)
    if len(message.command) < 2:
        return await Tm.edit(f"<code>{message.text}</code> sɪᴍʙᴏʟ ᴘʀᴇғɪx")
    else:
        ub_prefix = []
        for prefix in message.command[1:]:
            if prefix.lower() == "none":
                ub_prefix.append("")
            else:
                ub_prefix.append(prefix)
        try:
            client.set_prefix(message.from_user.id, ub_prefix)
            await set_pref(message.from_user.id, ub_prefix)
            parsed_prefix = " ".join(f"<code>{prefix}</code>" for prefix in ub_prefix)
            return await Tm.edit(f"{brhsl}<b> ᴘʀᴇғɪx ᴛᴇʟᴀʜ ᴅɪᴜʙᴀʜ ᴋᴇ: {parsed_prefix}</b>")
        except Exception as error:
            return await Tm.edit(str(error))


@PY.UBOT("setemoji", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    try:
        msg = await message.reply(f"{prs} ᴍᴇᴍᴘʀᴏsᴇs...", quote=True)

        if not client.me.is_premium:
            return await msg.edit(
                "<b>ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ᴀᴋᴜɴ ᴀɴᴅᴀ ʜᴀʀᴜ ᴘʀᴇᴍɪᴜᴍ ᴛᴇʀʟᴇʙɪʜ</b>"
            )

        if len(message.command) < 3:
            return await msg.edit(f"{ggl}<b> ᴛᴏʟᴏɴɢ ᴍᴀsᴜᴋᴋᴀɴ ǫᴜᴇʀʏ ᴅᴀɴ ᴇᴍᴏᴊɪ ɴʏᴀ</b>")

        query_mapping = {
            "pong": "EMOJI_PING",
            "user": "EMOJI_MENTION",
            "ubot": "EMOJI_USERBOT",
            "proses": "EMOJI_PROSES", 
            "berhasil":"EMOJI_BERHASIL",
            "gagal":"EMOJI_GAGAL",
            "keterangan": "EMOJI_BL_KETERANGAN",
            "menunggu": "EMOJI_MENUNGGU",
            "group":"EMOJI_BL_GROUP",
            "broadcast":"EMOJI_BROADCAST",
        }
        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            emoji_id = None
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break

            if emoji_id:
                await set_vars(client.me.id, query_var, emoji_id)
                await msg.edit(
                    f"<b> <code>{query_var}</code>{brhsl} ʙᴇʀʜᴀsɪʟ ᴅɪ sᴇᴛᴛɪɴɢ ᴋᴇ:</b> <emoji id={emoji_id}>{value}</emoji>"
                )
            else:
                await msg.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴇᴍᴏᴊɪ ᴘʀᴇᴍɪᴜᴍ</b>")
        else:
            await msg.edit(f"{ggl}<b> ᴍᴀᴘᴘɪɴɢ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")

    except Exception as error:
        await msg.edit(str(error))

