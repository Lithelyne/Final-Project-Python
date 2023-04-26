from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
from flask_app.models import recipe

DATABASE = "cookbook_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

#If there is a User in the ERD, set this model to User
class User:

    #Add other data (self.whatever = data['whatever'])
    def __init__(self,data:dict):
        self.id = data['id']
        self.user_name = data['user_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    #READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    #CREATE - update values needed in addition to name
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (user_name, first_name, last_name, email, password) VALUES (%(user_name)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    


    # UPDATE
    @classmethod
    def update(cls,data):
        query = """UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)

    
    #FIND USER BY EMAIL
    @classmethod
    def find_by_email(cls,email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email':email}
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) > 0:
            return User(result[0]) #This returns the result as an object
        else:
            return False

    #VALIDATION
    @staticmethod
    def validate_user(user:dict):
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters")
        if not EMAIL_REGEX.match(user['email']): 
            is_valid = False
            flash("Invalid email address!")
        if User.find_by_email(user['email']):
            is_valid = False
            flash("This email is already registered")
        if len(user['password']) < 1:
            is_valid = False
            flash("You must enter a password")
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Password must match")
        return is_valid