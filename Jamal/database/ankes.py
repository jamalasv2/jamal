from Jamal.database import mongodb

ankesdb = mongodb.ankes

async def get_ankes(user_id):
    chat = await ankesdb.find_one({"chat": user_id})
    if not chat:
        return []
    return chat["list"]


async def add_ankes(user_id, chat_id):
    list = await get_ankes(user_id)
    list.append(chat_id)
    await ankesdb.update_one({"chat": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_ankes(user_id, chat_id):
    list = await get_ankes(user_id)
    list.remove(chat_id)
    await ankesdb.update_one({"chat": user_id}, {"$set": {"list": list}}, upsert=True)
    return True
