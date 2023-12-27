"""
    App developed by Óscar Brizuela (122118103)
    Date: March 2023,
    Module: Web Development II (CS1116)
    UCC (University College of Cork)
"""

from flask import Flask, render_template, redirect, session, url_for, g, request
from flask_session import Session
from database import get_db, close_db
from forms import RegisterForm, LoginForm, PieceISellForm, PieceINeedForm, RegisterCarForm
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash

"""
IMPORTANT NOTES TO USE PIECEYCARS APP:

    --> Users passwords (username: password):
        - Connor McGregor: connor1
        - Michael OHalloran: michael2
        - Bennet Riordan: bennet3
        - Fintan Lukes: fintan4
        - Conor Murphy: conor5
        - Daniel Steve: daniel6
        - You can register yourself with the username and password you want

    --> Once you are logged in, you MUST log out to access properly 
        the landing page (route: http://127.0.0.1:5000/)

    --> You should execute the "schema.sql" file before running the app

    --> As commented in line 400 of this file, there's a problem when searching for 
        pieces with piece name = "Grilles", because there are more than 1 grilles registered,
        but only one appears. This doesn't happen with other pieces.
    
    --> I don't know how to let a user upload a real image to the system, so in order to simulate it,
        when a user registers a new piece or a car, he's asked just for its "fake" image URL.
    
    --> When searching a piece depending on the user cars (route in line 346), you must select a car for
        which specifications (brand, model...) match an existing piece in the system if you want to see 
        the pieces available for that car. If not, no piece will be showed, because there could be no pieces
        that match that car specifications.
        For example, when logging in with user "Connor McGregor", you can select his Audi A1-A4, because an 
        "AUDI A1-A4" from 2016 is registered in the system.
"""

"""
    Variable assignations for a correct flask use when using a DB and a session
"""
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "this-is-my-secret-key"
Session(app)
app.teardown_appcontext(close_db)

"""
    Auxiliary routes: I decided not to remove the routes that helped me with the testing
    while developing the app. These just show all the content of the DB tables in that moment.
"""

# Display all the users registered in the system
@app.route("/all_users", methods = ["GET", "POST"])
def all_users():
    db = get_db()
    users = db.execute("""SELECT * FROM user;""").fetchall()
    return render_template("all_users.html", users = users)

# Display all the cars registered in the system
@app.route("/all_cars", methods = ["GET", "POST"])
def all_cars():
    db = get_db()
    cars = db.execute("""SELECT * FROM car;""").fetchall()
    return render_template("all_cars.html", cars = cars)

# Display all the pieces registered in the system
@app.route("/all_pieces", methods = ["GET", "POST"])
def all_pieces():
    db = get_db()
    pieces = db.execute("""SELECT * FROM piece;""").fetchall()
    return render_template("all_pieces.html", pieces = pieces)

# Display all the "needs" (who wants what) registered in the system
@app.route("/all_needs", methods = ["GET", "POST"])
def all_needs():
    db = get_db()
    needs = db.execute("""SELECT * FROM need;""").fetchall()
    return render_template("all_needs.html", needs = needs)

"""
    String functions developed by me used for later features
"""
# Given a string string, it returns the string concatenated with a 3-digit random number
def randomUsername(user):
    return user + str(randint(0, 999))

# Given a string, it returns the same string but with its first letter in uppercase
def capitalize_first_letter(word):
    first_letter = word[0]
    first_letter = first_letter.upper()
    word = first_letter + word[1:]
    return word

"""
    Functions needed for checking the user login, sessions...
"""

@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next = request.url))
        return view(*args, **kwargs)
    return wrapped_view


"""
    Routes used in the app: the following routes and functions are the main app backend development.
"""

# Landing page, where the user can decide whether register, if he's not registered in the system yet,
# or log in, if he already has an account registered in the system.
@app.route("/", methods = ["GET", "POST"])
def register_login():
    return render_template("register_login.html")

