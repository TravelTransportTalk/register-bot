from typing import List

from telegram import BotCommand
from telegram._update import Update
from telegram.ext import (
    Application,
    PreCheckoutQueryHandler
)

from src.behavior.default_handler import default_builder
from src.data_init import TOKEN


import asyncio

def bot_start() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # simple start function
    application.add_handler(default_builder())

    # lower case for some f*ckin reason, Telegram!
    __init_commands(
        application,
        [
            BotCommand("start", "login user"),
            BotCommand("cancel", "go to main menu")
        ]
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def __init_commands(application, commands: List[BotCommand]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(application.bot.set_my_commands(commands))