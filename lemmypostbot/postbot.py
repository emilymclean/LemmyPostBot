from typing import List

from plemmy import LemmyHttp

from . import RepeatedPostHandler
from .configuration import Config
from .handler import Handler


class LemmyPostBot:
    http: LemmyHttp
    config: Config
    handlers: List[Handler]

    def __init__(self, http: LemmyHttp, config: Config, handlers: List[Handler]):
        self.http = http
        self.config = config
        self.handlers = handlers

    @staticmethod
    def create(
            http: LemmyHttp,
            config: Config
    ):
        return LemmyPostBot(
            http,
            config,
            [RepeatedPostHandler()]
        )
