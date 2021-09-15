from flask_app import app
from flask_app.controllers import user_controller
from flask_app.config.mysqlconnection import connectToMySQL
from flask import config, flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Validate Registration static method
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @staticmethod
    def register_validation(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash("First name must be greater than two characters")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash('Last name must be greater than two characters')
            is_valid = False
        if len(form_data['password']) < 8:
            flash('Password must contain at least eight characters')
            is_valid = False
        if not form_data['password'] == form_data['conf_pass']:
            flash('Both passwords must match!')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Email must be formatted in a valid fashion')
            is_valid = False
        return is_valid
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Validate Login Static method
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @staticmethod
    def login_validation(validation_data):
        is_valid = True
        if not validation_data['user']:
            flash('Invalid Email/Password')
            is_valid = False
        elif not bcrypt.check_password_hash(validation_data['user'].password, validation_data['password']):
            flash('Invalid Email/Password')
            is_valid = False
        return is_valid


    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Register User to database
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @classmethod
    def register(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Get User by email
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL('recipes').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Get User info
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @classmethod
    def get_user_info( cls, data ):
        query = 'SELECT * FROM users WHERE id = %(user_id)s'
        results = connectToMySQL('recipes').query_db(query, data)
        return cls(results[0])
    