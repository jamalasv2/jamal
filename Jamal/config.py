import os

DEVS = list(map(int, os.getenv("DEVS", "6442845161").split()))
SUDO = list(map(int, os.getenv("SUDO", "6442845161").split()))

API_ID = int(os.getenv("API_ID", "21839531"))
API_HASH = os.getenv("API_HASH", "2ea72246a26c4c29cc419175f738efa3")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8315033881:AAGofWP2jiGd6jwzyBsbCYZWOp1GDr6UfB4")
OWNER_ID = int(os.getenv("OWNER_ID", "6442845161"))
BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002023991424").split()))
SUPPORT = int(os.getenv("SUPPORT", "-1002023991424"))
LOG_SELES = int(os.getenv("LOG_SELES", "-1002291357152"))
MAX_BOT = int(os.getenv("MAX_BOT", "100"))
RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")
BAHASA = os.getenv("BAHASA", "id")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "AIzaSyAHG93LY01ZEnpGTdaqMQZj-d1mPR5au-8",
)
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://higanprem:1234@cluster0.mhdfibu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)
