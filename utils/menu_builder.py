from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from data.constants import BRANCH_EMOJIS, MENU_BUTTONS
from data.syllabus import SEMESTERS, SEMESTER_NAMES

class MenuBuilder:
    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [
            MENU_BUTTONS["SYLLABUS"],
            MENU_BUTTONS["STATS"],
            MENU_BUTTONS["HELP"],
            MENU_BUTTONS["FEEDBACK"],
            MENU_BUTTONS["RESET"]
        ]
        markup.add(*buttons)
        return markup
    
    @staticmethod
    def branch_first_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [f"{BRANCH_EMOJIS.get(b, b)}" for b in BRANCH_EMOJIS.keys()]
        markup.add(*buttons)
        markup.add(MENU_BUTTONS["MAIN_MENU"])
        return markup
    
    @staticmethod
    def semester_menu() -> ReplyKeyboardMarkup:
        """All semesters (1st-8th), shown after a branch is selected."""
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [f"📖 {SEMESTER_NAMES.get(sem, sem)}" for sem in SEMESTERS]
        markup.add(*buttons)
        markup.add(MENU_BUTTONS["BACK_TO_BRANCHES"], MENU_BUTTONS["MAIN_MENU"])
        return markup

    @staticmethod
    def session_menu(sessions: list) -> ReplyKeyboardMarkup:
        """Academic sessions available for the chosen branch + semester."""
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [f"🗓️ {s}" for s in sessions]
        markup.add(*buttons)
        markup.add(MENU_BUTTONS["BACK_TO_SEMESTERS"], MENU_BUTTONS["MAIN_MENU"])
        return markup
    
    @staticmethod
    def force_join_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📢 Join Telegram Channel", url="https://t.me/EngineersPathwayOfficial"),
            InlineKeyboardButton("✅ I've Joined", callback_data="check_join")
        )
        return markup
    
    @staticmethod
    def download_markup(download_url: str, semester: str, session: str, branch: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⬇️ Download PDF", url=download_url),
            InlineKeyboardButton("📤 Share Syllabus", switch_inline_query=f"{semester} {session} {branch} Syllabus")
        )
        return markup
    
    @staticmethod
    def admin_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📊 Export Database", callback_data="full_stats"),
            InlineKeyboardButton("📨 Feedback & Reply", callback_data="view_feedback")
        )
        return markup