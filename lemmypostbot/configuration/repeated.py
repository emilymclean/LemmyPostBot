from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import YAMLWizard

from .post import PostTemplate, PinSettings


@dataclass
class RepeatedPost(YAMLWizard):
    period: str  # Cron
    post: PostTemplate
    pin: Optional[PinSettings] = field(default_factory=lambda: None)
