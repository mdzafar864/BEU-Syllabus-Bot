import logging
import threading
import time
from datetime import datetime, timedelta

import telebot

from config import TOKEN, LOG_FILE, BASE_DIR, WEB_PORT
from models.user_session import UserSession
from models.analytics import Analytics
from handlers import (
    register_base_handlers,
    register_syllabus_handlers,
    register_admin_handlers,
    register_callback_handlers
)
from data.syllabus import SYLLABUS

# ================== LOGGING SETUP ==================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================== BOT INITIALIZATION ==================
bot = telebot.TeleBot(TOKEN)
user_session = UserSession()
analytics = Analytics()

# ================== REGISTER HANDLERS ==================
# NOTE: base_handlers must be registered LAST because it contains a
# catch-all handler (func=lambda m: True) for unknown commands.
# pyTelegramBotAPI stops at the FIRST handler whose condition matches,
# in registration order — so if base_handlers went first, its catch-all
# would swallow every message (like the "Syllabus" button) before
# syllabus/admin handlers ever got a chance to run.
register_syllabus_handlers(bot, analytics, user_session)
register_admin_handlers(bot, analytics)
register_callback_handlers(bot, analytics)
register_base_handlers(bot, analytics, user_session)

# ================== DAILY RESET SCHEDULER ==================
def daily_reset():
    while True:
        try:
            now = datetime.now()
            next_reset = datetime(now.year, now.month, now.day) + timedelta(days=1)
            sleep_seconds = (next_reset - now).total_seconds()
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
                analytics.reset_daily()
        except Exception as e:
            logger.error(f"Error in daily_reset: {e}")
            time.sleep(3600)

# ================== HEALTH CHECK SERVER ==================
def start_health_server():
    try:
        from flask import Flask, jsonify
        flask_app = Flask(__name__)
        
        @flask_app.route('/')
        def health():
            return "✅ BEU Syllabus Bot is running!", 200
        
        @flask_app.route('/health')
        def health_check():
            return jsonify({
                "status": "healthy",
                "users": len(analytics.total_users),
                "downloads": analytics.get_total_downloads()
            }), 200
        
        flask_app.run(host='0.0.0.0', port=WEB_PORT, debug=False)
    except ImportError:
        logger.warning("⚠️ Flask not installed. Install with: pip install flask")
    except Exception as e:
        logger.error(f"Error starting health server: {e}")

# ================== BOT RUN WITH AUTO-RESTART ==================
def run_bot():
    while True:
        try:
            logger.info("🚀 Starting bot...")
            bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            logger.info("Restarting bot in 10 seconds...")
            time.sleep(10)

# ================== MAIN ENTRY POINT ==================
if __name__ == "__main__":
    logger.info("🚀 BEU Syllabus Bot Starting on Railway!")
    logger.info(f"Base Directory: {BASE_DIR}")
    
    if not TOKEN:
        logger.error("❌ BOT_TOKEN environment variable not set!")
        raise ValueError("BOT_TOKEN is required")
    
    try:
        bot_info = bot.get_me()
        logger.info(f"✅ Bot Username: @{bot_info.username}")
        logger.info(f"✅ Bot ID: {bot_info.id}")
    except Exception as e:
        logger.error(f"❌ Failed to get bot info: {e}")
        raise
    
    logger.info(f"📚 Total Semesters: {len(SYLLABUS)}")
    
    # Start daily reset thread
    try:
        reset_thread = threading.Thread(target=daily_reset, daemon=True)
        reset_thread.start()
        logger.info("✅ Daily reset scheduler started")
    except Exception as e:
        logger.warning(f"⚠️ Daily reset scheduler not started: {e}")
    
    # Start health check server
    try:
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        logger.info(f"✅ Health check server started on port {WEB_PORT}")
    except Exception as e:
        logger.warning(f"⚠️ Health server not started: {e}")
    
    # Start bot with auto-restart
    run_bot()