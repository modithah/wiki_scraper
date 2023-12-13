import datetime
from dataclasses import dataclass

from dataclass_factory import Schema, Factory


@dataclass
class Revision:
    id: int
    user_id: int
    date: datetime.datetime
    tags: list[str]


def parse_timestamp(data):
    return datetime.datetime.fromtimestamp(data)


unixtime_schema = Schema(parser=parse_timestamp, serializer=datetime.datetime.timestamp)


factory = Factory(
    schemas={
        datetime: unixtime_schema,  # type: ignore [dict-item]
    }
)
