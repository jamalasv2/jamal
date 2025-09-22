from Jamal.database import mongodb

ubotdb = mongodb.ubot

async def add_ubot(user_id, api_id, api_hash, session_string):
    return await ubotdb.update_one(
        {"user_id": int(user_id)},
        {"$set": {
            "user_id": int(user_id),
            "api_id": int(api_id),
            "api_hash": api_hash,
            "session_string": session_string,
        }},
        upsert=True,
    )

async def remove_ubot(user_id):
    return await ubotdb.delete_one({"user_id": int(user_id)})

async def get_userbots():
    data = []
    async for ubot in ubotdb.find({"user_id": {"$exists": True}}):
        data.append(
            dict(
                user_id=int(ubot["user_id"]),
                api_id=int(ubot["api_id"]),
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data