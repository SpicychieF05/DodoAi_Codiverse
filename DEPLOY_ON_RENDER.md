# Deploying Codiverse Bot on Render

## Prerequisites

- A GitHub account with this repository pushed.
- A [Render](https://render.com) account.

## Step 1: Push Changes to GitHub

Make sure all the latest changes (including `render.yaml`, `Procfile`, and updated `agent.py`) are pushed to your GitHub repository.

## Step 2: Create a New Blueprint on Render

1. Log in to your Render Dashboard.
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect the `render.yaml` file.

## Step 3: Configure Environment Variables

Render will ask you to provide values for the environment variables defined in `render.yaml`.
Fill in the following:

- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token.
- `OPENAI_API_KEY`: Your OpenAI Key (if used).
- `GROQ_API_KEY`: Your Groq Key.
- `GOOGLE_API_KEY`: Your Gemini Key.
- `DEEPSEEK_API_KEY`: Your DeepSeek Key.
- `RAPIDAPI_KEY`: Your RapidAPI Key.
- `WEBHOOK_URL`: **Leave this empty for now.**

## Step 4: First Deployment

1. Click **Apply**.
2. Render will start building and deploying your bot.
3. **Important**: The first deployment might fail or be marked as "Unhealthy" because the bot will try to poll (since `WEBHOOK_URL` is empty) but Render expects a web server listening on a port.
   - _Don't worry about this yet._

## Step 5: Get Your Service URL

1. Once the service is created (even if it says "Deploy Failed" or "In Progress"), look for the **Service URL** at the top of the dashboard (e.g., `https://codiverse-bot.onrender.com`).
2. Copy this URL.

## Step 6: Set Webhook URL

1. Go to the **Environment** tab of your service.
2. Edit the `WEBHOOK_URL` variable.
3. Paste the URL you copied (e.g., `https://codiverse-bot.onrender.com`).
4. Click **Save Changes**.

## Step 7: Automatic Redeploy

Saving the environment variable will trigger a new deployment.

- Now, `agent.py` will see the `WEBHOOK_URL`.
- It will start a webhook server on port `8443` (or whatever Render assigns).
- The deployment should now succeed and be marked **Healthy**.

## Troubleshooting

- **Logs**: Check the "Logs" tab to see if the bot is starting correctly.
- **Port Binding**: Ensure the logs say "Starting webhook on port...".
- **Database**: Note that `api_stats.db` (SQLite) will be reset on every deployment because Render's filesystem is ephemeral. If you need persistent stats, consider using Render's PostgreSQL.
