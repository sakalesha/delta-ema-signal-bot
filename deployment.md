# Deploying to Render.com

Since your bot runs continuously (`while True` loop), the appropriate Render service is a **Background Worker**.

## Prerequisites
1. **GitHub Account**: You need to push this code to a GitHub repository.
2. **Render Account**: Sign up at [render.com](https://render.com).

## Step 1: Push Code to GitHub
I have already initialized a local git repository for you. You now need to push it to a new GitHub repo.

1. Create a **New Repository** on GitHub (name it `delta-ema-signal-bot`).
2. Run the following commands in your terminal (replace `<YOUR_USERNAME>` with your GitHub username):

```bash
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/delta-ema-signal-bot.git
git push -u origin main
```

## Step 2: Create Background Worker on Render
1. Go to your Render Dashboard.
2. Click **New +** and select **Background Worker**.
3. Connect your GitHub account and select the `delta-ema-signal-bot` repository.
4. Configure the service:
   - **Name**: `delta-ema-bot`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Click **Create Background Worker**.

## Step 3: Configure Environment Variables (Crucial)
Your bot needs API keys to work. Do **NOT** commit them to code in a real production scenario, but for now they are hardcoded.
* Ideally, update `notifier.py` to use `os.getenv` again and set these in Render:
    - `BOT_TOKEN`
    - `CHAT_ID`

## Note on Costs
Background Workers on Render are part of paid plans (starting ~$7/month).
If you want a **Free Tier** option, you must use a **Web Service**, but Render freezes free web services that don't receive HTTP traffic or bind to a port.
To make this work on Free Tier:
1. We need to add a small HTTP server (like Flask) to `main.py` to satisfy Render's port requirement.
2. You would need to use a service like **UptimeRobot** to ping your bot url every 5 minutes to keep it awake.

**Currently, the code is ready for the standard (Paid) Background Worker.**
