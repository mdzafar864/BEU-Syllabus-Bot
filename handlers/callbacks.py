import os
import html
import logging
import tempfile
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
    
    @bot.callback_query_handler(func=lambda call: call.data in ["full_stats", "view_feedback"])
    def admin_callbacks(call):
        try:
            if call.from_user.id != ADMIN_ID:
                bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
                return

            if call.data == "full_stats":
                # Send a JSON export of the MongoDB collections
                tmp_path = os.path.join(tempfile.gettempdir(), "bot_data_export.json")
                analytics.export_db(tmp_path)
                with open(tmp_path, 'rb') as f:
                    bot.send_document(call.message.chat.id, f, caption="📊 Database export (MongoDB, JSON)")
                os.remove(tmp_path)
                bot.answer_callback_query(call.id)

            elif call.data == "view_feedback":
                rows = analytics.db.get_recent_feedback(10)
                if not rows:
                    bot.answer_callback_query(call.id)
                    bot.send_message(call.message.chat.id, "📭 No feedback received yet.")
                    return

                text = "📨 <b>Recent Feedback</b> (latest 10)\n"
                for r in rows:
                    who = f"@{html.escape(r['username'])}" if r['username'] else html.escape(r['first_name'] or 'N/A')
                    msg = r['message'] if len(r['message']) <= 150 else r['message'][:150] + "…"
                    status = "✅ replied" if r['replied'] else "🕓 pending"
                    text += (
                        f"\n<b>#{r['id']}</b> · {who} · {status}\n"
                        f"ID: <code>{r['user_id']}</code> · {r['created_at']}\n"
                        f"{html.escape(msg)}\n"
                    )
                text += "\n↩️ Reply with: <code>/reply &lt;user_id&gt; &lt;message&gt;</code>"
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        except Exception as e:
            logger.error(f"Error in admin_callbacks: {e}")
