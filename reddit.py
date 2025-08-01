import os
from typing import TypedDict

import praw
from praw.models import Subreddit

reddit_instance: praw.Reddit | None = None
bot_names: list[str] = ["AutoModerator", "chessvision-ai-bot", "admin-tattler", "toolboxnotesxfer"]

class ModlogStatsUser(TypedDict):
    """
    Represents a user in the moderation log statistics.
    """
    name: str
    actions: dict[str, int] | None


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
    global bot_names
    log: list[praw.models.ModAction] = list(subreddit.log(limit=None, period='month'))
    
    log = [action for action in log if action.mod.name not in bot_names]
    return log

def get_moderators(subreddit: Subreddit.SubredditModeration) -> list[str]:
    """
    Retrieves a list of moderators for a given subreddit.
    
    :param subreddit: praw.models.Subreddit.SubredditModeration: The moderation object of the subreddit.
    :return: list[str]: A list of moderator usernames.
    """
    global bot_names
    return [mod.name for mod in subreddit.moderator() if mod.name not in bot_names]

def sort_actions(actions: list[praw.models.ModAction]) -> list[ModlogStatsUser]:
    """
    Sorts moderation actions by user and action type.
    
    :param actions: list[praw.models.ModAction]: A list of moderation actions.
    :return: list[ModlogStatsUser]: A list of ModlogStatsUser objects containing usernames and action counts.
    """
    #TODO: How do I get the action type?
    global bot_names
    user_actions: list[ModlogStatsUser] = []
    for action in actions:
        user = action.mod.name if action.mod is not None else None
        if user is None or user in bot_names:
            continue
        
        # Check if user already exists in the list
        
        
        
