import time
import uuid
from typing import Optional, Annotated, Any
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer, PlainSerializer

from enums import NotificationEnum


#  `/create` request model
class CreateNotification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(min_length=24, max_length=24)
    target_id: Optional[Annotated[str, Field(min_length=24, max_length=24)]] = None
    key: NotificationEnum
    data: Optional[Annotated[dict, Field(...)]] = {}

    #  Additional validation for `key` value
    @field_validator('key')
    def validate_key(cls, password, **kwargs):
        if password not in NotificationEnum:
            raise ValueError(f'Key must be on of the following values: {[key.valule for key in NotificationEnum]}')
        return password


#  Default response model
class DefaultResponse(BaseModel):
    success: bool
    error: Optional[Annotated[str, Field(...)]] = None

    # def model_dump(self, *args, **kwargs) -> dict[str, Any]:
    #     return super().model_dump(
    #         exclude_unset=self.success,
    #         **kwargs
    #     )


#  Notification model
class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = Field(default_factory=lambda: int(time.time()))
    is_new: bool = True
    user_id: str = Field(min_length=24, max_length=24)
    key: NotificationEnum
    target_id: str = Field(min_length=24, max_length=24)
    data: dict


#  `/list` request model
class ListRequest(BaseModel):
    user_id: str = Field(min_length=24, max_length=24)
    skip: int
    limit: int


class NotificationsResponse(BaseModel):
    elements: int
    new: int
    request: ListRequest
    list: list[Notification]


#  `/list` response model
class ListNotificationsResponse(DefaultResponse):
    data: NotificationsResponse


#  `/read` request model
class ReadRequest(BaseModel):
    user_id: str = Field(min_length=24, max_length=24)
    notification_id: str


ObjectStr = Annotated[
    Any, PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]


#  `/users` response model
class User(BaseModel):
    id: ObjectStr = Field(alias='_id')
    notifications: list[Notification]
