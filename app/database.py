import pymongo
from bson import ObjectId

from config import settings
from models import Notification


class DatabaseManager:
    def __init__(self, db_uri=settings.DB_URI, db_name=settings.DB_NAME, db_collection=settings.DB_COLLECTION):
        self.client: pymongo.MongoClient = pymongo.MongoClient(db_uri)
        self.db = self.client.get_database(name=db_name).get_collection(name=db_collection)

    def if_user_exists(self, user_id: str) -> bool:
        return bool(self.db.count_documents({'_id': ObjectId(user_id)}, limit=1))

    def add_notification(self, user_id: str, notification: Notification) -> bool:
        res = self.db.update_one({'_id': ObjectId(user_id)}, {'$push': {'notifications': notification.model_dump()}})
        if res.acknowledged:
            return True
        else:
            return False

    def get_list(self, user_id: str, skip: int, limit: int):
        return self.db.find_one({'_id': ObjectId(user_id)}, {'notifications': {'$slice': [0, limit]}, '_id': 0},
                                skip=skip)

    def read(self, user_id: str, notification_id: str) -> bool:
        res = self.db.update_one({'_id': ObjectId(user_id), 'notifications.id': notification_id},
                                 {'$set': {'notifications.$.is_new': False}})
        if res.acknowledged:
            return True
        else:
            return False

    #  Get all documents from collection for docker tests
    def get_collection(self):
        return [doc for doc in self.db.find({})]

    #  Insert document into collection for docker tests
    def insert_one(self):
        x = self.db.insert_one({'notifications': []})
        p = 1


def get_db():
    yield DatabaseManager()
