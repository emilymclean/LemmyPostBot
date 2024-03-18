from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional

import isodate
from dataclass_wizard import YAMLWizard


@dataclass
class PostTemplate(YAMLWizard):
    title: str
    content: Optional[str] = field(default_factory=lambda: None)
    link: Optional[str] = field(default_factory=lambda: None)


@dataclass
class PinSettings(YAMLWizard):
    pin_for: str  # ISO8601 duration
