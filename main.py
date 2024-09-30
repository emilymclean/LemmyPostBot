import os

from pythonlemmy import LemmyHttp

from lemmypostbot import Config, LemmyPostBot

if __name__ == "__main__":
    lemmy = LemmyHttp(os.environ["LEMMY_INSTANCE"])

    if "LEMMY_USERNAME" in os.environ and "LEMMY_PASSWORD" in os.environ:
        lemmy.login(os.environ["LEMMY_USERNAME"], os.environ["LEMMY_PASSWORD"])
    elif "LEMMY_JWT" in os.environ:
        lemmy.set_jwt(os.environ["LEMMY_JWT"])
    else:
        raise Exception("Please provide either LEMMY_USERNAME and LEMMY_PASSWORD, or LEMMY_JWT")


    with open("config.yml", "r") as ymlfile:
        content = ymlfile.read()
    config = Config.from_yaml(content)

    lemmypostbot = LemmyPostBot.create(lemmy, config)
    lemmypostbot.run()
