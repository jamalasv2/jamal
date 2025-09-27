from Jamal import *
from Jamal.core.helpers import get_emo
from langs import bhs, get_bhs

__MODULE__ = "set"
__HELP__ = get_bhs("set_cmd")

@PY.UBOT("setprefix", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    Tm = await message.reply(bhs("text_proses").format(em.proses))
    if len(message.command) < 2:
        return await Tm.edit(bhs("set_nop").format(em.gagal, message.text))
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
            return await Tm.edit(bhs("set_pre").format(em.berhasil, parsed_prefix))
        except Exception as error:
            return await Tm.edit(bhs("text_error").format(em.gagal, error))


@PY.UBOT("setemoji", sudo=True)
async def _(client, message):
    em = await get_emo(client)
    try:
        msg = await message.reply(bhs("text_proses").format(em.proses))

        if len(message.command) < 3:
            return await msg.edit(bhs("set_que").format(em.gagal))

        query_mapping = {
            "ping": "EMOJI_PING",
            "mention": "EMOJI_MENTION",
            "ubot": "EMOJI_USERBOT",
            "proses": "EMOJI_PROSES", 
            "berhasil":"EMOJI_BERHASIL",
            "gagal":"EMOJI_GAGAL",
            "keterangan": "EMOJI_BL_KETERANGAN",
            "waktu": "EMOJI_MENUNGGU",
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
                await msg.edit(bhs("set_sukses").format(em.berhasil, query_var, value))
    
            else:
                await msg.edit(bhs("set_fail").format(em.gagal))
        else:
            await msg.edit(bhs("set_qfail").format(em.gagal))

    except Exception as error:
        await msg.edit(bhs("text_error").format(em.gagal, error))

