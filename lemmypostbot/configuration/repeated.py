from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import YAMLWizard

from .post import PostTemplate, PinSettings, PostContext


@dataclass
class RepeatedPost(YAMLWizard):
    period: str  # Cron
    post: PostTemplate
    context: PostContext
    only_first_of_month: bool = False  # Only post on the first trigger of the month
    pin: Optional[PinSettings] = field(default_factory=lambda: None)
