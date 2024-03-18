from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import YAMLWizard


@dataclass
class PostTemplate(YAMLWizard):
    title: str
    content: Optional[str] = field(default_factory=lambda: None)
    link: Optional[str] = field(default_factory=lambda: None)


@dataclass
class PostContext(YAMLWizard):
    community_name: str


@dataclass
class PinSettings(YAMLWizard):
    pin_for: str  # ISO8601 duration
