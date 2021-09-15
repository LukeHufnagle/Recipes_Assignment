from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Go to new recipe route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/new_recipe')
def new_recipe():
    user_id = session['user_id']
    return render_template('new_recipe.html', user_id = user_id)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Create recipe route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new_recipe')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'datemade' : request.form['datemade'],
        'under30' : request.form['under30'],
        'user_id' : request.form['user_id']
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')
