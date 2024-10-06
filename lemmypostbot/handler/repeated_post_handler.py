from datetime import datetime
from typing import List, Any, Dict

import isodate
from croniter import croniter
from pythonlemmy import LemmyHttp

from .handler import Handler, ScheduledCallback, Task
from .. import RepeatedPost, PostHelper


class RepeatedPostHandler(Handler):

    @staticmethod
    def get_next(config: RepeatedPost) -> ScheduledCallback:
        cron = croniter(config.period, datetime.now())
        next_run = cron.get_next(datetime)
        return ScheduledCallback(
            next_run,
            CreatePostTask.name,
            {"config": config}
        )

    def can_handle(self, config: Any) -> bool:
        return isinstance(config, RepeatedPost)

    def initial(self, config: RepeatedPost) -> List[ScheduledCallback]:
        return [RepeatedPostHandler.get_next(config)]

    def list_tasks(self) -> List[Task]:
        return [CreatePostTask(), PostUnpinTask()]


class CreatePostTask(Task):
    name = "create_post_task"

    def task_name(self) -> str:
        return self.name

    def exec(self, request: LemmyHttp, args: Dict[str, Any]) -> List[ScheduledCallback]:
        config: RepeatedPost = args["config"]
        scheduled = [RepeatedPostHandler.get_next(config)]

        if config.only_first_of_month and not self._first_occurrence_in_month(config):
            return scheduled

        print("Making post")
        post_id = PostHelper.create_post(
            request,
            config.context,
            config.post
        )

        if config.pin is not None:
            PostHelper.pin_post(request, post_id, True)
            scheduled.append(ScheduledCallback(
                datetime.now() + isodate.parse_duration(config.pin.pin_for),
                PostUnpinTask.name,
                {"post_id": post_id}
            ))

        return scheduled

    @staticmethod
    def _first_occurrence_in_month(config: RepeatedPost, current_date: datetime = datetime.today()) -> bool:
        cron = croniter(config.period, current_date.replace(day=1))
        next_run: datetime = cron.get_next(datetime)

        return next_run.day == current_date.day


class PostUnpinTask(Task):
    name = "post_unpin_task"

    def task_name(self) -> str:
        return self.name

    def exec(self, request: LemmyHttp, args: Dict[str, Any]) -> List[ScheduledCallback]:
        post_id: int = args["post_id"]
        PostHelper.pin_post(request, post_id, False)
        return []
