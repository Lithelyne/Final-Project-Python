from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash

DATABASE = "cookbook_schema"

class Ingredient:

    def __init__(self,data:dict):
        self.id = data['id']
        self.text = data['text']
        self.recipe_id = data['recipe_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #CREATE
    @classmethod
    def save_ingredient(cls, **kwargs):
        data = kwargs
        query = "INSERT INTO ingredients (text, recipe_id) VALUES (%(text)s, %(recipe_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    #READ ALL
    @classmethod
    def get_all_ingredients(cls):
        query = "SELECT * FROM ingredients JOIN users ON ingredients.user_id=users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        ingredients = []
        for ingredient in results:
            ingredients.append(cls(ingredient))
        return ingredients

    
    # UPDATE
    @classmethod
    def update(cls,data):
        query = "UPDATE ingredients SET text=%(text)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s, date_made=%(date_made)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #DELETE
    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM ingredients WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #READ ONE WITH OTHERS (e.g. get user with ingredients)
    @classmethod
    def get_ingredient(cls,id):
        query = "SELECT * FROM ingredients JOIN users ON ingredients.user_id = users.id WHERE ingredients.id = %(id)s;"
        data = {'id':id}
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print("results =", results)
        user = cls(results[0])
        for ingredient in results:
            ingredient_data = {
                "id":ingredient["id"],
                "text":ingredient["text"],
                "description":ingredient["description"],
                "instructions":ingredient["instructions"],
                "under_30":ingredient["under_30"],
                "date_made":ingredient["date_made"],
                "user_id":ingredient["user_id"],
                "created_at":ingredient["created_at"],
                "updated_at":ingredient["updated_at"],
                "user":ingredient["first_name"],
            }
            # user.ingredients.append( Ingredient( ingredient_data ) )
        return user
    
    @staticmethod
    def validate_ingredient(ingredient):
        is_valid = True
        if len(ingredient['name']) < 1:
            is_valid = False
            flash("Name cannot be blank")
        if len(ingredient['description']) < 1:
            is_valid = False
            flash("Description cannot be blank")
        if len(ingredient['instructions']) < 1:
            is_valid = False
            flash("Instructions cannot be blank")
        if ingredient['date_made']=='':
            is_valid = False
            flash("Please select a date made")
        if 'under_30' not in ingredient:
            is_valid = False
            flash("Please select yes or no")

        return is_valid
        pass