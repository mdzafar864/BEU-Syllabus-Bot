import logging
from config import CHANNEL_USERNAME

logger = logging.getLogger(__name__)

def is_member(bot, user_id: int) -> bool:
    """Check if user is a member of the channel"""
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Membership check failed for {user_id}: {e}")
        return False

def check_join_required(bot, message) -> bool:
    """Check if user needs to join channel"""
    if not is_member(bot, message.chat.id):
        from utils.menu_builder import MenuBuilder
        try:
            bot.send_message(
                message.chat.id,
                "🔒 *Access Restricted*\n\n"
                "To access the syllabus and all features, you must join our Telegram channel:\n\n"
                "✅ Join Telegram Channel\n\n"
                "After joining, click the button below to verify access.",
                reply_markup=MenuBuilder.force_join_markup(),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending join required message: {e}")
        return True
    return False