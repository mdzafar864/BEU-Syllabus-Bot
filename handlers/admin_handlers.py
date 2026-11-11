import logging
import time
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import html
from utils.menu_builder import MenuBuilder
from utils.helpers import format_download_label
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
                f"<b>Total Users:</b> {analytics.get_total_users()}\n"
                f"<b>Active Today:</b> {analytics.get_active_today()}\n"
                f"<b>Total Downloads:</b> {analytics.get_total_downloads()}\n"
                f"<b>Unanswered Feedback:</b> {analytics.db.count_unreplied_feedback()}\n\n"
                "<b>Top Downloads:</b>\n"
            )
            
            top_downloads = analytics.get_top_downloads(10)
            if top_downloads:
                for sem, sess, branch, count in top_downloads:
                    admin_text += f"• {format_download_label(sem, sess, branch)}: {count}\n"
            else:
                admin_text += "• No downloads yet\n"

            admin_text += (
                "\n<b>Reply to a user:</b>\n"
                "<code>/reply &lt;user_id&gt; &lt;message&gt;</code>\n"
                "<i>Tap “Feedback &amp; Reply” below to see user IDs.</i>"
            )
            
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
            
            for user_id in analytics.get_all_user_ids():
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
                f"👥 <b>Total Users:</b> {analytics.get_total_users()}\n"
                f"📅 <b>Active Today:</b> {analytics.get_active_today()}\n"
                f"📚 <b>Total Downloads:</b> {analytics.get_total_downloads()}\n\n"
                "🖱️ <b>Button / Command Clicks:</b>\n"
            )
            
            for button, count in analytics.get_button_stats(10):
                stats_text += f"• {html.escape(button)}: {count}\n"
            
            bot.send_message(message.chat.id, stats_text, parse_mode='HTML')
        except Exception as e:
            logger.exception("Error in user_stats")

    @bot.message_handler(commands=['reply'])
    def reply_to_user(message):
        """Admin-only: /reply <user_id> <message> -> send a direct reply to a stored user."""
        try:
            if message.from_user.id != ADMIN_ID:
                bot.send_message(
                    message.chat.id,
                    "⚠️ *Admin Access Required*\n\nYou don't have permission to access this section.",
                    parse_mode='Markdown'
                )
                return

            parts = (message.text or "").split(maxsplit=2)
            if len(parts) < 3 or not parts[1].isdigit() or not parts[2].strip():
                bot.send_message(
                    message.chat.id,
                    "⚠️ Usage: /reply <user_id> <message>\n"
                    "Open /admin → “Feedback & Reply” to find user IDs."
                )
                return

            target_id = int(parts[1])
            reply_text = parts[2].strip()

            # Only reply to IDs we have actually stored
            if not analytics.db.user_exists(target_id):
                bot.send_message(
                    message.chat.id,
                    f"❌ User ID {target_id} was not found in the database."
                )
                return

            try:
                # Plain text (no parse_mode) so any characters in the reply are safe
                bot.send_message(target_id, f"💬 Reply from Admin\n\n{reply_text}")
            except Exception as send_error:
                logger.error(f"Reply to {target_id} failed: {send_error}")
                bot.send_message(
                    message.chat.id,
                    f"❌ Could not deliver the reply to {target_id} "
                    "(the user may have blocked the bot)."
                )
                return

            updated = analytics.db.mark_feedback_replied(target_id, reply_text)
            bot.send_message(
                message.chat.id,
                f"✅ Reply sent to {target_id}."
                + (f"\n📌 {updated} feedback item(s) marked as replied." if updated else "")
            )
            logger.info(f"Admin replied to user {target_id}")
        except Exception:
            logger.exception("Error in reply_to_user")
