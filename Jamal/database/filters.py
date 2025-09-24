from Jamal.database import mongo_client

collection = mongo_client["Jamal"]["filters"]


async def add_filter(user_id, filters_name, message):
    doc = {"_id": user_id, "filters": {filters_name: message}}
    result = await collection.find_one({"_id": user_id})
    if result:
        await collection.update_one(
            {"_id": user_id}, {"$set": {f"filters.{filters_name}": message}}
        )
    else:
        await collection.insert_one(doc)

async def get_filter(chat_id: int, keyword: str, owner: int):
    doc = await filters_col.find_one(
        {"chat_id": chat_id, "keyword": keyword.lower(), "owner": owner}
    )
    return doc["reply_text"] if doc else None

async def delete_filter(chat_id: int, keyword: str, owner: int):
    await filters_col.delete_one(
        {"chat_id": chat_id, "keyword": keyword.lower(), "owner": owner}
    )

async def get_all_filters(chat_id: int, owner: int):
    cursor = filters_col.find({"chat_id": chat_id, "owner": owner})
    return [doc async for doc in cursor]



