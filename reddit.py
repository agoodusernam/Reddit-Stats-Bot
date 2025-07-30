import os

import praw
from praw.models import Subreddit

reddit_instance: praw.Reddit | None = None


def get_reddit_instance() -> praw.Reddit:
    """
    Creates and returns a Reddit instance using credentials from environment variables.
    
    :return: praw.Reddit: An authenticated Reddit instance.
    """
    global reddit_instance
    if reddit_instance is not None:
        return reddit_instance
    reddit_instance = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD')
    )
    return reddit_instance


def get_subreddit(subreddit_name: str) -> Subreddit.SubredditModeration:
    """
    Returns a subreddit object for the given subreddit name.
    
    :param subreddit_name: str: The name of the subreddit to retrieve.
    :return: praw.models.Subreddit.SubredditModeration: The subreddit object.
    """
    reddit = get_reddit_instance()
    return reddit.subreddit(subreddit_name).mod

def get_modlog_last_month(subreddit: Subreddit.SubredditModeration) -> list[praw.models.ModAction]:
    """
    Retrieves the moderation log for the last month for a given subreddit.
    
    :param subreddit: praw.models.Subreddit.SubredditModeration: The moderation object of the subreddit.
    :return: list[praw.models.ModAction]: A list of moderation actions from the last month.
    """
    log: list[praw.models.ModAction] = list(subreddit.log(limit=None, period='month'))
    bot_names: list[str] = ["AutoModerator", "chessvision-ai-bot", "admin-tattler", "toolboxnotesxfer"]
    log = [action for action in log if action.mod.name not in bot_names]
    return log