# Home page, where the user can mainly see all the selling pieces registered in the app
@app.route("/home_page/<int:user_id>", methods = ["GET", "POST"])
def home_page(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    all_pieces = db.execute("""SELECT * FROM piece, user WHERE piece.owner != ? AND 
    piece.owner = user.user_id;""", ("None", )).fetchall()
    return render_template("home_page.html", user = user, all_pieces = all_pieces)

# Profile page, where the user can see his cars, the pieces he is looking for and the pieces he's selling
@app.route("/your_profile/<int:user_id>")
def your_profile(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone() 
    user_cars = db.execute("""SELECT * FROM car WHERE owner = ?""", (user_id,)).fetchall()
    pieces_user_needs = db.execute("""SELECT * FROM need, piece WHERE wanter = ? AND 
                                    need.piece_needed = piece.piece_id;""", (user_id,)).fetchall()
    pieces_user_sells = db.execute("""SELECT * FROM piece WHERE owner = ?;""", (user_id,)).fetchall()
    return render_template("your_profile.html", user_cars = user_cars,  user = user, pieces_user_sells = pieces_user_sells, pieces_user_needs = pieces_user_needs)

# Register form page, where the user can register himself in the system
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        mail = form.mail.data
        phone = form.phone.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM user WHERE username = ?""", (username,)).fetchone()
        if possible_clashing_user is not None:  # if the username has already been used...
            form.username.errors.append("Username already taken. Try with " + randomUsername(username))
        else:                                   # if the username hasn't been registered yet in the DB...
            db.execute("""INSERT INTO user (username, password_hash, mail, phone) VALUES (?, ?, ?, ?);""", (username, generate_password_hash(password), mail, phone))
            db.commit()
            user_registered = db.execute("""SELECT * FROM user WHERE username = ?""", (username,)).fetchone()
            return redirect(url_for("registered_successfully", user_id = user_registered["user_id"]))
    return render_template("register_form.html", form = form)

# Log in form page, where the user can log in the app if he previously has registered himself (or if he's one
# of the 6 user registered implicitly in the SQL file)
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        user_trying_to_login = db.execute("""SELECT * FROM user WHERE username = ?""", (username,)).fetchone()
        if user_trying_to_login is None:            # If there's nobody registered with that username...
            form.username.errors.append("Username is incorrect. Try again")
        elif not check_password_hash(user_trying_to_login["password_hash"], password):
                                                    # If the password provided doesn't match with the one stored in the DB...
            form.username.errors.append("Password is incorrect. Try again")
        else:                                       # If both the username and the password match...
            session.clear()
            session["user_id"] = user_trying_to_login["user_id"]
            return redirect(url_for("home_page", user_id = user_trying_to_login["user_id"]))
    return render_template("login_form.html", form = form)

# Register confirmation page 
@app.route("/registered_successfully/<int:user_id>", methods = ["GET", "POST"])
def registered_successfully(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    return render_template("registered_successfully.html", user = user)

# Car register form page, where the user can register his cars in the system.
# As explained in the "forms.py" file, the form is a mix between a WTForm and a HTML form 
# (see reasons in "forms.py" -> RegisterCarForm description)
@app.route("/register_my_car/<int:user_id>", methods = ["GET", "POST"])
def register_my_car(user_id):
    form = RegisterCarForm()
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    car_registered = ""
    if form.validate_on_submit():
        brand = request.values.get('brand')
        model_set = request.values.get('model')
        model = form.model.data
        car_year = form.car_year.data
        image_URL = form.image_URL.data
        if brand == "bmw":
            brand = brand.upper()
        else:
            brand = capitalize_first_letter(brand)
        if model_set != "iX":
            model_set = capitalize_first_letter(model_set)
        if model != "iX":
            model = capitalize_first_letter(model)
        db.execute("""INSERT INTO car (brand, model_set, model, year, owner, image_URL) VALUES (?, ?, ?, ?, ?, ?);""", (brand, model_set, model, car_year, user_id, image_URL)).fetchone()
        db.commit()
        car_registered = db.execute("""SELECT * FROM car WHERE owner = ? AND brand = ? AND model_set = ? AND model = ? AND year = ?;""", (user_id, brand, model_set, model, car_year)).fetchone()
        return redirect(url_for("car_registered_successfully", user_id = user["user_id"], car_id = car_registered["car_id"]))
    return render_template("register_car_form.html", form = form, user = user, car = car_registered)

# "Piece a user is looking for" form page, where the user can register the pieces he's looking for in the system.
# As explained in the "forms.py" file, the form is a mix between a WTForm and a HTML form 
# (see reasons in "forms.py" -> PieceINeedForm description)
@app.route("/add_piece_I_need/<int:user_id>", methods = ["GET", "POST"])
def add_piece_I_need(user_id):
    form = PieceINeedForm()
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    if form.validate_on_submit():
        piece_name = form.piece_name.data
        brand = request.values.get('brand')
        model_set = request.values.get('model')
        model = form.model.data
        if brand == "bmw":
            brand = brand.upper()
        else:
            brand = capitalize_first_letter(brand)
        if model_set != "iX":
            model_set = capitalize_first_letter(model_set)
        if model != "iX":
            model = capitalize_first_letter(model)
        car_year = form.car_year.data
        piece_year = form.piece_year.data
        old_piece = db.execute("""SELECT * FROM piece WHERE name = ? AND car_year = ? AND piece_year = ? AND car_brand = ? AND car_model_set = ? AND car_model = ?;""", 
                               (piece_name, car_year, piece_year, brand, model_set, model)).fetchone()
        if old_piece is None:       # if there is not yet a piece with all the specifications provided by the user in the system,
                                    # a new piece with no owner is inserted in the piece table and in the need table
            db.execute("""INSERT INTO piece (name, car_brand, car_model_set, car_model, car_year, piece_year) VALUES (?, ?, ?, ?, ?, ?);""",
                        (piece_name, brand, model_set, model, car_year, piece_year,))
            db.commit()
            new_piece_inserted_with_no_owner = db.execute("""SELECT * FROM piece WHERE name = ? AND 
                                                        car_year = ? AND piece_year = ? AND car_brand = ? AND car_model_set = ? AND car_model = ?;""", 
                                                        (piece_name, car_year, piece_year, brand, model_set, model)).fetchone()
            db.execute("""INSERT INTO need (piece_needed, wanter) VALUES (?, ?);""", (new_piece_inserted_with_no_owner["piece_id"], user_id))
            db.commit()
            piece_id_redirect = new_piece_inserted_with_no_owner["piece_id"]
            existing_piece_value = 0

        else:   # if there is already a piece with all the specifications provided by the user in the system,
                # we only have to insert a new piece in the need table, not in the piece table
            db.execute("""INSERT INTO need (piece_needed, wanter) VALUES (?, ?);""", (old_piece["piece_id"], user_id))
            db.commit()
            piece_already_existing = db.execute("""SELECT * FROM piece WHERE name = ? AND 
                                                        car_year = ? AND piece_year = ? AND car_brand = ? AND car_model_set = ? AND car_model = ?;""", 
                                                        (piece_name, car_year, piece_year, brand, model_set, model)).fetchone()
            piece_id_redirect = piece_already_existing["piece_id"]
            existing_piece_value = 1
        return redirect(url_for("added_successfully_piece_I_need", user_id = user["user_id"], piece_id = piece_id_redirect, existing_piece = existing_piece_value))
    return render_template("piece_I_need_form.html", form = form, user = user)

# "Piece a user is selling" form page, where the user can register the pieces he wants to sell in the system.
# As explained in the "forms.py" file, the form is a mix between a WTForm and a HTML form 
# (see reasons in "forms.py" -> PieceISellForm description)
# Unlike the "Piece a user is looking for" form, a user can add to his selling pieces a piece that 
# he was already selling
@app.route("/add_piece_I_sell/<int:user_id>", methods = ["GET", "POST"])
def add_piece_I_sell(user_id):
    form = PieceISellForm()
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    if form.validate_on_submit():
        piece_name = form.piece_name.data
        brand = request.values.get('brand')
        model_set = request.values.get('model')
        model = form.model.data
        car_year = form.car_year.data
        piece_year = form.piece_year.data
        price = form.price.data
        image_URL = form.image_URL.data
        if brand == "bmw":
            brand = brand.upper()
        else:
            brand = capitalize_first_letter(brand)
        if model_set != "iX":
            model_set = capitalize_first_letter(model_set)
        if model != "iX":
            model = capitalize_first_letter(model)
        db.execute("""INSERT INTO piece(name, car_brand, car_model_set, car_model, car_year, piece_year, owner, price, image_URL) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (piece_name, brand, model_set, model, car_year, piece_year, user_id, price, image_URL))
        db.commit()
        piece_registered = db.execute("""SELECT * FROM piece WHERE name = ? AND car_brand = ? AND car_model_set = ? AND car_year = ? AND piece_year = ? AND price = ?;""",
                                       (piece_name, brand, model_set, car_year, piece_year, price, )).fetchone()
        return redirect(url_for("added_successfully_piece_I_sell", user_id = user["user_id"], piece_id = piece_registered["piece_id"]))
    return render_template("piece_I_sell_form.html", form = form, user = user)

# Car register confirmation page
@app.route("/car_registered_successfully/<int:user_id>/<int:car_id>", methods = ["GET", "POST"])
def car_registered_successfully(user_id, car_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    car = db.execute("""SELECT * FROM car WHERE car_id = ?;""", (car_id, )).fetchone()
    user_cars_list = db.execute("""SELECT * FROM car WHERE owner = ?;""", (user_id, )).fetchall()
    return render_template("car_registered_successfully.html", user = user, user_cars_list = user_cars_list, car_added = car)

# Add piece I need confirmation page
@app.route("/added_successfully_piece_I_need/<int:user_id>/<int:piece_id>/<int:existing_piece>", methods = ["GET", "POST"])
def added_successfully_piece_I_need(user_id, piece_id, existing_piece):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    piece = db.execute("""SELECT * FROM piece WHERE piece_id = ?;""", (piece_id, )).fetchone()
    pieces_I_need = db.execute("""SELECT * FROM need, piece WHERE need.wanter = ? AND 
                                piece.piece_id = need.piece_needed;""", (user_id,)).fetchall()
    if existing_piece == 0:
        return render_template("added_successfully_needed_piece.html", user = user,  piece_added_to_need = piece, pieces_I_need = pieces_I_need)
    else:
        return render_template("piece_already_added.html", user = user,  piece_added_to_need = piece)

# Add piece I sell confirmation page
@app.route("/added_successfully_piece_I_sell/<int:user_id>/<int:piece_id>", methods = ["GET", "POST"])
def added_successfully_piece_I_sell(user_id, piece_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    piece = db.execute("""SELECT * FROM piece WHERE piece_id = ?;""", (piece_id, )).fetchone()
    pieces_I_sell = db.execute("""SELECT * FROM piece WHERE owner = ?;""", (user_id,)).fetchall()
    return render_template("added_successfully_selling_piece.html", user = user, piece_registered = piece, pieces_I_sell = pieces_I_sell)

# "Search piece depending on user car" form page, where a user can search the pieces available for him
# according to the cars he owns
@app.route("/search_piece_depending_on_car/<int:user_id>", methods = ["GET", "POST"])
def search_piece_depending_on_car(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    cars_list = db.execute("""SELECT * FROM car WHERE owner = ?;""", (user_id, )).fetchall()
    return render_template("search_piece_depending_on_car.html", cars_list = cars_list, user = user)

# "Search piece depending on user car" results page, where a user can look at the pieces results from the search
@app.route("/show_pieces_for_car/<int:user_id>", methods = ["GET", "POST"])
def show_pieces_for_car(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    car_from_form = request.values.get('cars')
    user_car = db.execute("""SELECT * FROM car, user WHERE car.owner = user.user_id AND car.car_id = ?;""", (car_from_form, )).fetchone()
    pieces_for_user_car = db.execute("""SELECT * FROM piece, user WHERE piece.car_brand = ? AND piece.car_model_set = ?
                                    AND piece.car_year = ? AND piece.owner = user.user_id;""", (user_car["brand"], user_car["model_set"], user_car["year"], )).fetchall()
    return render_template("pieces_available_car.html", pieces_for_user_car = pieces_for_user_car, user = user, user_car = user_car)


# "Pieces available" results page, where a user can see all the pieces registered in the system according to his needs
# (in other words, pieces the user is looking for and are available in the system)
@app.route("/pieces_available/<int:user_id>", methods = ["GET", "POST"])
def pieces_available(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    pieces_available = db.execute("""SELECT * FROM need, piece, user WHERE need.wanter = ? AND
                                    piece.piece_id = need.piece_needed AND piece.owner != ?  AND piece.owner = user.user_id;""", (user_id, "None")).fetchall() 
    return render_template("pieces_available_for_user.html", user = user, pieces_available = pieces_available)

# User profile page when visited by the user logged in, where he can see the visited user cars, needs and selling pieces.
@app.route("/piece_owner_profile/<int:user_id>/<int:user_visited_id>")
def piece_owner_profile(user_id, user_visited_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    user_visited = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_visited_id, )).fetchone()
    user_visited_cars = db.execute("""SELECT * FROM car WHERE owner = ?;""", (user_visited_id, )).fetchall()
    pieces_user_visited_sells = db.execute("""SELECT * FROM piece WHERE owner = ?;""", (user_visited_id, )).fetchall()
    pieces_user_visited_needs = db.execute("""SELECT * FROM piece, need WHERE wanter = ? AND 
                                    need.piece_needed = piece.piece_id;""", (user_visited_id, )).fetchall()
    return render_template("piece_owner_profile.html", user = user, 
                           user_visited = user_visited, user_visited_cars = user_visited_cars, 
                           pieces_user_visited_sells = pieces_user_visited_sells, pieces_user_needs = pieces_user_visited_needs)

# Piece filter page, where the user can search a piece/list of pieces according to the inputs provided,
# like the piece name, the car brand, the model...
# # As explained in the "forms.py" file, the form is a HTML form 
# (see reasons in "forms.py" -> PieceFilterForm description)
@app.route("/piece_filter/<int:user_id>", methods = ["GET", "POST"])
def piece_filter(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    return render_template("piece_filter.html", user = user)

# Piece filter results page, where the user can see the results of the previous filter.
# Attention: there is a bug when in the previous filter the piece name "Grilles" is selected
@app.route("/piece_filtered/<int:user_id>", methods = ["GET", "POST"])
def piece_filtered(user_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    piece_name = request.values.get('piece_name')
    car_brand = request.values.get('brand')
    car_model_set = request.values.get('model')
    car_year = request.values.get('car_year')
    piece_year = request.values.get('piece_year')
    query = "SELECT * FROM piece, user WHERE piece.owner = user.user_id"
    params = []
    recent_search = ""
    if car_brand:
        if car_brand == "bmw":
            car_brand = car_brand.upper()
        else:
            car_brand = capitalize_first_letter(car_brand)
        query += " AND piece.car_brand = ?"
        params.append(car_brand)
        recent_search = recent_search + "Brand: " + car_brand + "/"
    if car_model_set:
        if car_model_set != "iX":
            car_model_set = capitalize_first_letter(car_model_set)
        query += " AND piece.car_model_set = ?"
        params.append(car_model_set)
        recent_search = recent_search + "Model set: " + car_model_set + "/"
    if piece_name:
        query += " AND piece.name = ?"
        params.append(piece_name)
        recent_search = recent_search + "Name: " + piece_name + "/"
    if car_year:
        query += " AND piece.car_year = ?"
        params.append(car_year)
        recent_search = recent_search + "Car year: " + car_year + "/"
    if piece_year:
        query += " AND piece.piece_year = ?"
        params.append(piece_year)
        recent_search = recent_search + "Piece year: " + piece_year + "/"
    recent_search = recent_search[:-1] 
    if "recent_searches" not in session:
        session["recent_searches"] = []
    session["recent_searches"].append(recent_search + "\n")
    pieces_filtered = db.execute(query, params).fetchall()
    return render_template("pieces_filtered.html", pieces_filtered = pieces_filtered, user = user, 
                           recent_searches = session["recent_searches"])

# Delete car function, with which a user can delete a car he owns. It leads the user to a 
# "car deleted confirmation"
@app.route("/delete_car/<int:user_id>/<int:car_id>", methods = ["GET", "POST"])
def delete_car(user_id, car_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    db.execute("""DELETE FROM car WHERE car_id = ?;""", (car_id, ))
    db.commit()
    return render_template("car_deleted_successfully.html", user = user)

# Delete piece a user needs function, with which a user can delete a piece he's looking for. 
# It leads the user to a "piece deleted confirmation".
@app.route("/delete_piece_I_need/<int:user_id>/<int:piece_id>", methods = ["GET", "POST"])
def delete_piece_I_need(user_id, piece_id):
    db = get_db()
    user = db.execute("""SELECT * FROM user WHERE user_id = ?;""", (user_id, )).fetchone()
    db.execute("""DELETE FROM piece WHERE piece_id = ?;""", (piece_id, ))
    db.commit()
    db.execute("""DELETE FROM need WHERE piece_needed = ? AND wanter = ?;""", (piece_id, user_id, ))
    db.commit()
    return render_template("piece_you_need_deleted_successfully.html", user = user)

# Delete piece a user is selling function, with which a user can delete a piece he's looking for. It leads the user to a 
# "piece deleted confirmation".
@app.route("/delete_piece_I_sell/<int:user_id>/<int:piece_id>", methods = ["GET", "POST"])
def delete_piece_I_sell(user_id, piece_id):
    db = get_db()
    user = db.execute("""SELECT * FROM USER WHERE user_id = ?;""", (user_id, )).fetchone()
    db.execute("""DELETE FROM piece WHERE piece_id = ?;""", (piece_id, ))
    db.commit()
    return render_template("piece_you_sell_deleted_successfully.html", user = user)

# Car page, where a user can see the details of a specific car
@app.route("/car/<int:user_id>/<int:car_id>")
def car(user_id, car_id):
    db = get_db()
    car = db.execute("""SELECT * FROM car, user WHERE car_id = ? AND car.owner = user.user_id;""", (car_id, )).fetchone()
    user = db.execute("""SELECT * FROM USER WHERE user_id = ?;""", (user_id, )).fetchone()
    return render_template("car.html", car = car, user = user)

# Piece page, where a user can see the details of a specific piece
@app.route("/piece/<int:user_id>/<int:piece_id>")
def piece(user_id, piece_id):
    db = get_db()
    user = db.execute("""SELECT * FROM USER WHERE user_id = ?;""", (user_id, )).fetchone()
    piece = db.execute("""SELECT * FROM piece, user WHERE piece_id = ? AND piece.owner = user.user_id;""", (piece_id, )).fetchone()
    return render_template("piece.html", piece = piece, user = user)

# Log out function, with which a user can log out and clear his session.
# It leads the user to the landing page
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register_login"))
