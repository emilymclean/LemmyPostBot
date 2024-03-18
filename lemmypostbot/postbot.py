from datetime import datetime
from time import sleep
from typing import List, Any

from plemmy import LemmyHttp

from . import RepeatedPostHandler
from .configuration import Config
from .handler import Handler
from .handler.handler import ScheduledCallback


class LemmyPostBot:
    http: LemmyHttp
    config: Config
    handlers: List[Handler]
    _queue: List[ScheduledCallback] = []

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

    def run(self):
        print("Initialising configuration")
        self._handle(self.config.repeated)

        while True:
            print(f"Task queue size {len(self._queue)}")
            if len(self._queue) == 0:
                return

            callback = self._queue.pop(0)
            waiting_time = (callback.time - datetime.now()).total_seconds()
            print(f"Waiting time for next item: {waiting_time}")
            if waiting_time > 0:
                sleep(waiting_time)

            self._add_all_to_queue(callback.callback(self.http))
            pass

    def _handle(self, configs: List[Any]):
        if len(configs) == 0:
            return

        handler = next(x for x in self.handlers if x.can_handle(configs[0]))

        for config in configs:
            self._add_all_to_queue(handler.initial(config))

    def _add_all_to_queue(self, callbacks: List[ScheduledCallback]):
        for callback in callbacks:
            self._add_to_queue(callback)

    def _add_to_queue(self, callback: ScheduledCallback):
        if len(self._queue) == 0:
            self._queue.append(callback)
            return

        index = -1
        for i, item in enumerate(self._queue):
            if item.time > callback.time:
                index = i
                break

        if index == -1:
            self._queue.append(callback)
        else:
            self._queue.insert(index, callback)
