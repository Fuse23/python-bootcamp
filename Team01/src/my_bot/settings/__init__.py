"""
The file contains the initialization of the bot and the user data warehouse.

Variables:
    BOT_TOKEN (str): Your bot's token to connect to the Telegram API.
    dp (Dispatcher): Dispatcher object for processing bot messages and commands.
    user_info (userInfo): An object for storing user information.
    hero_name (HeroName): An object for managing the names of heroes in the game.
    user_progress (User Progress): An object for tracking user progress.
    bot: A bot object for interacting with the Telegram API.
    users_data (dict): The user's local data storage, where the key is the
        telegram id, the value is the controller.
    users_in_game (dict): A local repository of information about the presence
        of users in the game, where the key is telegram id.
    users_story_id (dict): Local storage for identifying the current user history,
        where the key is telegram id.
"""
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from database import (
    UserInfo,
    HeroName,
    UserProgress,
)


BOT_TOKEN = "BOT_TOKEN"


dp = Dispatcher()
user_info = UserInfo()
hero_name = HeroName()
user_progress = UserProgress()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

users_data = {}
users_in_game = {}
users_story_id = {}
