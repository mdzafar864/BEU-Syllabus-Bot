from datetime import datetime
import logging
from telebot import TeleBot
from utils.menu_builder import MenuBuilder
from utils.validators import check_join_required
from models.analytics import Analytics
from models.user_session import UserSession
from data.constants import MENU_BUTTONS
import html
from utils.helpers import format_download_label

logger = logging.getLogger(__name__)

def register_base_handlers(bot: TeleBot, analytics: Analytics, user_session: UserSession):
    
    @bot.message_handler(commands=['start', 'menu'])
    def start(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "start")
            user_session.clear(message.chat.id)
            
            welcome_text = (
                "🎓 *BEU Syllabus Bot* 🎓\n\n"
                "📚 *Available Features:*\n"
                "• Download semester-wise syllabus\n"
                "• Branch-wise syllabus access\n"
                "• Share syllabus with friends\n\n"
                "💡 *How to use:*\n"
                "1️⃣ Click '📚 Syllabus'\n"
                "2️⃣ Select your branch\n"
                "3️⃣ Choose your semester\n"
                "4️⃣ Choose your academic session\n"
                "5️⃣ Download or share your syllabus!\n\n"
                "📊 Check stats to see bot usage!"
            )
            
            bot.send_message(
                message.chat.id,
                welcome_text,
                reply_markup=MenuBuilder.main_menu(),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in start: {e}")
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["HELP"])
    def show_help(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "help")
            
            help_text = (
                "📚 *Help & Guide*\n\n"
                "*How to use:*\n"
                "1. Tap '📚 Syllabus'\n"
                "2. Choose your branch\n"
                "3. Select your semester\n"
                "4. Select your academic session\n"
                "5. Download or share PDF\n\n"
                "*Features:*\n"
                "• ⬇️ Download PDF - Save syllabus to device\n"
                "• 📤 Share - Share syllabus with friends\n\n"
                "*Commands:*\n"
                "/start - Restart bot\n"
                "/menu - Show main menu\n\n"
                "👨‍💻 *Contact Developer:* [Click Here](https://www.linkedin.com/in/mdzafar864)"
            )
            
            bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error in show_help: {e}")
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["STATS"])
    def show_stats(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "stats")
            
            stats_text = (
                "📊 *Bot Statistics*\n\n"
                f"👥 *Total Users:* {analytics.get_total_users():,}\n"
                f"📅 *Active Today:* {analytics.get_active_today():,}\n"
                f"📚 *Total Downloads:* {analytics.get_total_downloads():,}\n\n"
                "📈 *Popular Downloads:*\n"
            )
            
            top_downloads = analytics.get_top_downloads(5)
            if top_downloads:
                for sem, sess, branch, count in top_downloads:
                    stats_text += f"• {format_download_label(sem, sess, branch)}: {count}\n"
            else:
                stats_text += "• No downloads yet\n"
            
            stats_text += f"\n🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}"
            
            bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error in show_stats: {e}")
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["FEEDBACK"])
    def get_feedback(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "feedback")
            
            feedback_text = (
                "💬 *Send Feedback*\n\n"
                "We value your feedback! Please send your:\n"
                "• Suggestions for improvement\n"
                "• Bug reports\n"
                "• Feature requests\n\n"
                "Just type your message below, and it will be forwarded to the admin."
            )
            bot.send_message(message.chat.id, feedback_text, parse_mode='Markdown')
            bot.register_next_step_handler(message, process_feedback)
        except Exception as e:
            logger.error(f"Error in get_feedback: {e}")
    
    def process_feedback(message):
        try:
            feedback_content = (message.text or "").strip()
            if not feedback_content:
                bot.send_message(
                    message.chat.id,
                    "⚠️ Please send your feedback as a *text message*. Tap ⭐ Feedback to try again.",
                    reply_markup=MenuBuilder.main_menu(),
                    parse_mode='Markdown'
                )
                return

            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            user_id = message.from_user.id

            from config import ADMIN_ID

            # Store the feedback together with the sender's user ID
            feedback_id = analytics.db.add_feedback(
                user_id, username, first_name, last_name, feedback_content
            )

            # HTML + escaping so user text can't break the formatting
            esc = html.escape
            feedback_msg = (
                f"📝 <b>New Feedback #{feedback_id}</b>\n\n"
                f"👤 <b>User Information:</b>\n"
                f"├ First Name: <code>{esc(first_name or 'N/A')}</code>\n"
                f"├ Last Name: <code>{esc(last_name or 'N/A')}</code>\n"
                f"├ Username: {('@' + esc(username)) if username else 'N/A'}\n"
                f"└ User ID: <code>{user_id}</code>\n\n"
                f"💬 <b>Feedback Message:</b>\n"
                f"└ {esc(feedback_content)}\n\n"
                f"🕐 <b>Time:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                f"↩️ Reply with: <code>/reply {user_id} your message</code>"
            )

            bot.send_message(ADMIN_ID, feedback_msg, parse_mode='HTML')

            bot.send_message(
                message.chat.id,
                "✅ *Thank you for your feedback!*\n\n"
                "Your message has been sent to the admin.\n\n"
                "🙏 Thanks for helping us improve!",
                reply_markup=MenuBuilder.main_menu(),
                parse_mode='Markdown'
            )

            logger.info(f"Feedback #{feedback_id} stored from user {user_id} (@{username})")

        except Exception as e:
            logger.error(f"Error in process_feedback: {e}")
            bot.send_message(
                message.chat.id,
                "⚠️ *Sorry!*\n\n"
                "There was an issue sending your feedback. Please try again later.",
                reply_markup=MenuBuilder.main_menu(),
                parse_mode='Markdown'
            )

    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["RESET"])
    def reset_session(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "reset")
            user_session.clear(message.chat.id)
            bot.send_message(
                message.chat.id,
                "🔄 Session reset! You can start fresh now.",
                reply_markup=MenuBuilder.main_menu()
            )
        except Exception as e:
            logger.error(f"Error in reset_session: {e}")
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["MAIN_MENU"])
    def back_to_main_menu(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "main_menu")
            user_session.clear(message.chat.id)
            start(message)
        except Exception as e:
            logger.error(f"Error in back_to_main_menu: {e}")
    
    @bot.message_handler(func=lambda m: True)
    def handle_unknown(message):
        try:
            if check_join_required(bot, message):
                return
            
            analytics.track_user(message.chat.id, "unknown")
            
            bot.send_message(
                message.chat.id,
                "❓ *Unknown Command*\n\n"
                "Please use the menu buttons below or type /start to restart.",
                reply_markup=MenuBuilder.main_menu(),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in handle_unknown: {e}")                          
