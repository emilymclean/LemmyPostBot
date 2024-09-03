import os

from pythonlemmy import LemmyHttp

from lemmypostbot import Config, LemmyPostBot

if __name__ == "__main__":
    lemmy = LemmyHttp(os.environ["LEMMY_INSTANCE"])
    lemmy.login(os.environ["LEMMY_USERNAME"], os.environ["LEMMY_PASSWORD"])
    with open("config.yml", "r") as ymlfile:
        content = ymlfile.read()
    config = Config.from_yaml(content)

    lemmypostbot = LemmyPostBot.create(lemmy, config)
    lemmypostbot.run()
