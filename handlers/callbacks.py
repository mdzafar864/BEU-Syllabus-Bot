import os
import logging
from telebot import TeleBot
from utils.validators import is_member
from utils.menu_builder import MenuBuilder
from models.analytics import Analytics
from config import ADMIN_ID

logger = logging.getLogger(__name__)

def register_callback_handlers(bot: TeleBot, analytics: Analytics):
    
    @bot.callback_query_handler(func=lambda call: call.data == "check_join")
    def verify_join(call):
        try:
            if is_member(bot, call.from_user.id):
                bot.answer_callback_query(call.id, "✅ Access Granted! Welcome aboard!")
                bot.send_message(
                    call.message.chat.id,
                    "🎉 *Access Verified!* 🎉\n\n"
                    "Welcome to BEU Syllabus Bot!\n"
                    "Use the menu below to get started.",
                    reply_markup=MenuBuilder.main_menu(),
                    parse_mode='Markdown'
                )
                analytics.track_user(call.from_user.id, "verified")
            else:
                bot.answer_callback_query(
                    call.id, 
                    "❌ Please join the Telegram channel first!", 
                    show_alert=True
                )
        except Exception as e:
            logger.error(f"Error in verify_join: {e}")
    
    @bot.callback_query_handler(func=lambda call: call.data in ["full_stats", "save_data"])
    def admin_callbacks(call):
        try:
            if call.from_user.id != ADMIN_ID:
                bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
                return
            
            if call.data == "full_stats":
                if os.path.exists(analytics.filename):
                    with open(analytics.filename, 'rb') as f:
                        bot.send_document(call.message.chat.id, f, caption="📊 Full analytics data")
                else:
                    bot.send_message(call.message.chat.id, "No analytics data found!")
            
            elif call.data == "save_data":
                analytics.save()
                bot.answer_callback_query(call.id, "✅ Data saved successfully!")
        except Exception as e:
            logger.error(f"Error in admin_callbacks: {e}")