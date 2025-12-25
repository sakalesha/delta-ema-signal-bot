# Deploying to Render.com (Free Tier)

To run this bot for **FREE** on Render, we use a **Web Service** instead of a Background Worker. We have added a small web server (`Flask`) to the bot so it satisfies Render's requirements.

## Prerequisites
1. **GitHub Account**: Push your code to a repository.
2. **Render Account**: [render.com](https://render.com).
3. **UptimeRobot Account** (Free): [uptimerobot.com](https://uptimerobot.com) (Required to keep the bot awake).

## Step 1: Push Code to GitHub
Ensure you have pushed the latest changes (including `requirements.txt` and `main.py`) to your GitHub repository.

```bash
git add .
git commit -m "Add web server for Render Free Tier"
git push
```

## Step 2: Create Web Service on Render
1. Go to your Render Dashboard.
2. Click **New +** and select **Web Service**.
3. Connect your `delta-ema-signal-bot` repository.
4. Configure the service:
   - **Name**: `delta-ema-bot`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Select **Free**.
5. Click **Create Web Service**.

## Step 3: Configure Environment Variables
In the Render dashboard for your service, go to **Environment**:
1. Add `TELEGRAM_BOT_TOKEN`: Your new bot token.
2. Add `TELEGRAM_CHAT_ID`: Your chat ID.

## Step 4: Keep It Awake (Crucial)
Render's Free Tier spins down services after 15 minutes of inactivity. To prevent this:
1. Copy your Render Service URL (e.g., `https://delta-ema-bot.onrender.com`).
2. Go to **UptimeRobot**.
3. Click **Add New Monitor**.
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Delta Bot
   - **URL/IP**: Paste your Render URL.
   - **Monitoring Interval**: **5 minutes** (Important!).
4. Click **Create Monitor**.

**Done!** UptimeRobot will ping your bot every 5 minutes, keeping it active 24/7 for free.
