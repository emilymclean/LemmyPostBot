from datetime import datetime
from typing import List, Any

import isodate
from croniter import croniter
from plemmy import LemmyHttp

from .handler import Handler, ScheduledCallback, Task
from .. import RepeatedPost, PostHelper


class RepeatedPostHandler(Handler):

    @staticmethod
    def get_next(config: RepeatedPost) -> ScheduledCallback:
        cron = croniter(config.period, datetime.now())
        next_run = cron.get_next(datetime)
        return ScheduledCallback(
            next_run,
            CreatePostTask(config).handle
        )

    def can_handle(self, config: Any) -> bool:
        return isinstance(config, RepeatedPost)

    def initial(self, config: RepeatedPost) -> List[ScheduledCallback]:
        return [RepeatedPostHandler.get_next(config)]


class CreatePostTask(Task):
    config: RepeatedPost

    def __init__(self, config: RepeatedPost):
        self.config = config

    def handle(self, request: LemmyHttp) -> List[ScheduledCallback]:
        scheduled = []

        print("Making post")
        post_id = PostHelper.create_post(
            request,
            self.config.context,
            self.config.post
        )

        scheduled.append(RepeatedPostHandler.get_next(self.config))

        if self.config.pin is not None:
            PostHelper.pin_post(request, post_id, True)
            scheduled.append(ScheduledCallback(
                datetime.now() + isodate.parse_duration(self.config.pin.pin_for),
                PostUnpinTask(post_id).handle
            ))

        return scheduled


class PostUnpinTask(Task):
    post_id: int

    def __init__(self, post_id: int):
        self.post_id = post_id

    def handle(self, request: LemmyHttp) -> List[ScheduledCallback]:
        PostHelper.pin_post(request, self.post_id, False)
        return []
