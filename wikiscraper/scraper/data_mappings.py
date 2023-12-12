import datetime
from dataclasses import dataclass, field


@dataclass
class Revision:
    id: int
    user_id: int
    date: datetime.datetime
    tags: list[str]
