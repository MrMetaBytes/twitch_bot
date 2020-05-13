import json
from typing import Any, List, Optional, Union


PREFIX_BLACKLIST = [
    '!',
    '/',
]

PREFIX_WHITELIST = [
    '/me '
]


class Command:
    def __init__(self, name: str, message: Optional[str] = None, permission: Optional[str] = None) -> None:
        self.name = name
        self.permission = permission
        self._message = message
        self.response = self._message

    def __hash__(self) -> int:
        return hash(self.name)

    def handle(self, args: List[str], permission: Union[str, None]) -> None:
        if self.permission is not None and self.permission != permission:
            raise ValueError("Invalid permission for command")
        if args:
            self.response = self._message.format(args)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'message': self._message,
            'permission': self.permission,
        }


class CommandManager:
    def __init__(self, commands_path: str) -> None:
        self._commands_path = commands_path
        self._commands = {}
        self.load()

    def save(self) -> None:
        with open(self._commands_path, 'w+') as f:
            serialized_commands = [
                _command.to_dict()
                for _command in self._commands.values()
            ]
            f.write(json.dumps(serialized_commands, sort_keys=True, indent=4))

    def load(self) -> List[Command]:
        with open(self._commands_path) as f:
            commands_list = json.loads(f.read())

        for _command in commands_list:
            new_command = Command(**_command)
            self._commands[new_command.name] = new_command

    def get(self, command_name: str) -> Union[Command, None]:
        return self._commands.get(command_name)

    def store(self, command_name: str, message: str, permission: Optional[str] = None) -> None:
        white_listed = any(
            message.startswith(prefix)
            for prefix in PREFIX_WHITELIST
        )
        if not white_listed and any((
            message.startswith(prefix)
            for prefix in PREFIX_BLACKLIST
        )):
            raise ValueError("DAMNNN YOUUU BASIL!!!!")
        new_command = Command(command_name, str(message))
        self._commands[command_name] = new_command
