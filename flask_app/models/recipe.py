from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash

DATABASE = "cookbook_schema"

class Recipe:

    def __init__(self,data:dict):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.sub_type = data['sub_type']
        self.prep_time = data['prep_time']
        self.cook_time = data['cook_time']
        self.description = data['description']
        self.directions = data['directions']
        self.test = data['test']
        self.notes = data['notes']
        self.open = data['open']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['user_name']
        self.version = data['version']


    #READ ALL
    @classmethod
    def get_all_recipes(cls,id):
        data={'id':id}
        query = "SELECT * FROM recipes WHERE user_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, type, sub_type, prep_time, cook_time, description, directions, test, notes, open, user_id) VALUES (%(name)s,%(type)s,%(sub_type)s,%(prep_time)s,%(cook_time)s,%(description)s,%(directions)s,%(test)s,%(notes)s,%(open)s,%(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # UPDATE
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, type=%(type)s, sub_type=%(sub_type)s, prep_time=%(prep_time)s, cook_time=%(cook_time)s, description=%(description)s,directions=%(directions)s,test=%(test)s,notes=%(notes)s,open=%(open)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #DELETE
    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #READ ONE WITH OTHERS (e.g. get user with recipes)
    @classmethod
    def get_recipe(cls,id):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        data = {'id':id}
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print("results =", results)
        user = cls(results[0])
        for recipe in results:
            recipe_data = {
                "id":recipe["id"],
                "name":recipe["name"],
                "description":recipe["description"],
                "instructions":recipe["instructions"],
                "under_30":recipe["under_30"],
                "date_made":recipe["date_made"],
                "user_id":recipe["user_id"],
                "created_at":recipe["created_at"],
                "updated_at":recipe["updated_at"],
                "user":recipe["first_name"],
            }
            # user.recipes.append( Recipe( recipe_data ) )
        return user
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            is_valid = False
            flash("Name cannot be blank")
        if len(recipe['description']) < 1:
            is_valid = False
            flash("Description cannot be blank")
        if len(recipe['instructions']) < 1:
            is_valid = False
            flash("Instructions cannot be blank")
        if recipe['date_made']=='':
            is_valid = False
            flash("Please select a date made")
        if 'under_30' not in recipe:
            is_valid = False
            flash("Please select yes or no")

        return is_valid
        pass