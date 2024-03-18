import os

from plemmy import LemmyHttp

from lemmypostbot import Config, LemmyPostBot

if __name__ == "__main__":
    lemmy = LemmyHttp(os.environ["instance"])
    lemmy.login(os.environ["username"], os.environ["password"])
    with open("config.yml", "r") as ymlfile:
        content = ymlfile.read()
    config = Config.from_yaml(content)

    lemmypostbot = LemmyPostBot.create(lemmy, config)
    