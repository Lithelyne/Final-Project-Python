from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models.ingredient import Ingredient

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
        self.instructions = data['instructions']
        self.test = data['test']
        self.notes = data['notes']
        self.open = data['open']
        self.user_id = data['user_id']
        self.original = data['original']
        self.version = data['version']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_name = data['user_name']
        self.ingredients = []



    #READ ALL
    @classmethod
    def get_all_recipes(cls,id):
        data={'id':id}
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE user_id = %(id)s AND test = 0;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_test_recipes(cls,id):
        data={'id':id}
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE user_id = %(id)s AND test = 1;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    
    #CREATE
    @classmethod
    def save(cls, data,type=None,sub_type=None,prep_time=None,cook_time=None,description=None,notes=None):
        query = "INSERT INTO recipes (name, type, sub_type, prep_time, cook_time, description, instructions, user_id, test, notes, open, original, version) VALUES (%(name)s,%(type)s,%(sub_type)s,%(prep_time)s,%(cook_time)s,%(description)s,%(instructions)s,%(user_id)s,%(test)s,%(notes)s,%(open)s,%(original)s,%(version)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    

    #SEND TO TEST KITCHEN
    @classmethod
    def send_to_test(cls,id):
        data={'id':id}
        query = "UPDATE recipes SET test=1, original = %(id)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    # UPDATE
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, type=%(type)s, sub_type=%(sub_type)s, prep_time=%(prep_time)s, cook_time=%(cook_time)s, description=%(description)s,instructions=%(instructions)s WHERE id = %(id)s;"
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
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id JOIN ingredients on recipes.id = ingredients.recipe_id WHERE recipes.id = %(id)s;"
        data = {'id':id}
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print("results =", results)
        recipe = cls(results[0])
        for ingredient in results:
            ingredient_data = {
                "id":ingredient["ingredients.id"],
                "text":ingredient["text"],
                "created_at":ingredient["created_at"],
                "updated_at":ingredient["updated_at"],
                "recipe_id":ingredient["recipe_id"]
            }
            recipe.ingredients.append( Ingredient( ingredient_data ) )
        return recipe
    
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


        return is_valid
        pass