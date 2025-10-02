import asyncio
import datetime
import os
import logging

import discord
import discord.ext.commands
import discord.ext
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)

logging.basicConfig(level=logging.INFO)
t_now = datetime.datetime.now()
year = t_now.year
month = t_now.month + 1 if t_now.day > 1 or (t_now.day == 1 and t_now.time() > datetime.time(0, 0)) else t_now.month
schedule_time = datetime.datetime(year, month, 1, 0, 0, 0, 0)

@discord.ext.tasks.loop(seconds=59)
async def every_first_of_month():
    """
    Kinda scuffed function to run every 1st of the month at midnight.
    :return:
    """
    # Set initial schedule_time to the next 1st of the month at midnight
    global schedule_time

    
    await bot.wait_until_ready()
    
    now = datetime.datetime.now()
    if schedule_time <= now:
        # func
        # Schedule for the next 1st of the month
        next_month = schedule_time.month + 1
        next_year = schedule_time.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        schedule_time = datetime.datetime(next_year, next_month, 1, 0, 0, 0, 0)


async def load_extensions() -> bool:
    """
    Load all cogs from the 'cogs' directory.
    :return: True if successful, False if an error occurs.
    """
    try:
        success = True
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded {filename[:-3]}')
                
                except discord.ext.commands.ExtensionNotFound:
                    logging.error(f'Extension {filename[:-3]} not found.')
                    print(f'Extension {filename[:-3]} not found, skipping.')
                    success = False
                
                except discord.ext.commands.ExtensionAlreadyLoaded:
                    logging.warning(f'Extension {filename[:-3]} is already loaded.')
                    print(f'Extension {filename[:-3]} is already loaded, skipping.')
                    success = False
                
                except discord.ext.commands.NoEntryPointError:
                    logging.error(f'No entry point found in {filename[:-3]}.')
                    print(f'No entry point found in {filename[:-3]}, skipping.')
                    success = False
                
                except discord.ext.commands.ExtensionFailed:
                    logging.error(f'Failed to load extension {filename[:-3]}, there was an execution error in the cog.')
                    print(f'Failed to load extension {filename[:-3]}, skipping.')
                    success = False
        
        return success
    
    except PermissionError:
        print('Permission denied while trying to load extensions. Please check your file permissions.')
        return False
    
    except NotImplementedError:
        print('Cogs path is not a directory. Please check your cogs directory structure.')
        return False
    
    except Exception as e:
        print(f'An unexpected error occurred while loading extensions: {e}')
        return False


@bot.event
async def on_ready() -> None:
    """
    Event handler for when the bot is ready.
    :return: None
    """
    if not await load_extensions():
        print('Failed to load some extensions. Please check the logs for details.')
    
    print(f"Loaded {len(bot.cogs)} cogs:")
    for cog in bot.cogs:
        print(f" - {cog}")
    
    print(f"Total commands: {len(bot.commands)}")
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


async def main() -> None:
    bot.run(os.getenv('DISCORD_TOKEN'), reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())
