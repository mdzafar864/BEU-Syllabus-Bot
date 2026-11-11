"""
Syllabus data.

Structure:  SYLLABUS[semester][session][branch] = google drive link

Ported from data.js. An empty string means the PDF has not been added yet;
the bot treats such combinations as "not available".
"""
from typing import List, Optional

SYLLABUS = {
    "1st": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/1iRWghHRyCP6WPZ3Xoc0DdScIytir3xRn/preview",
            "CSE": "https://drive.google.com/file/d/1EHpLPUo0_7086gFmk2WRZv2fMw93Jcdb/preview",
            "EE": "https://drive.google.com/file/d/1BtS61CEIOidszDe5FLBVQUake_8RQZlK/preview",
            "ECE": "https://drive.google.com/file/d/1t57gqcXtYajz6p5q6FXtcBVPb-mUgX1m/preview",
            "ME": "https://drive.google.com/file/d/1gyWaJKhhcZNmSF9WlWfqRXfnTeA87hvY/preview",
        },
        "2024-2028": {
            "CE": "https://drive.google.com/file/d/1Qd3X732fBWyEax1GTudkBWn7fpe57CgA/preview",
            "CSE": "https://drive.google.com/file/d/1Zp-UAEgj72UstczPS_wSIBtlPU48USal/preview",
            "IOT": "https://drive.google.com/file/d/1TldGBNBWl1hfn7faKNgBK12BjDjXV7hE/preview",
            "EE": "https://drive.google.com/file/d/1dZCtmM7w3H9dRpsWMlDhhJZNvFOiA1up/preview",
            "ECE": "https://drive.google.com/file/d/14cLD5aiYQp_2U3qKN16pa7U4fowBMg3J/preview",
            "ME": "https://drive.google.com/file/d/1mjC8PqyEFIc1_27QQxtAb3V1i3ota7y_/preview",
            "AI": "https://drive.google.com/file/d/10jbUuttq5qN0Tv7LTkk4dWCrZGgbUZ10/preview",
        },
        "2026-2030": {
            "CSE": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "AI": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "CS": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "DS": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "AIML": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "IOT": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "IOTCS": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "NET": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "IT": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "3DAG": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "MC": "https://drive.google.com/file/d/1v18YYmZ5bTUaYQgzIb_tEwlzVQjKLL11/preview",
            "EE": "https://drive.google.com/file/d/1LBQiy0HuJj6ZEEtx82uZXz5tUKRAe2Pp/preview",
            "EEE": "https://drive.google.com/file/d/1LBQiy0HuJj6ZEEtx82uZXz5tUKRAe2Pp/preview",
            "ECE": "https://drive.google.com/file/d/1LBQiy0HuJj6ZEEtx82uZXz5tUKRAe2Pp/preview",
            "ACT": "https://drive.google.com/file/d/1LBQiy0HuJj6ZEEtx82uZXz5tUKRAe2Pp/preview",
            "VLSI": "https://drive.google.com/file/d/1LBQiy0HuJj6ZEEtx82uZXz5tUKRAe2Pp/preview",
            "EIE": "https://drive.google.com/file/d/1LBQiy0HuJj6ZEEtx82uZXz5tUKRAe2Pp/preview",
            "ME": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "MSME": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "RA": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "CE": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "CECA": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "PE": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "CHLT": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "CHPP": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "WM": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "AE": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "BRE": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "MTE": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "MIN": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "CHE": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "FTS": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "FPP": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
            "FTM": "https://drive.google.com/file/d/1_i3PFbBhv4meQ_fjhIVbrr_RGxJpIUtX/preview",
        },
    },
    "2nd": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/1jW97lTtufHT26vkRP6KISUiKWSYe6F3o/preview",
            "CSE": "https://drive.google.com/file/d/16JynS8hA5JtsSlIc3-HBUPqI9o1F2ziN/preview",
            "EE": "https://drive.google.com/file/d/1CrAHd-0bwzESjiLtb-AQwOeKtopyiJm9/preview",
            "ECE": "https://drive.google.com/file/d/1eJQJy3I853QoqfNzOT5XFUgncJKxbnv6/preview",
            "ME": "https://drive.google.com/file/d/1xwhvlJIQJRCqKLCPTKeOOdjzkUgr8S5U/preview",
        },
        "2024-2028": {
            "CE": "https://drive.google.com/file/d/13q_AFXP9e2AWyHHtHWp_Fm4bRgtME3qv/preview",
            "CSE": "https://drive.google.com/file/d/15Y2Vsq8xe3Cl2Sc4BcXtL4XQMsqwKIFh/preview",
            "IOT": "https://drive.google.com/file/d/1iRpJ1SB_KyGgn84MqLZMutHnCHNTsYWk/preview",
            "EE": "https://drive.google.com/file/d/1wgmEj8RSBWleYUZ1JjzD7tICuiQgJEDW/preview",
            "ECE": "https://drive.google.com/file/d/1THqchJygHP7BVVQjj-kf4YmMHBrjfA_x/preview",
            "ME": "https://drive.google.com/file/d/1m_OdT4lGAZxSXuQUwwk_xvxHagzdrZR7/preview",
            "AI": "https://drive.google.com/file/d/10jbUuttq5qN0Tv7LTkk4dWCrZGgbUZ10/preview",
        },
    },
    "3rd": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/1IS4EV9JvOfoLW3cYRW7U-qBkXyRAvFlD/preview",
            "CSE": "https://drive.google.com/file/d/1ZlU22NFGirTuV01jKYiG9zdSU_IO29-t/preview",
            "EE": "https://drive.google.com/file/d/1D2gAZlW299s9f60wcdicGSZK7DpZVXkc/preview",
            "ECE": "https://drive.google.com/file/d/1auOpeh5UX4E23rnxIQo1K9TdFrqSXrm0/preview",
            "ME": "https://drive.google.com/file/d/1XE_l1tfHGZHMDIxU6KNlcjlqiKxKN-ZW/preview",
        },
        "2024-2028": {
            "CE": "https://drive.google.com/file/d/1GzMwwCkUrHPmc5fgyWOxOSsPof9dQZO8/preview",
            "CSE": "https://drive.google.com/file/d/18tjQnI2qGtbSzRWEp08KqKY4gDvE25em/preview",
            "IOT": "https://drive.google.com/file/d/1DyoqlnntdtG-RA0ET1wH4FrR-DOB3mtF/preview",
            "EE": "https://drive.google.com/file/d/1nKpL1rXXa7EGJqbvDkmEem1uh74QWjOU/preview",
            "ECE": "https://drive.google.com/file/d/1kWy1_zhggLM9U4jrkTzGWNdLcE-4QXMr/preview",
            "ME": "https://drive.google.com/file/d/1UFZLtpjIdwiyE9b6BNWfvStfHQztmr1a/preview",
            "AI": "https://drive.google.com/file/d/1psBOKvD7xHSEOkzAjiFmJ8giSeJu6hxM/preview",
        },
    },
    "4th": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/17w5zTFNaWUOg7S_vUrqW_AxtMyf7bPdU/preview",
            "CSE": "https://drive.google.com/file/d/1ODCj6Omx6dUuHR-Cmwh4iu37TaMQyTLn/preview",
            "EE": "https://drive.google.com/file/d/1G-cJOckwjZRoaDz0Nnw-CphpqBcZztA7/preview",
            "ECE": "https://drive.google.com/file/d/1nkfp0xRno6_ybJSWqZ6_ryiwI4aNsjXh/preview",
            "ME": "https://drive.google.com/file/d/1LoOVU0xZ9kkANCFNMmZbsWhgquoDbPgW/preview",
        },
        "2024-2028": {
            "CE": "",
            "CSE": "",
            "EE": "https://drive.google.com/file/d/1BCJ8zrbXmVMS69iAWu7wncgcpxWsqZHy/preview",
            "ECE": "",
            "ME": "",
        },
    },
    "5th": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/1tGXDItZ5g-AsnsXN0KmMifbA36vgxA0C/preview",
            "CSE": "https://drive.google.com/file/d/1SZdAT8a1vrIfrMPYjl0Q-0cc3hBba3z3/preview",
            "EE": "https://drive.google.com/file/d/1MA_tDBF7Fuvg8OGgn8bzg4mHSUTmQ-dC/preview",
            "ECE": "https://drive.google.com/file/d/1dJV_E7tPdhmmA7IutIDeaDMz3rxYb9XR/preview",
            "ME": "https://drive.google.com/file/d/1FW1-YDLvthfdG52szzsLzTIU9DOI03bc/preview",
        },
        "2024-2028": {
            "CE": "https://drive.google.com/file/d/1zplxNkclO9vL0hqaR_VoeD2gpMrzzFHi/preview",
            "CSE": "https://drive.google.com/file/d/1SZdAT8a1vrIfrMPYjl0Q-0cc3hBba3z3/preview",
            "EE": "https://drive.google.com/file/d/1MA_tDBF7Fuvg8OGgn8bzg4mHSUTmQ-dC/preview",
            "ECE": "https://drive.google.com/file/d/1MHmOfqd7MgTA6qw2qCFLUkBpau_iXk90/preview",
            "ME": "https://drive.google.com/file/d/1aBKZP3P9Ttni0RPa-HWK6yi1vND1_KlL/preview",
        },
    },
    "6th": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/1MxzSoTSdMgCvgCPiDFsDjVuu4QaJCQge/preview",
            "CSE": "https://drive.google.com/file/d/1ckXxGY5kdHmxlAIGsq-NfDskA4Mj_xQj/preview",
            "EE": "https://drive.google.com/file/d/1obhgEQmyRzDg1XPG7Gc6u5SyMugXN9bn/preview",
            "ECE": "https://drive.google.com/file/d/1reUmWqura-4UnEx7tpjv6wANADxvW_lc/preview",
            "ME": "https://drive.google.com/file/d/19UDBkvdYqgMqRzV_Fgre8vq8utOapy2q/preview",
        },
        "2024-2028": {
            "CE": "https://drive.google.com/file/d/1MxzSoTSdMgCvgCPiDFsDjVuu4QaJCQge/preview",
            "CSE": "https://drive.google.com/file/d/1ckXxGY5kdHmxlAIGsq-NfDskA4Mj_xQj/preview",
            "EE": "https://drive.google.com/file/d/1obhgEQmyRzDg1XPG7Gc6u5SyMugXN9bn/preview",
            "ECE": "https://drive.google.com/file/d/1reUmWqura-4UnEx7tpjv6wANADxvW_lc/preview",
            "ME": "https://drive.google.com/file/d/1QCpGOtY_LtwM8ZAnwQLStXTYc6q53tCc/preview",
        },
    },
    "7th": {
        "2018-2023": {
            "CE": "https://drive.google.com/file/d/1Qy64E3CCdfhQvD8PaihwPDFVz2FwDqGr/preview",
            "CSE": "https://drive.google.com/file/d/1uW4HVIaLErhWIyj36Lday4JMH1ZfuLEp/preview",
            "EE": "https://drive.google.com/file/d/1ey1jhsveL-eO0gc0FgwlNs7U05qRQHp5/preview",
            "ECE": "https://drive.google.com/file/d/1aDSSzOz8kWsmO0oJV7Z5CZ2lnCXReEqq/preview",
            "ME": "https://drive.google.com/file/d/1kMv43ZFJMctH_iRYbI230GCNN4UkZYud/preview",
        },
        "2024-2028": {
            "CE": "https://drive.google.com/file/d/1Qy64E3CCdfhQvD8PaihwPDFVz2FwDqGr/preview",
            "CSE": "https://drive.google.com/file/d/1uW4HVIaLErhWIyj36Lday4JMH1ZfuLEp/preview",
            "EE": "https://drive.google.com/file/d/1ey1jhsveL-eO0gc0FgwlNs7U05qRQHp5/preview",
            "ECE": "https://drive.google.com/file/d/1aDSSzOz8kWsmO0oJV7Z5CZ2lnCXReEqq/preview",
            "ME": "https://drive.google.com/file/d/11YjrIW6xbq2fP4RMOIDfYjs6IWj5egYN/preview",
        },
    },
    "8th": {
        "2018-2023": {
            "EE": "https://drive.google.com/file/d/1BwL_f3KCmWzuEulEth3G3hQw5sxLvBOy/preview",
            "ME": "https://drive.google.com/file/d/1PPkfTohITDMkIFNuw836gSOSUjCFtt3n/preview",
            "CE": "https://drive.google.com/file/d/1DV6rPVbPYfuPehfUlg6sKlaw-VkcwEuq/preview",
        },
        "2024-2028": {
            "EE": "https://drive.google.com/file/d/1BwL_f3KCmWzuEulEth3G3hQw5sxLvBOy/preview",
            "ME": "https://drive.google.com/file/d/17kkis9xvs3GVZP9ZODKwTrwhC0c8ES56/preview",
            "CE": "https://drive.google.com/file/d/1DV6rPVbPYfuPehfUlg6sKlaw-VkcwEuq/preview",
        },
    },
}

