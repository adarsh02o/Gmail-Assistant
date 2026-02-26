# 🔒 Private Setup Guide

**IMPORTANT:** This file (`PRIVATE_GUIDE.md`) contains sensitive instructions. **Access to this file is for your eyes only.** It is added to `.gitignore`, so it will not be uploaded to GitHub.

---

## 📱 Part 1: Setting Up Telegram Notifications (Spoon-Fed Guide)

Follow these exact steps to get messages on your phone.

### Step 1: Create Your Bot
1.  Open the **Telegram app** on your phone or computer.
2.  In the search bar, type `@BotFather` and click on the verified account (blue checkmark).
3.  Tap **Start** (or type `/start`).
4.  Type this command: `/newbot`
5.  BotFather will ask for a **name**. Type something like: `My Gmail Assistant`
6.  BotFather will ask for a **username**. It **must end in `bot`**. Type something unique like: `AdarshGmailAuto_bot`
7.  **🎉 Success!** BotFather will give you a long string of API text. 
    *   **Look for section:** `Use this token to access the HTTP API:`
    *   **The Token looks like:** `123456789:ABCdefGhIJKlmNoPQRstUVwxyZ`
    *   **Copy this token.** This is your `TELEGRAM_BOT_TOKEN`.

### Step 2: Get Your Chat ID
1.  In Telegram search bar, search for `@userinfobot`.
2.  Click **Start**.
3.  It will immediately reply with your details.
4.  Look for the line that says `Id: 12345678`.
5.  **Copy this number.** This is your `TELEGRAM_CHAT_ID`.

### Step 3: Put it in the Code
1.  Open the file named `.env` in this folder.
2.  Paste your values like this (no spaces around the equal sign):
    ```ini
    TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstUVwxyZ
    TELEGRAM_CHAT_ID=12345678
    ```
3.  Save the file.

---

## ⏰ Part 2: Scheduling with Cron (Linux Automated Task)

We will tell your Linux system to run this script automatically every morning at 8:00 AM.

### Step 1: Prepare the Command
We need the **absolute path** to your folder and python. Based on your system, here are your paths:

*   **Folder:** `/home/zen/openclaw gmail `
*   **Python:** `/home/zen/openclaw gmail /.venv/bin/python`
*   **Script:** `gmail_automator.py`

### Step 2: Open the Cron Editor
1.  Open your terminal.
2.  Type this command and hit Enter:
    ```bash
    crontab -e
    ```
    > **⚠️ Error: "/usr/bin/vi: No such file or directory"?**
    > If you see this error, run this command instead:
    > ```bash
    > EDITOR=nano crontab -e
    > ```

3.  If it asks you to choose an editor, press `1` (for nano) and hit Enter.

### Step 3: Add the Schedule
1.  Use the arrow keys to go to the very bottom of the file.
2.  Paste this **exact line** on a new empty line:

    ```bash
    0 8 * * * cd "/home/zen/openclaw gmail " && "/home/zen/openclaw gmail /.venv/bin/python" gmail_automator.py >> cron.log 2>&1
    ```

    **What does this do?**
    *   `0 8 * * *`: Run at Minute:00, Hour:08 (8:00 AM).
    *   `cd ...`: Move to the folder first.
    *   `&&`: If moving folder works, then...
    *   `...python ...`: Run the script.
    *   `>> cron.log`: Save the text output to a log file so you can check errors.

### Step 4: Save and Exit
*   **If using Nano:** Press `Ctrl + O`, then `Enter` (to save), then `Ctrl + X` (to exit).
*   **If using Vi/Vim:** Press `Esc`, type `:wq`, then `Enter`.

### Step 5: Verify
Type this in the terminal:
```bash
crontab -l
```
You should see the line you just added. You are done! 🚀

---

## �️ Part 3: Customizing Your Bot (Advanced Filters)

We have added powerful filtering features to keep your inbox and Telegram notifications clean.

### 1. Trash Promotional Emails Automatically
We have added a keyword list in `gmail_automator.py`. Any email containing these keywords will be **labeled as "Promotion" AND moved to Trash immediately**.

To change these keywords, edit this list in `gmail_automator.py`:

```python
# Customizable Keywords for filtering promotional emails
PROMOTION_KEYWORDS = [
    "sale", 
    "discount", 
    "offer 50%", 
    "subscribe now", 
    "limited time",
    "new collection",
    "exclusive deal",
    "clearance",
    "free shipping",
]
```

### 2. Silence Annoying Senders in Telegram
Sometimes you want the email to be processed, but you **don't want a Telegram notification** for it. We added an "Ignore List" for senders.

Emails from these senders will **not** appear in your Telegram report:

```python
# Senders to ignore in Telegram report
PROMO_SENDERS = ["info@", "newsletter@", "offers@", "noreply@", "marketing@"]
```

You can add any email address or part of an address (like `@spammy-marketing.com`) to this list.

---

## 🛡️ Part 4: How to Safely Push to GitHub

You want to share your code without sharing your passwords.

### 1. Verify `.gitignore`
Make sure you have a file named `.gitignore` in your folder with these contents:
```text
credentials.json
token.pickle
.env
__pycache__/
.venv/
PRIVATE_GUIDE.md
cron.log
```
*Any file listed here will be INVISIBLE to Git.*

### 2. Initialize Git
Run these commands in your terminal one by one:

```bash
# 1. Start a new git repository
git init

# 2. Rename the branch to 'main'
git branch -M main

# 3. Add all files (The .gitignore will block the secret ones automatically)
git add .

# 4. Check status (Make sure .env and credentials.json are NOT listed)
git status

# 5. Commit the files
git commit -m "Initial commit of Gmail Automation Toolkit"

# 6. Link to your GitHub (Replace with your actual repo URL)
git remote add origin https://github.com/adarsh02o/gmail-automation.git

# 7. Push the code
git push -u origin main
```

