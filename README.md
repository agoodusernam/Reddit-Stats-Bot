# Subreddit Stats Bot
A discord bot that sends statistics about a specific subreddit and the moderators of that subreddit.

# Installation
1. Clone the repository:
   ```bash
   git clone <>
   ```
2. Navigate to the project directory:
    ```bash
      cd RedditStatBot
    ```
3. Install the required dependencies:
    ```bash
   pip install -r requirements.txt
    ```
4. Go into the .env file and set the following variables:
    - `DISCORD_TOKEN`: Your Discord bot token.
    - `SUBREDDIT`: The subreddit you want to get statistics for. (e.g., `r/python`).
    - `REDDIT_CLIENT_ID`: Your Reddit app client ID.
    - `REDDIT_CLIENT_SECRET`: Your Reddit app client secret.
    - `REDDIT_USER_AGENT`: A user agent string for your Reddit app.
    - `REDDIT_USERNAME`: The username for the reddit account.
    - `REDDIT_PASSWORD`: The password for the reddit account.


5. Run the bot:
   ```bash
   python main.py
    ```
   