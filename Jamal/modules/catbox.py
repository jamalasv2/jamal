import requests

from Jamal import *
from Jamal.core import *


__MODULE__ = "catbox"
__HELP__ = """
<BLOCKQUOTE>**『 bantuan untuk catbox 』**

**❏ perintah:** <code>{0}catbox</code> [ balas pesan dokumen ]
— untuk mengunggah foto / video ke catbox</BLOCKQUOTE>
"""

CATBOX_URL = "https://catbox.moe/user/api.php"

@PY.UBOT("catbox", sudo=True)
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrg = await EMO.BL_KETERANGAN(client)
    if not message.reply_to_message or not message.reply_to_message.media:
        return await message.reply(
            f"{ggl}**balas ke media atau berkas**"
        )

    msg = await message.reply(f"**{prs}mengunggah ke catbox..")
    
    file_path = await client.download_media(message.reply_to_message)

    with open(file_path, "rb") as f:
        files = {"fileToUpload": f}
        data = {"reqtype": "fileupload"}
        response = requests.post(CATBOX_URL, files=files, data=data)

    if response.status_code == 200 and "https://" in response.text:
        await msg.edit(
            f"**{brhsl}berhasil diunggah ke catbox\n{ktrg}tautan:** {response.text}", disable_web_page_preview=True
        )
        os.remove(file_path)
    else:
        await msg.edit(f"{ggl}gagal mengunggah ke catbox!**\n`{response.text}`")
