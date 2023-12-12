import datetime
from dataclasses import dataclass


@dataclass
class Revision:
    id: int
    user_id: int
    date: datetime.datetime
    tags: list[str]
