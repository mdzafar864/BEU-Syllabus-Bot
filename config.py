import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"

# Admin ID from Environment Variable
ADMIN_ID = int(os.getenv("ADMIN_ID"))

LOG_FILE = BASE_DIR / "bot.log"
ANALYTICS_FILE = BASE_DIR / "analytics.json"  # legacy JSON, imported once into MongoDB

# MongoDB Atlas connection string, e.g. mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "beu_syllabus_bot")

WEB_PORT = int(os.getenv("PORT", 8080))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
