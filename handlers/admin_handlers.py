import logging
import time
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.menu_builder import MenuBuilder
from models.analytics import Analytics
from config import ADMIN_ID

logger = logging.getLogger(__name__)

def register_admin_handlers(bot: TeleBot, analytics: Analytics):
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        try:
            if message.from_user.id != ADMIN_ID:
                bot.send_message(
                    message.chat.id, 
                    "⚠️ *Admin Access Required*\n\nYou don't have permission to access this section.", 
                    parse_mode='Markdown'
                )
                return
            
            admin_text = (
                "<b>Admin Panel</b>\n\n"
                "<i>Access verified successfully. Welcome, Admin!</i>\n\n"
                f"<b>Total Users:</b> {len(analytics.total_users)}\n"
                f"<b>Active Today:</b> {len(analytics.daily_active)}\n"
                f"<b>Total Downloads:</b> {sum(analytics.daily_downloads.values())}\n\n"
                "<b>Top Downloads:</b>\n"
            )
            
            top_downloads = analytics.get_top_downloads(10)
            for sem_branch, count in top_downloads:
                admin_text += f"• {sem_branch}: {count}\n"
            
            markup = MenuBuilder.admin_markup()
            
            bot.send_message(message.chat.id, admin_text, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            logger.error(f"Error in admin_panel: {e}")
    
    @bot.message_handler(commands=['broadcast'])
    def broadcast_message(message):
        try:
            if message.from_user.id != ADMIN_ID:
                bot.send_message(
                    message.chat.id, 
                    "⚠️ *Admin Access Required*\n\nYou don't have permission to access this section.", 
                    parse_mode='Markdown'
                )
                return
            
            msg = message.text.replace('/broadcast', '').strip()
            if not msg:
                bot.send_message(message.chat.id, "⚠️ Usage: /broadcast <message>")
                return
            
            success = 0
            failed = 0
            
            status_msg = bot.send_message(message.chat.id, "📤 Sending broadcast...")
            
            for user_id in list(analytics.total_users):
                try:
                    bot.send_message(user_id, f"📢 *Announcement*\n\n{msg}", parse_mode='Markdown')
                    success += 1
                except:
                    failed += 1
                time.sleep(0.1)
            
            bot.edit_message_text(
                f"✅ Broadcast completed!\n\n"
                f"✓ Success: {success}\n"
                f"✗ Failed: {failed}",
                message.chat.id,
                status_msg.message_id
            )
        except Exception as e:
            logger.error(f"Error in broadcast_message: {e}")
    
    @bot.message_handler(commands=['stats'])
    def user_stats(message):
        try:
            if message.from_user.id != ADMIN_ID:
                bot.send_message(
                    message.chat.id, 
                    "⚠️ *Admin Access Required*\n\nYou don't have permission to access this section.", 
                    parse_mode='Markdown'
                )
                return
            
            stats_text = (
                "📊 <b>Detailed Statistics</b>\n\n"
                f"👥 <b>Total Users:</b> {len(analytics.total_users)}\n"
                f"📅 <b>Active Today:</b> {len(analytics.daily_active)}\n"
                f"📚 <b>Total Downloads:</b> {sum(analytics.daily_downloads.values())}\n\n"
                "📈 <b>Command Usage:</b>\n"
            )
            
            for cmd, count in sorted(analytics.command_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
                stats_text += f"• /{cmd}: {count}\n"
            
            bot.send_message(message.chat.id, stats_text, parse_mode='HTML')
        except Exception as e:
            logger.exception("Error in user_stats")
