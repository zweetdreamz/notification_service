from database import DatabaseManager, get_db
from enums import NotificationEnum
from models import Notification, ListNotificationsResponse, NotificationsResponse, ListRequest
from tasks import send_email_report_dashboard


class NotificationManager:
    def __init__(self, database: DatabaseManager):
        self.database = database

    def create(self, user_id: str, key: NotificationEnum, target_id: str | None = None, data: dict = None) -> bool:
        #  Check if user_id exists
        if not self.database.if_user_exists(user_id=user_id):
            raise Exception(f'User doesnt exist user_id = {user_id}')

        #  Check if target_id exists
        if key == NotificationEnum.new_message or key == NotificationEnum.new_login:
            if not self.database.if_user_exists(user_id=target_id):
                raise Exception(f'User doesnt exist target_id = {target_id}')

        match key:
            case NotificationEnum.registration:
                send_email_report_dashboard.delay(key=key)
                return True
            case NotificationEnum.new_message:
                notification = Notification(
                    user_id=user_id,
                    key=key,
                    target_id=target_id,
                    data=data
                )
                return self.database.add_notification(user_id=user_id, notification=notification)
            #  В задании пояснение для new_message = new_post
            case NotificationEnum.new_post:
                raise NotImplemented()
            case NotificationEnum.new_login:
                send_email_report_dashboard.delay(key=key)
                notification = Notification(
                    user_id=user_id,
                    key=key,
                    target_id=target_id,
                    data=data
                )
                return self.database.add_notification(user_id=user_id, notification=notification)
            case _:
                raise Exception(f'Unexpected key = {key}')

    def get_list(self, user_id: str, skip: int, limit: int) -> NotificationsResponse:
        #  Check if user_id exists
        if not self.database.if_user_exists(user_id=user_id):
            raise Exception(f'User doesnt exist user_id = {user_id}')

        notifications = self.database.get_list(user_id=user_id, skip=skip, limit=limit)['notifications']
        new_notifications_count = len([notif for notif in notifications if notif.get('is_new')])
        return NotificationsResponse(
            new=new_notifications_count,
            elements=len(notifications),
            list=notifications,

            #  Не слишком изящно, но как-то при проектировании упустил момент с полем `request` в ответе
            request=ListRequest(
                user_id=user_id,
                skip=skip,
                limit=limit
            )
        )

    def read(self, user_id: str, notification_id: str) -> bool:
        #  Check if user_id exists
        if not self.database.if_user_exists(user_id=user_id):
            raise Exception(f'User doesnt exist user_id = {user_id}')

        return self.database.read(user_id=user_id, notification_id=notification_id)

    def get_collection(self):
        return self.database.get_collection()

    def generate(self):
        self.database.insert_one()


def get_manager():
    yield NotificationManager(database=next(get_db()))
