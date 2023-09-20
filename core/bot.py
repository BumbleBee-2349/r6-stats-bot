import os
from core.embed import get_discord_intents, invalid_title_message
from dotenv import load_dotenv
from responses.response import handle_response
from discord.ext import commands


load_dotenv()
intents = get_discord_intents()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        await message.author.send(embed=response) if is_private else await message.channel.send(embed=response)
    except Exception as error:
        print(error)


def run():
    TOKEN = os.getenv('DISCORD_TOKEN')

    @bot.event
    async def on_ready():
        print(f'{bot.user} is running!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if "stats" not in channel:
            return

        await send_message(message, user_message, is_private=False)
    
    bot.run(TOKEN)
