from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user_model


class Recipe:
    def __init__(self, data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.thirtymin = data['thirtymin']
        self.datemade = data['datemade']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.user = {}
    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash('Recipe name must be at least three characters long')
            is_valid = False
        if len(form_data['description']) < 3:
            flash('Description must be at least three characters long')
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash('Instructions must be at least three characters long')
            is_valid = False
        return is_valid
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Create new recipe
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @classmethod
    def create_recipe( cls, data ):
        query = 'INSERT INTO recipes (name, description, instructions, datemade, thirtymin, user_id, created_at, updated_at) VALUES( %(name)s, %(description)s, %(instructions)s, %(datemade)s, %(under30)s, %(user_id)s, NOW(), NOW());'
        results = connectToMySQL('recipes').query_db(query, data)
        return results
    
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Get all recipes
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @classmethod
    def get_all_recipes(cls, data):
        query = 'SELECT * FROM recipes LEFT JOIN users ON users.id = user_id WHERE user_id = %(user_id)s'
        results = connectToMySQL('recipes').query_db(query, data)

        all_recipes = []

        for row in results:
            recipe = cls(row) 
            
            user_data = {
                'id'  : row['users.id'],
                'first_name'  : row['first_name'],
                'last_name'  : row['last_name'],
                'email'  : row['email'],
                'password' : row['password'],
                'created_at'  : row['users.created_at'],
                'updated_at'  : row['users.updated_at']
            }
            recipe.user = user_model.User(user_data)
            all_recipes.append(recipe)
        return all_recipes
    
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Get all recipes
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @classmethod
    def show_one_recipe(cls, data):
        query = 'SELECT * FROM recipes LEFT JOIN users ON users.id = user_id WHERE recipes.id = %(recipe_id)s'
        results = connectToMySQL('recipes').query_db(query, data)

        recipe = cls(results[0])
        user_data = {
                'id'  : results[0]['users.id'],
                'first_name'  : results[0]['first_name'],
                'last_name'  : results[0]['last_name'],
                'email'  : results[0]['email'],
                'password' : results[0]['password'],
                'created_at'  : results[0]['users.created_at'],
                'updated_at'  : results[0]['users.updated_at']
        }
        recipe.user = user_model.User(user_data)
        return recipe

    @classmethod
    def update_recipe( cls, data ):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, datemade = %(datemade)s, thirtymin = %(under30)s, updated_at = NOW() WHERE id = %(recipe_id)s;'
        results = connectToMySQL('recipes').query_db(query, data)
        return 