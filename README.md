# 🤖 BEU Syllabus Bot

<p align="center">
  <img src="logo.png" alt="BEU Syllabus Bot Logo" width="160">
</p>

<h1 align="center">BEU Syllabus Bot</h1>

<p align="center">
<b>Instant BEU B.Tech Syllabus on Telegram</b>
</p>

<p align="center">
<a href="https://t.me/beu_syllabuss_bot">
<img src="https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram">
</a>
<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Telegram%20API-Supported-success?style=for-the-badge">
<img src="https://img.shields.io/badge/Open%20Source-Yes-brightgreen?style=for-the-badge">
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

---

# 📖 About

**BEU Syllabus Bot** is a Telegram Bot developed for **Bihar Engineering University (BEU)** students.

It allows students to access the latest **Branch-wise** and **Semester-wise** syllabus PDFs instantly without searching multiple websites.

---

# ✨ Features

- 📚 Branch-wise Syllabus
- 🎓 Semester-wise Navigation
- 🗓️ Session-wise Syllabus (2018-2023, 2024-2028, 2026-2030)
- 📄 Official PDF Syllabus
- ⚡ Instant Response
- 📥 One Click Download
- 🤖 Telegram Based
- 📱 Mobile Friendly
- 🔄 Regular Updates
- 🎯 Easy to Use
- 💯 Free Forever

---

# 🎓 Supported Branches

- Computer Science Engineering (CSE)
- Information Technology (IT)
- Artificial Intelligence & Machine Learning (AIML)
- Artificial Intelligence & Data Science (AIDS)
- Civil Engineering (CE)
- Mechanical Engineering (ME)
- Electrical Engineering (EE)
- Electronics & Communication Engineering (ECE)
- Electrical & Electronics Engineering (EEE)

---

# 🗄️ Database (SQLite)

Stats and feedback are stored in `bot_data.db` (Python's built-in `sqlite3`, no extra install).
Override the location with the `DB_PATH` environment variable.

| Table | Purpose |
|---|---|
| `bot_stats` | total users, active today, total downloads |
| `popular_downloads` | download counter per (semester, session, branch) |
| `button_clicks` | usage counter per command / button |
| `users` | every user ID seen (unique + active counts, broadcast list) |
| `feedback` | feedback text stored with the sender's user ID and reply status |

An existing `analytics.json` is imported once (users + command counts) on first start.

**Admin:** `/admin` → *Feedback & Reply* lists recent feedback with user IDs. Reply with
`/reply <user_id> <message>` (admin only).

> ⚠️ On hosts with an ephemeral disk (e.g. Render free tier) `bot_data.db` is wiped on every
> redeploy — point `DB_PATH` at a persistent disk to keep your data.

---

# 🔀 Bot Flow

`Syllabus` → **Branch** → **Semester** (all 8 listed) → **Academic Session** → PDF

Links live in `data/syllabus.py` as `SYLLABUS[semester][session][branch]`. To add a PDF, fill in the matching entry (an empty string means "not available yet").

---

# 📚 Supported Semesters

- 1st Semester
- 2nd Semester
- 3rd Semester
- 4th Semester
- 5th Semester
- 6th Semester
- 7th Semester
- 8th Semester

---

# 🚀 Bot Link

### 👉 https://t.me/beu_syllabuss_bot

---

# 🛠 Built With

- Python
- python-telegram-bot
- Telegram Bot API
- Google Drive
- JSON Database

---

# 📂 Project Structure

```text
Beu-Syllabus-Bot
│
├── bot.py
├── handlers/
├── database/
├── utils/
├── requirements.txt
├── .env
├── logo.png
└── README.md
```

---

# 📦 Installation

Clone Repository

```bash
git clone https://github.com/mdzafar864/Beu-Syllabus-Bot.git
```

Go to Project

```bash
cd Beu-Syllabus-Bot
```

Install Requirements

```bash
pip install -r requirements.txt
```

Run Bot

```bash
python bot.py
```

---

# ⚙️ Environment Variables

Create a **.env** file

```env
BOT_TOKEN=YOUR_BOT_TOKEN
```

---

# 📸 Screenshots

```
screenshots/home.jpg
screenshots/branch.jpg
screenshots/semester.jpg
screenshots/pdf.jpg
```

---

# 🌟 Why Use This Bot?

- Free
- Fast
- Reliable
- Official Syllabus PDFs
- No Login Required
- Easy Navigation
- Mobile Friendly
- Instant Access

---

# 🚀 Future Roadmap

- 🔍 Search Syllabus
- ❤️ Favorites
- 🌙 Dark Mode
- 📢 Notifications
- 📊 Usage Analytics
- 📚 Notes Section
- 📝 PYQ Integration
- 🎥 Video Resources

---

# 🤝 Contributing

Contributions are always welcome!

1. Fork Repository

2. Create Branch

```bash
git checkout -b feature-name
```

3. Commit Changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Create Pull Request

---

# 👨‍💻 Developer

<p align="center">
<img src="Developer.png" width="170">
</p>

## Md Zafar

💻 Full Stack Developer

🎓 B.Tech Student

🏫 Bihar Engineering University

🌐 Portfolio

https://mdzafar864.github.io/Portfolio/

🐙 GitHub

https://github.com/mdzafar864

📧 Email

mdzafarsabour35@gmail.com

---

# ⭐ Support

If you like this project,

⭐ Star this Repository

🍴 Fork it

📢 Share it with Friends

❤️ Contribute to Improve It

---

# 📜 License

Licensed under the **MIT License**.

---

# 🙏 Acknowledgements

Special Thanks To

- Bihar Engineering University
- Telegram
- Python Community
- Open Source Contributors
- Every BEU Student

---

<p align="center">
⭐ If you find this project useful, please give it a Star.
</p>

<p align="center">
<a href="https://github.com/mdzafar864/Beu-Syllabus-Bot">⭐ Star Repository</a> •
<a href="https://t.me/beu_syllabuss_bot">🤖 Telegram Bot</a> •
<a href="https://github.com/mdzafar864">🐙 GitHub</a>
</p>

---

<p align="center">
© 2026 <strong>BEU Syllabus Bot</strong> · Developed by <strong>Md Zafar</strong>
</p>