**That's it! Your code is now live on GitHub, but your secrets are safe on your computer.**

---

## ☁️ Part 5: Running While Computer is Off (GitHub Actions)

**Question:** "Can we set it to run while the computer is off?"
**Answer:** Yes! But not on your local computer. We need to move the execution to the cloud (GitHub Actions).

### Step 1: Prepare Your Secrets
Since GitHub cannot access your local `token.pickle` or `.env` file, we need to upload them securely as "Secrets".

1.  **Generate the Base64 Token:**
    Run this command in your terminal:
    ```bash
    "/home/zen/openclaw gmail /.venv/bin/python" get_base64_token.py
    ```
    Copy the long string of characters it prints.

2.  **Go to GitHub:**
    *   Open your repository on GitHub.
    *   Go to **Settings** -> **Secrets and variables** -> **Actions**.
    *   Click **New repository secret**.

3.  **Add These 3 Secrets:**
    *   **Name:** `GMAIL_TOKEN_BASE64`
        *   **Value:** (Paste the long string from step 1)
    *   **Name:** `TELEGRAM_BOT_TOKEN`
        *   **Value:** (Your bot token from Part 1)
    *   **Name:** `TELEGRAM_CHAT_ID`
        *   **Value:** (Your chat ID from Part 1)

### Step 2: Push the Workflow
I have already created a workflow file for you at `.github/workflows/daily_run.yml`.
Just push your changes to GitHub:

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main
```

Now, GitHub will automatically run your script every day at **8:00 AM IST** (2:30 UTC), even if your computer is off!

---

## 🐳 Part 5: What about Docker?

**Question:** "What happens if I make a docker container here how it helps?"

**Answer:** Docker is like a "magic box" that contains everything your code needs to run (Python, libraries, etc.).

### Why use it?
1.  **Consistency:** Use Docker if you want to be 100% sure the code runs exactly the same on your computer, your friend's computer, or a server.
2.  **Easy Deployment:** If you later decide to rent a cheap server (VPS) instead of using GitHub Actions, you can just send this "box" (container) there and it will run immediately without installing Python or libraries manually.

**Do you need it for GitHub Actions?** No. GitHub Actions can install Python and run your script directly, which is simpler for this project. Docker is better if you have complex dependencies.

---

## 🚀 Part 6: Job Application & Interview Aggressive Mode

I have upgraded your script to **"Aggressive Job Hunt Mode"**. It now automatically scans for:
1.  **Interviews:** "schedule", "interview", "invitation", "next steps"
2.  **Shortlisting:** "shortlisted", "moving forward", "hiring team"
3.  **Assessments:** "test link", "hackerrank", "leetcode", "codility", "glider", "exam"

### How to Customize Keywords
If you want to add or remove keywords (e.g., if you are applying for a specific role like "Python Developer"):

1.  Open `gmail_automator.py`.
2.  Find the section **`# --- JOB HUNT MODE ---`** (around line 130).
3.  Edit the `job_queries` list:

```python
    job_queries = [
        'subject:(interview OR shortlisted OR "next steps")',
        '("talent acquisition" OR recruiter OR "hiring team")',
        # Add your own custom search here:
        'subject:("python developer" OR "backend engineer")'
    ]
```

---

## ⏳ Part 7: Modifying the Schedule (Local Cron)


You asked: *"how code filter important emails"*

The script uses Gmail's search operators to find emails. You can change this easily.

1.  Open `gmail_automator.py`.
2.  Find the `main()` function (around line 125).
3.  Look for this line:
    ```python
    keyword = "important"
    ```
4.  **Change it** to customize what emails are picked up.

### Examples of Filters:

*   **Emails from a specific person:**
    ```python
    keyword = "from:boss@company.com"
    ```

*   **Emails with a specific subject:**
    ```python
    keyword = "subject:invoice"
    ```

*   **Unread emails from a specific domain:**
    ```python
    keyword = "from:*@sammobile.com is:unread"
    ```

*   **Complex search (OR logic):**
    ```python
    keyword = "{subject:urgent subject:important}"
    ```
    *(Note: Curly braces `{}` mean OR in Gmail search queries)*

---

## ⏳ Part 6: Modifying the Schedule (Local Cron)


If you want to change how often the script runs (e.g., every 3 hours instead of once a day), follow these steps:

1.  Open the cron editor:
    ```bash
    crontab -e
    ```

2.  Find the line you added earlier. It looks like `0 8 * * * ...`

3.  Change the numbers at the beginning:
    *   **Every morning at 8 AM (Default):** `0 8 * * *`
    *   **Every 3 hours:** `0 */3 * * *`
    *   **Every hour:** `0 * * * *`
    *   **Every 30 minutes:** `*/30 * * * *`

4.  Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).

---

## 🔮 Further Improvements (Ideas for You)

Here are some cool features you can add to the code yourself:

1.  **Attachment Saver**: Modify the script to automatically download attachments (like PDFs or invoices) from emails with specific subjects and save them to a local folder.
2.  **Auto-Responder**: Add logic to send an automatic reply if an email contains keywords like "Urgent" but you are out of office.
3.  **Database Logging**: instead of just printing to the console, save email metadata (Sender, Subject, Date) into a SQLite database for long-term tracking.
4.  **AI Summary**: Use the OpenAI API to read the body of long emails and send a 1-sentence summary to your Telegram.

