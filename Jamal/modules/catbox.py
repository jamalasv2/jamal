import requests

from Jamal import *
from Jamal.core.helpers.class_emoji import get_emo

from langs import bhs, get_bhs


__MODULE__ = "catbox"
__HELP__ = get_bhs("catbox_cmd")

CATBOX_URL = "https://catbox.moe/user/api.php"

@PY.UBOT("catbox", sudo=True)
async def _(client, message):
    em = get_emo(client)
    if not message.reply_to_message or not message.reply_to_message.media:
        return await message.reply(bhs("catbox_nomsg").format(em.gagal))

    msg = await message.reply(bhs("text_proses").format(em.proses))
    
    file_path = await client.download_media(message.reply_to_message)

    with open(file_path, "rb") as f:
        files = {"fileToUpload": f}
        data = {"reqtype": "fileupload"}
        response = requests.post(CATBOX_URL, files=files, data=data)

    if response.status_code == 200 and "https://" in response.text:
        await msg.edit(bhs("catbox_berhasil").format(em.berhasil, em.keterangan, response.text, disable_web_page_preview=True))
        os.remove(file_path)
    else:
        await msg.edit(bhs("catbox_gagal").format(em.gagal, response.text))
