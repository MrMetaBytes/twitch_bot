from irc.bot import ServerSpec

with open('.oauth_token') as f:
    token = f.readline()


DEFAULT_SERVER_SPEC = ServerSpec(
    host='irc.chat.twitch.tv',
    password=token
)
