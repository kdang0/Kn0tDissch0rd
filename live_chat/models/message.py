from live_chat.config.mysqlconnection import connectToMySQL
from live_chat.models.user import User

class Message:
    def __init__(self, data):
        self.id = data["id"]
        self.message_content = data["message_content"]
        self.created_at  = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.room_id = data["room_id"]
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message_content, room_id, user_id) "
        query += "VALUES (%(message_content)s, %(room_id)s, %(user_id)s);"
        return connectToMySQL("live_chat_schema").query_db(query, data)

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        results = connectToMySQL("live_chat_schema").query_db(query,data)
        if results:
            return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages;"
        messages = []
        results = connectToMySQL('live_chat_schema').query_db(query)
        if results:
            for message in results:
                messages.append(cls(message))    
            return messages
    
    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT * FROM messages LEFT JOIN users " 
        query += "ON users.id = messages.user_id "
        query += "WHERE room_id = %(room_id)s;"
        user_messages = []
        results = connectToMySQL('live_chat_schema').query_db(query, data)
        print(results)
        if results:
            for row in results:
                message = cls(row)
                user_data = {
                    "id" : row["users.id"],
                    **row
                }
                message.user = User(user_data)
                user_messages.append(message)
            return user_messages
