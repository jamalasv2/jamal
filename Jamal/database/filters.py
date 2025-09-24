from Jamal.database import mongo_client

collection = mongo_client["Jamal"]["filters"]


# Simpan / update filter
async def save_filter(user_id, keyword, value):
    """
    Simpan filter baru atau update yang lama.
    value: dict -> { "type": "text", "data": "..." } atau { "type": "photo", "message_id": 123 }
    """
    doc = {"_id": user_id, "filters": {keyword: value}}
    result = await collection.find_one({"_id": user_id})
    if result:
        await collection.update_one(
            {"_id": user_id},
            {"$set": {f"filters.{keyword}": value}}
        )
    else:
        await collection.insert_one(doc)


# Ambil filter berdasarkan keyword
async def get_filter(user_id, keyword):
    result = await collection.find_one({"_id": user_id})
    if result is not None:
        return result.get("filters", {}).get(keyword)
    return None


# Hapus 1 filter
async def rm_filter(user_id, keyword):
    await collection.update_one(
        {"_id": user_id},
        {"$unset": {f"filters.{keyword}": ""}}
    )


# Ambil semua filter user
async def all_filters(user_id):
    doc = await collection.find_one({"_id": user_id})
    if not doc:
        return {}
    return doc.get("filters", {})  # <-- dict


# Hapus semua filter user
async def rm_all_filters(user_id):
    await collection.update_one(
        {"_id": user_id},
        {"$unset": {"filters": ""}}
    )


# Cari filter (opsional, buat fitur searchfilters)
async def search_filters(user_id, query):
    """
    Cari filter yang keyword-nya mengandung 'query'.
    """
    result = await collection.find_one({"_id": user_id})
    if not result or "filters" not in result:
        return []
    return [k for k in result["filters"].keys() if query.lower() in k.lower()]
