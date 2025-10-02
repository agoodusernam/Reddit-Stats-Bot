from discord.ext import commands

import reddit

class Stats(commands.Cog, name='Stats'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='mlstats',
                      aliases=['stats', 'mlstats'],
                      help='Show stats for the modlog for the subreddit')
    async def modlog_stats(self, ctx: commands.Context):
        """Show stats for the modlog for the subreddit"""
        stats = reddit.count_actions(reddit.get_modlog_last_month(reddit.get_subreddit("chess")))
        msg = f"**Modlog stats for r/chess (last 30 days)**\n"
        for user, count in stats.items():
            msg += f"• **{user}**: {count}\n"
            
        await ctx.send(msg)
        
        
