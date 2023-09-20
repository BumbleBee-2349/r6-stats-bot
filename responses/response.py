from services.tracker_request import request_data
from core.embed import invalid_title_message


def handle_response(message: str):
    args = message.split(" ")
    if len(args) < 2 or args[0] != "show":
        return invalid_title_message()

    platform, nickname = args[1], args[2]

    return request_data(platform, nickname)
