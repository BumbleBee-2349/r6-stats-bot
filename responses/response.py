from services.tracker_request import request_data
import discord


def handle_response(message: str) -> str:
    
    args = message.split(" ")
    if len(args) < 2:
        return discord.Embed(title=f"Invalid command, please, insert <platform> <nickname>", color=0x7289DA)

    platform, nickname = args[0], args[1]

    return request_data(platform, nickname)
    