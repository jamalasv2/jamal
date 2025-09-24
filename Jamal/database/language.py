from Jamal.database import mongodb

# Ambil collection 'users' di database Jamal.language
langs = mongodb["Jamal"]["language"]["users"]

# Cache dictionary
langm = {}

async def get_lang(user_id: int):
    mode = langm.get(user_id)
    if not mode:
        lang = await langs.find_one({"_id": user_id})
        if not lang:
            langm[user_id] = "id"
            return "id"
        langm[user_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(user_id: int, lang: str):
    langm[user_id] = lang
    await langs.update_one(
        {"_id": user_id},
        {"$set": {"lang": lang}},
        upsert=True
    )
