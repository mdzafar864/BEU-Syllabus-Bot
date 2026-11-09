import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"

# Admin ID from Environment Variable
ADMIN_ID = int(os.getenv("ADMIN_ID"))

LOG_FILE = BASE_DIR / "bot.log"
ANALYTICS_FILE = BASE_DIR / "analytics.json"  # legacy JSON, imported once into SQLite
DB_FILE = os.getenv("DB_PATH", str(BASE_DIR / "bot_data.db"))

WEB_PORT = int(os.getenv("PORT", 8080))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
