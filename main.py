import sys

import config

from bitbit.bot import TwitchBot


if __name__ == "__main__":
    bot = TwitchBot([config.DEFAULT_SERVER_SPEC], 'bitbitbot', ['#mrmetabytes'])
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.shutdown()
        sys.exit()