# Which sessions are selectable for each semester (display order).
SESSIONS_BY_SEMESTER = {
    "1st": ["2018-2023", "2024-2028", "2026-2030"],
    "2nd": ["2018-2023", "2024-2028"],
    "3rd": ["2018-2023", "2024-2028"],
    "4th": ["2018-2023", "2024-2028"],
    "5th": ["2018-2023", "2024-2028"],
    "6th": ["2018-2023", "2024-2028"],
    "7th": ["2018-2023", "2024-2028"],
    "8th": ["2018-2023", "2024-2028"],
}

# All semesters, in display order.
SEMESTERS = list(SYLLABUS.keys())

SEMESTER_NAMES = {
    "1st": "1st Semester",
    "2nd": "2nd Semester",
    "3rd": "3rd Semester",
    "4th": "4th Semester",
    "5th": "5th Semester",
    "6th": "6th Semester",
    "7th": "7th Semester",
    "8th": "8th Semester",
}


def get_syllabus_link(semester: str, session: str, branch: str) -> Optional[str]:
    """Return the Drive link for (semester, session, branch), or None if missing."""
    link = SYLLABUS.get(semester, {}).get(session, {}).get(branch, "")
    link = (link or "").strip()
    return link or None


def get_sessions_for(semester: str, branch: str) -> List[str]:
    """Sessions of `semester` that actually have a syllabus PDF for `branch`."""
    return [
        s for s in SESSIONS_BY_SEMESTER.get(semester, [])
        if get_syllabus_link(semester, s, branch)
    ]
