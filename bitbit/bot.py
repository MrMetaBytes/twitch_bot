import json
import logging
from typing import List

from irc.bot import ServerSpec, SingleServerIRCBot
from irc.client import Event, ServerConnection

from bitbit.commands import CommandManager
from bitbit.utils import TwitchTags

logger = logging.getLogger(__name__)


class TwitchBot(SingleServerIRCBot):
    def __init__(self, server_specs: List[ServerSpec], username: str, channels: List[str]) -> None:
        self.username = username
        self._channels = channels
        self._server_specs = server_specs

        self._command_manager = CommandManager("data/commands.json")
        super().__init__(self._server_specs, self.username, self.username)

    def on_welcome(self, c, e):
        """Event for server conneciton success"""
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')

        for channel in self._channels:
            logger.info(f'Joining {channel}')
            c.join(channel)
            c.privmsg(channel, 'Oh shit waddup, here come dat bot')

    def on_pubmsg(self, conn: ServerConnection, event: Event) -> None:
        """Event for message recieve"""
        channel = event.target
        message = event.arguments[0]
        print(message)

        if message[0] == '!':
            tags = TwitchTags(event.tags)
            self.handle_command(conn, channel, message, tags)

    def shutdown(self) -> None:
        self._command_manager.save()

    def handle_command(self, conn: ServerConnection, channel: str, message: str, tags: TwitchTags) -> None:
        """Command Handler for the chat bot"""
        try:
            command_name, *msg = message[1:].split()
            command_name = command_name.lower()
            msg = ' '.join(msg)

            if command_name == 'me':
                self._command_manager.store(
                    command_name=tags.user.lower(),
                    message=msg
                )
                conn.privmsg(channel, f'The command !{tags.user.lower()} has been updated!')
                return

            command = self._command_manager.get(command_name)
            if not command:
                return

            command.handle(tags.permission, msg)
            if command and command.response:
                conn.privmsg(channel, command.response)
        except Exception as e:
            print(f"Uh Oh: {e}")
