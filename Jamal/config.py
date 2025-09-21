import os

DEVS = list(map(int, os.getenv("DEVS", "6625839378").split()))
SUDO = list(map(int, os.getenv("SUDO", "").split()))


API_ID = int(os.getenv("API_ID", "26394847"))
API_HASH = os.getenv("API_HASH", "cd52ac30233feb251a5c7fbdbdacb414")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8389602601:AAF3M8a9I8tF-p-k-zxH5KKxGO2WqH9PW28")
OWNER_ID = int(os.getenv("OWNER_ID", "6625839378"))
BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002023991424").split()))
SUPPORT = int(os.getenv("SUPPORT", "-1002023991424"))
LOG_SELES = int(os.getenv("LOG_SELES", "-1002291357152"))
MAX_BOT = int(os.getenv("MAX_BOT", "100"))
RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")
BAHASA = os.getenv("BAHASA", "en")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "AIzaSyAHG93LY01ZEnpGTdaqMQZj-d1mPR5au-8",
)
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://higanubot:1234@cluster0.6eqqisq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)