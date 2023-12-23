import pymongo
from datetime import datetime


class Connection:
    """A connection to the database."""

    def __init__(self, uri):
        self.connection_string = uri
        self.client = pymongo.MongoClient(self.connection_string)
        self.current_database = "chat_program"
        self.database = self.client[self.current_database]

        # Tables
        self.logs = self.database["logs"]
        self.messages = self.database["messages"]
        self.counts = self.database["counts"]
    
    # MESSAGES

    def add_message(self, message, sender):
        try:
            count = self.get_counts()["messages"]
            code_data = {
                "_id": count,
                "timestamp": datetime.now(),
                "message": message,
                "sender": sender
            }
            self.messages.insert_one(code_data)
            self.update_counts({"messages": count + 1})
            return self.get_code(count)
        except Exception as e:
            return self.error_log(error_message=f"Code Error: {e}", error_code=1000)

    def get_message(self, value, by="_id"):
        return self.messages.find_one({by: value})
    
    def get_all_messages(self):
        return list(self.messages.find())
    
    # COUNTS

    def get_counts(self):
        return self.counts.find_one()
    
    def update_counts(self, update_data):
        result = self.counts.update_one({}, {"$set": update_data})
        return result
    
    def initialize_counts(self):
        counts = self.get_counts()

        if not counts:

            counts_data = {
                "messages": 0,
                "logs": 0,
                "users": 0
            }

            self.counts.insert_one(counts_data)

        return self.get_counts()

    def error_log(self, error_message, error_code):
        count = self.get_counts()["logs"]
        log = {
            "_id": count,
            "timestamp": datetime.now(),
            "error_code": error_code,
            "error_message": error_message,
        }
        self.logs.insert_one(log)
        self.update_counts({"logs": count + 1})

        return error_code