# Gmail Automation Toolkit

A Python automation tool to manage a Gmail inbox. It filters important emails, organizes promotions, creates daily summaries, and sends a Telegram report.

## Features

- Job hunt mode: highlights interview, shortlist, and test emails.
- Automated labeling and cleanup of promotional emails.
- Daily unread summary for the last 24 hours.
- Telegram notifications for quick review.
- Optional GitHub Actions scheduler.

## Requirements

- Python 3.8+
- A Google Cloud project with Gmail API enabled
- A Telegram bot (for notifications)

## API Setup

### 1) Google Gmail API (OAuth 2.0)

1. Open Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing one.
3. Enable the Gmail API: APIs & Services -> Library -> Gmail API -> Enable.
4. Configure OAuth consent screen (External is fine for personal use).
5. Create OAuth credentials:
   - APIs & Services -> Credentials -> Create Credentials -> OAuth client ID
   - Application type: Desktop app
6. Download the JSON file and save it as `credentials.json` in the project root.

### 2) Telegram Bot API

1. Open Telegram and chat with @BotFather.
2. Create a new bot and copy the bot token.
3. Get your chat ID (use @userinfobot or any chat ID finder bot).
4. Add these to a local `.env` file in the project root:

```ini
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Local Setup

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## First-Time Authentication

Run the token generator to complete OAuth login and create `token.pickle`:

```bash
python generate_token.py
```

## Run the Automation

```bash
python gmail_automator.py
```

## GitHub Actions (Optional)

The workflow file is at `.github/workflows/daily_run.yml`. To run in GitHub Actions:

1. Generate base64 token for secrets:

```bash
python get_base64_token.py
```

2. Add these GitHub Actions secrets:

- `GMAIL_TOKEN_BASE64`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## Configuration Notes

- Update keywords and filters in `gmail_automator.py`:
  - `PROMOTION_KEYWORDS` for promotional detection
  - `PROMO_SENDERS` to exclude noisy senders from reports
  - Job hunt queries for role-specific terms

## Project Structure

```bash
gmail-automation/
├── .env                      # Local env vars for Telegram and runtime config
├── .git/                     # Git metadata (local repo state)
├── .github/
│   └── workflows/
│       └── daily_run.yml     # GitHub Actions schedule/runner config
├── .gitignore                # Files and folders excluded from git
├── .venv/                    # Local Python virtual environment
├── __pycache__/              # Python bytecode cache (auto-generated)
├── credentials.json          # Google OAuth client secrets (DO NOT COMMIT)
├── cron.log                  # Cron run logs (local)
├── cron_debug.log            # Cron debug logs (local)
├── generate_token.py         # Interactive OAuth login to create token.pickle
├── get_base64_token.py       # Encodes token.pickle for GitHub Secrets
├── gmail_automator.py        # Main automation: filter, label, notify
├── gmail_helper.py           # Helper utilities for Gmail API and diagnostics
├── PRIVATE_GUIDE.md          # Private setup notes (local)
├── README.md                 # Project usage and setup guide
├── requirements.txt          # Python dependencies list
├── run_gmail.sh              # Shell wrapper to run the automation
└── token.pickle              # Cached OAuth token (DO NOT COMMIT)
```

## Security Notes

- Never commit `.env`, `credentials.json`, or `token.pickle`.
- Use GitHub Actions secrets for CI runs.
