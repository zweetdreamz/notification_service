from strenum import StrEnum
from enum import auto


# noinspection PyArgumentList
class NotificationEnum(StrEnum):
    registration = auto()
    new_message = auto()
    new_post = auto()
    new_login = auto()
