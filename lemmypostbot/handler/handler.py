from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Any, List

from plemmy import LemmyHttp


@dataclass
class ScheduledCallback:
    time: datetime
    callback: Callable[[LemmyHttp, Any], List[Any]]  # Returned Any is actually ScheduledCallback


class Handler(ABC):

    @abstractmethod
    def can_handle(self, config: Any) -> bool:
        pass

    @abstractmethod
    def initial(self, config: Any) -> List[ScheduledCallback]:
        pass

    @abstractmethod
    def handle(self, request: LemmyHttp, config: Any) -> List[ScheduledCallback]:
        pass
