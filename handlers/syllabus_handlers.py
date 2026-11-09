import logging
from datetime import datetime
from telebot import TeleBot
from data.syllabus import (
    SEMESTERS,
    SEMESTER_NAMES,
    get_syllabus_link,
    get_sessions_for,
)
from data.constants import BRANCH_EMOJIS, MENU_BUTTONS
from utils.menu_builder import MenuBuilder
from utils.helpers import (
    get_download_link,
    download_drive_file,
    format_branch_text,
    format_semester_text,
    format_session_text,
)
from utils.validators import check_join_required
from models.analytics import Analytics
from models.user_session import UserSession

logger = logging.getLogger(__name__)

SEMESTER_PREFIX = "📖 "
SESSION_PREFIX = "🗓️ "

# Reverse lookups: button label -> internal key
SEMESTER_BUTTONS = {f"{SEMESTER_PREFIX}{SEMESTER_NAMES.get(s, s)}": s for s in SEMESTERS}


def register_syllabus_handlers(bot: TeleBot, analytics: Analytics, user_session: UserSession):

    # ---------- helpers ----------
    def send_branch_menu(chat_id):
        user_session.set(chat_id, "selected_branch", None)
        user_session.set(chat_id, "selected_semester", None)
        user_session.set(chat_id, "step", "waiting_for_branch")
        bot.send_message(
            chat_id,
            format_branch_text(),
            reply_markup=MenuBuilder.branch_first_menu(),
            parse_mode='Markdown'
        )

    def send_semester_menu(chat_id, branch):
        user_session.set(chat_id, "selected_branch", branch)
        user_session.set(chat_id, "selected_semester", None)
        user_session.set(chat_id, "step", "waiting_for_semester")
        bot.send_message(
            chat_id,
            format_semester_text(branch),
            reply_markup=MenuBuilder.semester_menu(),
            parse_mode='Markdown'
        )

    # ---------- step 0: Syllabus button -> branches ----------
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["SYLLABUS"])
    def show_branches_first(message):
        try:
            if check_join_required(bot, message):
                return

            analytics.track_user(message.chat.id, "syllabus")
            send_branch_menu(message.chat.id)
        except Exception as e:
            logger.error(f"Error in show_branches_first: {e}")

    # ---------- step 1: branch -> ALL semesters ----------
    @bot.message_handler(func=lambda m: m.text in list(BRANCH_EMOJIS.values()))
    def branch_selected_first(message):
        try:
            if check_join_required(bot, message):
                return

            analytics.track_user(message.chat.id, "branch_select")

            selected_branch = next(
                (b for b, name in BRANCH_EMOJIS.items() if name == message.text), None
            )
            if not selected_branch:
                bot.send_message(message.chat.id, "❌ Invalid branch!")
                return

            send_semester_menu(message.chat.id, selected_branch)

        except Exception as e:
            logger.error(f"Error in branch_selected_first: {e}")
            bot.send_message(
                message.chat.id,
                "⚠️ Error! Please try again.",
                reply_markup=MenuBuilder.main_menu()
            )

    # ---------- step 2: semester -> session picker ----------
    @bot.message_handler(func=lambda m: m.text in SEMESTER_BUTTONS)
    def semester_selected(message):
        try:
            if check_join_required(bot, message):
                return

            analytics.track_user(message.chat.id, "semester_select")

            semester = SEMESTER_BUTTONS[message.text]
            session = user_session.get(message.chat.id)

            if not session or not session.get("selected_branch"):
                bot.send_message(
                    message.chat.id,
                    "⚠️ पहले Branch चुनें!",
                    reply_markup=MenuBuilder.branch_first_menu()
                )
                return

            branch = session["selected_branch"]
            sessions = get_sessions_for(semester, branch)

            if not sessions:
                bot.send_message(
                    message.chat.id,
                    f"❌ {BRANCH_EMOJIS.get(branch, branch)} branch का "
                    f"{SEMESTER_NAMES.get(semester, semester)} का syllabus अभी उपलब्ध नहीं है।\n\n"
                    "कृपया कोई दूसरा Semester चुनें।",
                    reply_markup=MenuBuilder.semester_menu()
                )
                return

            user_session.set(message.chat.id, "selected_semester", semester)
            user_session.set(message.chat.id, "step", "waiting_for_session")

            bot.send_message(
                message.chat.id,
                format_session_text(branch, semester, sessions),
                reply_markup=MenuBuilder.session_menu(sessions),
                parse_mode='Markdown'
            )

        except Exception as e:
            logger.error(f"Error in semester_selected: {e}")
            bot.send_message(message.chat.id, "⚠️ Error! Please try again.")

    # ---------- step 3: session -> send the PDF ----------
    @bot.message_handler(func=lambda m: m.text and m.text.startswith(SESSION_PREFIX))
    def session_selected(message):
        try:
            if check_join_required(bot, message):
                return

            analytics.track_user(message.chat.id, "session_select")

            academic_session = message.text[len(SESSION_PREFIX):].strip()
            data = user_session.get(message.chat.id) or {}
            branch = data.get("selected_branch")
            semester = data.get("selected_semester")

            if not branch:
                bot.send_message(
                    message.chat.id,
                    "⚠️ पहले Branch चुनें!",
                    reply_markup=MenuBuilder.branch_first_menu()
                )
                return

            if not semester:
                bot.send_message(
                    message.chat.id,
                    "⚠️ पहले Semester चुनें!",
                    reply_markup=MenuBuilder.semester_menu()
                )
                return

            original_url = get_syllabus_link(semester, academic_session, branch)
            if not original_url:
                bot.send_message(
                    message.chat.id,
                    f"❌ {BRANCH_EMOJIS.get(branch, branch)} - "
                    f"{SEMESTER_NAMES.get(semester, semester)} ({academic_session}) "
                    "का syllabus उपलब्ध नहीं है।",
                    reply_markup=MenuBuilder.session_menu(get_sessions_for(semester, branch))
                )
                return

            download_url = get_download_link(original_url)

            analytics.track_download(message.chat.id, semester, branch, academic_session)
            key = f"{semester}_{academic_session}_{branch}"

            markup = MenuBuilder.download_markup(download_url, semester, academic_session, branch)

            bot.send_chat_action(message.chat.id, 'upload_document')

            caption = (
                f"📚 *{SEMESTER_NAMES.get(semester, semester)} - "
                f"{BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n"
                f"🗓️ *Session:* {academic_session}\n\n"
                f"📅 *Requested:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
                f"📊 *Downloads Today:* {analytics.daily_downloads.get(key, 0)}"
            )

            file_bytes = download_drive_file(original_url)

            if file_bytes is not None:
                try:
                    bot.send_document(
                        message.chat.id,
                        file_bytes,
                        visible_file_name=f"{semester}_{academic_session}_{branch}_Syllabus.pdf",
                        caption=caption,
                        reply_markup=markup,
                        parse_mode='Markdown'
                    )
                    logger.info(
                        f"Syllabus sent: {semester} - {academic_session} - {branch} "
                        f"to user {message.chat.id}"
                    )
                except Exception as doc_error:
                    logger.error(f"Document send failed: {doc_error}")
                    file_bytes = None

            if file_bytes is None:
                bot.send_message(
                    message.chat.id,
                    f"{caption}\n\n"
                    f"⚠️ PDF सीधे नहीं भेज पाए, नीचे दिए गए बटन से download करें।",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )

        except Exception as e:
            logger.error(f"Error in session_selected: {e}")
            bot.send_message(message.chat.id, "⚠️ Error! Please try again.")

    # ---------- navigation ----------
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["BACK_TO_SEMESTERS"])
    def back_to_semesters(message):
        try:
            if check_join_required(bot, message):
                return

            analytics.track_user(message.chat.id, "back_to_semesters")
            branch = user_session.get_branch(message.chat.id)
            if not branch:
                send_branch_menu(message.chat.id)
                return
            send_semester_menu(message.chat.id, branch)
        except Exception as e:
            logger.error(f"Error in back_to_semesters: {e}")

    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["BACK_TO_BRANCHES"])
    def back_to_branches(message):
        try:
            if check_join_required(bot, message):
                return

            analytics.track_user(message.chat.id, "back_to_branches")
            send_branch_menu(message.chat.id)
        except Exception as e:
            logger.error(f"Error in back_to_branches: {e}")
