# 📧 Gmail Automation Toolkit

A powerful, Python-based automation tool to manage your Gmail inbox efficiently. It filters important emails, organizes promotional content, generates daily summaries, and sends notifications directly to your **Telegram**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Gmail API](https://img.shields.io/badge/Google-Gmail%20API-red?style=for-the-badge&logo=gmail)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram)

---

## 🚀 Key Features

*   **🎯 Aggressive Job Hunt Mode**: Automatically detects **Interviews**, **Shortlisting**, and **Coding Tests** (HackerRank, LeetCode, etc.) and tags them in your notification.
*   **☁️ 24/7 Cloud Execution**: Runs on **GitHub Actions** for free, even when your computer is off.
*   **🔐 Secure Authentication**: Uses OAuth 2.0 to securely access your Gmail account.
*   **🧹 Inbox Decluttering**: Moves promotional emails to a specific "Promo_Processed" label.
*   **📱 Instant Notifications**: Sends a complete action report to your Telegram chat every morning at 8:00 AM.

---

## 🛠️ Getting Started (The "I'm Job Hunting" Edition)

### 1. Fork & Setup
1.  **Fork this repo** to your own GitHub account.
2.  Clone it locally to set up your credentials.
3.  Run `pip install -r requirements.txt`.

### 2. Generate Secrets
Run the helper script to generate your secure token:
```bash
python get_base64_token.py
```
*(Copy the long text it prints)*

### 3. Add Secrets to GitHub
Go to **Settings** -> **Secrets and variables** -> **Actions** and add:
*   `GMAIL_TOKEN_BASE64`: (The long text from step 2)
*   `TELEGRAM_BOT_TOKEN`: (Your bot token)
*   `TELEGRAM_CHAT_ID`: (Your chat ID)

**That's it!** The bot will now run daily and notify you of any interview updates.

### 4. Customizing Filters
Open `gmail_automator.py` and scroll to the `Job Hunt Mode` section to add specific keywords for your industry (e.g., "React Developer", "Data Scientist").

---

## 📜 Original Installation

*   **Python 3.8** or higher installed.
*   A **Google Cloud Project** with the Gmail API enabled.
*   A **Telegram Bot Token** (for notifications).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/adarsh02o/gmail-automation.git
    cd gmail-automation
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Google Credentials**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a project and enable the **Gmail API**.
    *   Create **OAuth 2.0 Client IDs** (Select "Desktop App").
    *   Download the JSON file, rename it to `credentials.json`, and place it in this folder.

4.  **Configure Environment Variables**
    *   Create a `.env` file in the root directory.
    *   Add your Telegram configuration:
        ```ini
        TELEGRAM_BOT_TOKEN=your_bot_token_here
        TELEGRAM_CHAT_ID=your_chat_id_here
        ```

---

## 🏃 Usage

### 1. Authenticate (First Time Only)
Run the setup script to log in to your Google Account. A browser window will open for you to authorize the app.
```bash
python generate_token.py
```

### 2. Run the Automation
Execute the main script to process your inbox and send the Telegram report.
```bash
python gmail_automator.py
```

---

## 📂 Project Structure

```bash
gmail-automation/
├── generate_token.py    # Setup script for Google OAuth login
├── gmail_automator.py   # Main script for filtering & Telegram reporting
├── gmail_helper.py      # Diagnostic script to test connection
├── requirements.txt     # List of Python dependencies
├── .env                 # (Hidden) Stores your API keys - DO NOT COMMIT
├── credentials.json     # (Hidden) Google OAuth credentials - DO NOT COMMIT
└── token.pickle         # (Hidden) Saved login session - DO NOT COMMIT
```

---

## � Further Improvements & Roadmap

The current version handles basic automation, but there is always room to grow! Here are some features you can consider adding:

1.  **💌 Auto-Reply Bot**: Automatically send replies to emails with specific subject lines (e.g., "Out of Office").
2.  **📎 Attachment Extraction**: Automatically find emails with attachments (like invoices) and save them to a local `Downloads` folder.
3.  **🧠 AI Integration**: Connect the script to an LLM (Large Language Model) to generate concise summaries of long email threads.
4.  **🗄️ Database Logging**: Save key email metadata to a SQLite database for local searching and analytics.
5.  **⏰ Configurable Scheduler**: Make the scheduling configuration easier via a config file instead of relying solely on `cron`.

---

## �📜 License

This project is licensed under the MIT License - feel free to use and modify it!

---
*Created by [adarsh02o](https://github.com/adarsh02o)*
