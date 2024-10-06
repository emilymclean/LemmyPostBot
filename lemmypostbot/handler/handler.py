from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Any, List, Dict

from pythonlemmy import LemmyHttp


@dataclass
class ScheduledCallback:
    time: datetime
    task_name: str
    task_args: Dict[str, Any]


class Task(ABC):

    @abstractmethod
    def task_name(self) -> str:
        pass

    @abstractmethod
    def exec(self, http: LemmyHttp, args: Dict[str, Any]) -> List[ScheduledCallback]:
        pass


class Handler(ABC):

    @abstractmethod
    def can_handle(self, config: Any) -> bool:
        pass

    @abstractmethod
    def initial(self, config: Any) -> List[ScheduledCallback]:
        pass

    @abstractmethod
    def list_tasks(self) -> List[Task]:
        pass
