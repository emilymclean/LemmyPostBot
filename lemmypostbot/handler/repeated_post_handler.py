from datetime import datetime
from typing import List, Any

import isodate
from croniter import croniter
from plemmy import LemmyHttp

from .handler import Handler, ScheduledCallback
from .. import RepeatedPost, PostHelper


class RepeatedPostHandler(Handler):

    def can_handle(self, config: Any) -> bool:
        return config is RepeatedPostHandler

    def _get_next(self, config: RepeatedPost) -> ScheduledCallback:
        cron = croniter(config.period, datetime.now())
        next_run = cron.get_next(datetime)
        return ScheduledCallback(
            next_run,
            self.handle
        )

    def initial(self, config: RepeatedPost) -> List[ScheduledCallback]:
        return [self._get_next(config)]

    def handle(self, request: LemmyHttp, config: RepeatedPost) -> List[ScheduledCallback]:
        scheduled = []

        post_id = PostHelper.create_post(
            request,
            config.context,
            config.post
        )

        scheduled += self._get_next(config)

        if config.pin is not None:
            PostHelper.pin_post(request, post_id, True)
            scheduled += ScheduledCallback(
                datetime.now() + isodate.parse_duration(config.pin.pin_for),
                PostUnpinTask(post_id).unpin
            )

        return scheduled


class PostUnpinTask:
    post_id: int

    def __init__(self, post_id: int):
        self.post_id = post_id

    def unpin(self, request: LemmyHttp, config: RepeatedPost) -> List[ScheduledCallback]:
        PostHelper.pin_post(request, self.post_id, False)
        return []