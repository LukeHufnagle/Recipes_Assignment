from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Index Route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/')
def index():
    return render_template('index.html')


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Register Route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/register', methods=['POST'])
def register():
    if not User.register_validation(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.register(data)
    session['user_id'] = user_id
    return redirect('/dashboard')


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Login User route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }

    user_in_db = User.get_by_email(data)
    validation_data = {
        'user' : user_in_db,
        'password' : request.form['password']
    }

    if not User.login_validation(validation_data):
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Display dashboard route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/dashboard')
def dashboard():  
    data = {
        'user_id' : session['user_id']
    }
    user = User.get_user_info(data)
    recipes = Recipe.get_all_recipes(data)
    return render_template('dashboard.html', user=user, recipes = recipes)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Logout Route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Show one recipe
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/show/<int:recipe_id>')
def show_one_recipe(recipe_id):
    data = {
        'recipe_id' : recipe_id
    }
    recipe = Recipe.show_one_recipe(data)
    return render_template("show_one_recipe.html", recipe=recipe)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Edit Recipe Routes
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'recipe_id' : recipe_id
    }
    recipe = Recipe.show_one_recipe(data)
    return render_template("edit_one_recipe.html", recipe=recipe)

@app.route('/update/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/{recipe_id}")

    data = {
        'recipe_id' : recipe_id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'datemade' : request.form['datemade'],
        'under30' : request.form['under30']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')