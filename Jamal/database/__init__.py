from motor.motor_asyncio import AsyncIOMotorClient

from Jamal.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.jamal_ubot

from Jamal.database.expired import *
from Jamal.database.ankes import *
from Jamal.database.notes import *
from Jamal.database.saved import *
from Jamal.database.userbot import *
from Jamal.database.pref import *
from Jamal.database.otp import *
from jamal.database.variabel import *
