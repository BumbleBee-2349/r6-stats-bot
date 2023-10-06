import discord
from utils.constants import CORN_FLOWER_BLUE_COLOR


def invalid_title_message() -> discord.Embed:
    return discord.Embed(title="Invalid command, please, insert show <platform> <nickname>",
                         color=CORN_FLOWER_BLUE_COLOR)


def full_profile_title_message(url: str) -> discord.Embed:
    return discord.Embed(title="Click to see full profile", url=url, color=CORN_FLOWER_BLUE_COLOR)


def failed_retrieving_stats_message(nickname_input: str) -> discord.Embed:
    return discord.Embed(title=f"Failed to retrieve the stats for nickname -> {nickname_input}",
                         color=CORN_FLOWER_BLUE_COLOR)


def failed_retrieving_stats_invalid_message(nickname_input: str) -> discord.Embed:
    return discord.Embed(title=f"Failed to retrieve the stats for nickname -> {nickname_input}, not enough data to"
                               f" retrieve, I'm really sorry 😢",
                         color=CORN_FLOWER_BLUE_COLOR)


def get_discord_intents():
    return discord.Intents.default()
