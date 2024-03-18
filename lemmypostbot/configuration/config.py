from dataclasses import dataclass
from typing import List

from dataclass_wizard import YAMLWizard

from .repeated import RepeatedPost


@dataclass
class Config(YAMLWizard):
    repeated: List[RepeatedPost]
