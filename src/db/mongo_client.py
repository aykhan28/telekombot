from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="chatbot"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_message(self, user_id, role, message):
        self.db.messages.insert_one({"user_id": user_id, "role": role, "message": message})

    def get_messages(self, user_id):
        return list(self.db.messages.find({"user_id": user_id}, {"_id": 0, "role": 1, "message": 1}))

    def clear_history(self, user_id):
        self.db.messages.delete_many({"user_id": user_id})