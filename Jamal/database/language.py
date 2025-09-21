from Jamal.database import mongodb

langs = mongodb["Jamal"]["language"]

async def get_lang(user_id):
    mode = langm.get(user_id)
    if not mode:
        lang = await langs.users.find_one({"_id": user_id})
        if not lang:
            langm[user_id] = "en"
            return "en"
        langm[user_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(user_id):
    langm[user_id] = lang
    await langs.users.update_one({"_id": user_id}, {"$set": {"lang": lang}}, upsert=True)
