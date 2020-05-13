from typing import List


class TwitchTags:
    """Parses and objectifies Twitch Tags from messages"""

    def __init__(self, tags: List[dict]) -> None:
        rekeyed_dict = {
            tag['key']: tag['value']
            for tag in tags
        }
        self.user = rekeyed_dict['display-name']
        self.permission = rekeyed_dict['user-type']
