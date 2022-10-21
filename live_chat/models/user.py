from live_chat.config.mysqlconnection import connectToMySQL
from live_chat import bcrypt
from live_chat.models.room import Room
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_cur_user(cls, data):
        query = "SELECT * FROM users WHERE"
        query += ' AND'.join(f' {key} = %({key})s' for key in data)
        query += ";"
        user = connectToMySQL('live_chat_schema').query_db(query, data)
        if user:
            return cls(user[0])

    @classmethod
    def save(cls, data):
        data['password'] = bcrypt.generate_password_hash(data["password"])
        query = "INSERT INTO users (name, email, password)"
        query += " VALUES(%(name)s, %(email)s, %(password)s);"

        return connectToMySQL('live_chat_schema').query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users = []
        results = connectToMySQL("live_chat_schema").query_db(query)
        if results:
            for user in results:
                users.append(cls(user))
            return users

    @classmethod
    def get_rooms_joined(cls,data):
        query = "SELECT * FROM users LEFT JOIN joins ON users.id = joins.user_id "
        query += "LEFT JOIN rooms ON rooms.id = joins.room_id WHERE users.id = %(id)s;"
        results = connectToMySQL('live_chat_schema').query_db(query,data)
        if results:
            user = cls(results[0])
            user.rooms_joined = []
            for row in results:
                room_data = {
                    "id" : row["rooms.id"],
                    "name" : row["rooms.name"],
                    "created_at" : row["rooms.created_at"],
                    "updated_at" : row["rooms.updated_at"],
                    "user_id" : row["rooms.user_id"]
                }
                room = Room(room_data)
                user.rooms_joined.append(room)
            return user


    @classmethod
    def join(cls, data):
        query = "INSERT INTO joins(room_id, user_id) "
        query += "VALUES(%(room_id)s, %(user_id)s);"
        return connectToMySQL('live_chat_schema').query_db(query,data)

    @classmethod
    def leave(cls,data):
        query = "DELETE FROM joins WHERE room_id = %(room_id)s AND user_id = %(user_id)s;"
        return connectToMySQL('live_chat_schema').query_db(query,data)

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user["name"]) < 2 and not user["name"].isalpha():
            flash("Invalid name", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email", "register")
            is_valid = False
        results = User.get_cur_user({"email" : user["email"]})
        if results:
            flash("This email is already taken", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_login(data):
        
        user_in_db = User.get_cur_user({"email" : data["email"]})
        if not user_in_db:
            flash("Invalid Email/Password", "login")
            return False
        if not bcrypt.check_password_hash(user_in_db.password, data['password']):
            flash("Invalid Email/Password", "login")
            return False
        return True