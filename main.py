from lemmypostbot import Config

if __name__ == "__main__":
    with open("config.yml", "r") as ymlfile:
        content = ymlfile.read()
    print(Config.from_yaml(content))