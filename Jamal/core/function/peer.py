from Jamal import *

async def install_my_peer(client):
    """Cache peer agar command bisa lebih cepat"""
    try:
        await client.get_dialogs()  # fetch semua chat
        print(f"Peer installed for {client.me.id}")
    except Exception as e:
        print(f"Gagal install peer {client.me.id}: {e}")