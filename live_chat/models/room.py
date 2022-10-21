from live_chat.config.mysqlconnection import connectToMySQL
from live_chat.models import user

class Room:
    def __init__ (self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM rooms WHERE id = %(id)s;"
        results = connectToMySQL('live_chat_schema').query_db(query,data)
        if results:
            return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM rooms;"
        rooms = []
        results = connectToMySQL("live_chat_schema").query_db(query)
        if results:
            for room in results:
                rooms.append(cls(room))
            return rooms
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM rooms WHERE id = %(id)s;"
        return connectToMySQL('live_chat_schema').query_db(query,data)

    @classmethod
    def get_rooms_not_joined(cls,data):
        query = "SELECT * FROM rooms LEFT JOIN joins ON rooms.id = joins.room_id "
        query += "WHERE rooms.id NOT IN "
        query += "(SELECT rooms.id FROM rooms LEFT JOIN joins ON rooms.id = joins.room_id "
        query += "LEFT JOIN users ON users.id = joins.user_id WHERE users.id = %(id)s);"
        results = connectToMySQL('live_chat_schema').query_db(query,data)
        if results:
            rooms = []
            for row in results:
                rooms.append(cls(row))
            return rooms

    @classmethod
    def get_users_joined(cls, data):
        query = "SELECT * FROM rooms LEFT JOIN joins ON rooms.id = joins.room_id "
        query += "LEFT JOIN users ON users.id = joins.user_id WHERE rooms.id = %(id)s;"
        results = connectToMySQL('live_chat_schema').query_db(query,data)
        if results:
            room = cls(results[0])
            room.users_joined = []
            for row in results:
                user_data = {
                    **row,
                    "id" : row["users.id"],
                    "name" : row["users.name"],
                    "created_at" : row["users.created_at"],
                    "updated_at" : row["users.updated_at"]
                }
                a_user = user.User(user_data)
                room.users_joined.append(a_user)
            return room

    @classmethod
    def recent_created(cls, data):
        query = "SELECT * FROM rooms WHERE user_id = %(user_id)s ORDER BY rooms.id DESC LIMIT 1;"
        results = connectToMySQL('live_chat_schema').query_db(query,data)
        if results:
            return cls(results[0])
    

    @classmethod
    def save(cls,data):
        query = "INSERT INTO rooms(user_id, name) "
        query += "VALUES(%(user_id)s, %(name)s);"
        return connectToMySQL('live_chat_schema').query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM rooms WHERE id = %(id)s;"
        return connectToMySQL('live_chat_schema').query_db(query, data)