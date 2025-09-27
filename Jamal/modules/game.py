from Jamal import *


__MODULE__ = "game"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɢᴀᴍᴇ 』</b>

 <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}catur</code>
 <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ʙᴇʀᴍᴀɪɴ ɢᴀᴍᴇ ᴄᴀᴛᴜʀ
  """


@PY.UBOT("catur", sudo=True)
@PY.TOP_CMD
async def _(client, message):
    try:
        x = await client.get_inline_bot_results("GameFactoryBot")
        msg = message.reply_to_message or message
        await client.send_inline_bot_result(
            message.chat.id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
        )
    except Exception as error:
        await message.reply(error)
