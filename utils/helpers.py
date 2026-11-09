import logging
import re
from datetime import datetime
from io import BytesIO

import requests

from data.constants import BRANCH_EMOJIS
from data.syllabus import SEMESTERS, SEMESTER_NAMES

logger = logging.getLogger(__name__)


def get_file_id(drive_url: str) -> str:
    """Extract the Google Drive file id from any common drive URL format"""
    if "id=" in drive_url:
        return drive_url.split("id=")[-1].split("&")[0]
    elif "/d/" in drive_url:
        return drive_url.split("/d/")[1].split("/")[0]
    return drive_url


def get_download_link(drive_url: str) -> str:
    """Build a plain (browser-facing) download link from a Google Drive URL.
    Used only for the inline 'Download PDF' button, NOT for sending the file."""
    try:
        file_id = get_file_id(drive_url)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    except Exception:
        return drive_url


def download_drive_file(drive_url: str, chunk_size: int = 32768):
    """
    Actually download a Google Drive file's bytes, handling the
    'Google Drive can't scan this file for viruses' confirmation page
    that appears for larger files. Telegram's send_document CANNOT
    fetch drive.google.com/uc?export=download URLs directly for such
    files (it gets an HTML page instead of the PDF), so we must fetch
    the bytes ourselves and upload them to Telegram.

    Returns a BytesIO object on success, or None on failure.
    """
    file_id = get_file_id(drive_url)
    base_url = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    try:
        response = session.get(base_url, params={"id": file_id}, stream=True, timeout=30)

        # Look for the confirm token Google issues for large/scan-warned files
        token = None
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                token = value
                break

        if token is None:
            # Newer Drive pages embed the confirm token in the HTML body
            match = re.search(r'confirm=([0-9A-Za-z_-]+)', response.text[:200000] if response.text else "")
            if match:
                token = match.group(1)

        if token:
            response = session.get(
                base_url,
                params={"id": file_id, "confirm": token},
                stream=True,
                timeout=30,
            )

        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            logger.error(f"Drive returned HTML instead of a file for id={file_id} (link may not be public)")
            return None

        buffer = BytesIO()
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                buffer.write(chunk)
        buffer.seek(0)

        if buffer.getbuffer().nbytes == 0:
            logger.error(f"Downloaded 0 bytes for drive file id={file_id}")
            return None

        return buffer
    except Exception as e:
        logger.error(f"Failed to download drive file id={file_id}: {e}")
        return None
    finally:
        session.close()

def format_branch_text() -> str:
    """Format branch selection text"""
    text = "🏗️ *पहले अपनी Branch चुनें:*\n\n"
    for branch, emoji_name in BRANCH_EMOJIS.items():
        text += f"• {emoji_name}\n"
    text += "\n💡 *Branch चुनने के बाद Semester और Session select करेंगे*"
    return text

def format_semester_text(branch: str) -> str:
    """Format semester selection text (lists ALL semesters)"""
    branch_name = BRANCH_EMOJIS.get(branch, branch)
    text = f"📚 *{branch_name} Branch*\n\n"
    text += "अब अपना *Semester* चुनें:\n\n"
    for i, sem in enumerate(SEMESTERS, 1):
        text += f"{i}. {SEMESTER_NAMES.get(sem, sem)}\n"
    text += "\n💡 *Semester चुनने के बाद Session select करेंगे*"
    return text

def format_session_text(branch: str, semester: str, sessions: list) -> str:
    """Format academic session selection text"""
    branch_name = BRANCH_EMOJIS.get(branch, branch)
    sem_name = SEMESTER_NAMES.get(semester, semester)
    text = f"📚 *{branch_name} - {sem_name}*\n\n"
    text += "अब अपना *Academic Session* चुनें:\n\n"
    for i, sess in enumerate(sessions, 1):
        text += f"{i}. {sess}\n"
    return text

def format_time(timestamp) -> str:
    """Format datetime for display"""
    return timestamp.strftime('%d %b %Y, %I:%M %p')

def get_command_stats_text(command_stats: dict) -> str:
    """Format command statistics"""
    text = "📈 *Command Usage:*\n"
    for cmd, count in sorted(command_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
        text += f"• /{cmd}: {count}\n"
    return text