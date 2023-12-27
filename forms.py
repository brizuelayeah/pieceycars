from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, EqualTo, NumberRange
from datetime import datetime

"""
    WTForms used in app.py
"""

"""
    Register form: a user needs to input his username, password, email and phone to be registered in the system
"""
class RegisterForm(FlaskForm):
    username = StringField("Set your username:", validators = [InputRequired()])
    password = PasswordField("Set your password:", validators = [InputRequired()])
    password2 = PasswordField("Confirm your password:", validators = [InputRequired(), EqualTo("password")])
    mail = StringField("Email:", validators = [InputRequired()])
    phone = StringField("Phone number:", validators = [InputRequired()])
    submit = SubmitField("Register")

"""
    Login form: a user needs to input his username and password to log in the system
"""
class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [InputRequired()])
    password = PasswordField("Password:", validators = [InputRequired()])
    submit = SubmitField("Log in")

"""
    Register car form: a user needs to enter the brand, model set, specific model, car year and URL car image to
    register his car in the system.
    However, the brand and the model set aren't part of this WTForm, but they are of an HTML form coded in the 
    "register_car_form.html" file. This is because I want to display a different selection form depending on the 
    brand selected by the user, and WTForms didn't allow me to do this.
"""
class RegisterCarForm(FlaskForm):
    model = StringField("Which one of the set you selected is your car? (example: If you selected MERCEDES and Class A, you can type \"A45\")", validators = [InputRequired()])
    car_year = IntegerField("Which year is your car?", validators = [InputRequired(), NumberRange(1960, datetime.now().year)])
    image_URL = StringField("Enter the URL of the image of your car)", validators = [InputRequired()])
    submit = SubmitField("Register car")

"""
    Piece I sell form: a user needs to enter the car brand of the piece, its model set, its specific model,
    its car year (the year of the car for which this piece would be recommended), its piece year, its price
    and the URL piece image to register a new piece he's selling in the system.
    However, the brand and the model set aren't part of this WTForm, but they are of an HTML form coded in the
    "piece_I_sell_form.html" file. This is because I want to display a different selection form depending on the
    brand selected by the user, and WTForms didn't allow me to do this.
"""
class PieceISellForm(FlaskForm):
    piece_name = SelectField("Which piece do you want to sell?",
    choices = ["Rear wing", "Bumpers", "Grilles", "Fenders", "Suspension", "Rim", "Splitter"], default = "Aileron",
    validators = [InputRequired()])
    model = StringField("Which one of the set you selected is your car? (example: If you selected MERCEDES and Class A, you can type \"A45\")", validators = [InputRequired()])
    car_year = IntegerField("Which year could be the car in which you would place this piece?", validators = [InputRequired(), NumberRange(1960, datetime.now().year)])
    piece_year = IntegerField("When did you buy this piece?", validators = [InputRequired(), NumberRange(1960, datetime.now().year)])
    price = IntegerField("Set a price for the piece you want to sell:", validators = [InputRequired(), NumberRange(0, )])
    image_URL = StringField("Enter the URL of the image of your piece)", validators = [InputRequired()])
    submit = SubmitField("Add piece I sell to my profile")

"""
    Piece I need form: a user needs to enter the car brand of the piece, its model set, its specific model,
    its car year (the year of the car for which this piece would be recommended), its piece year and the URL piece 
    image to register a new piece he's looking for in the system.
    However, the brand and the model set aren't part of this WTForm, but they are of an HTML form coded in the
    "piece_I_need_form.html" file. This is because I want to display a different selection form depending on the
    brand selected by the user, and WTForms didn't allow me to do this.
"""
class PieceINeedForm(FlaskForm):
    piece_name = SelectField("Which piece do you want to buy?",
    choices = ["Rear wing", "Bumpers", "Grilles", "Fenders", "Suspension", "Rim", "Splitter"], default = "Aileron",
    validators = [InputRequired()])
    model = StringField("Which one of the set you selected is your car? (example: If you selected MERCEDES and Class A, you can type \"A45\")", validators = [InputRequired()])
    car_year = IntegerField("Which year could be the car in which you would place this piece?", validators = [InputRequired(), NumberRange(1960, datetime.now().year)])
    piece_year = IntegerField("When did you buy this piece?", validators = [InputRequired(), NumberRange(1960, datetime.now().year)])
    submit = SubmitField("Add piece I want to my profile")

"""
    Piece filter form: a user needs to enter the car brand of the piece, its model set, its specific model,
    its car year (the year of the car for which this piece would be recommended) and its piece year in order to
    filter a piece or list of pieces among all the pieces registered in the system with an owner (those which are being
    sold, because those with no owner are registered just as pieces somebody is looking for, but don't need to be 
    being sold).
    However, the whole form is developed in HTML in the file "piece_filter.html".
"""