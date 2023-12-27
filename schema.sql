DROP TABLE IF EXISTS user;

CREATE TABLE user
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    mail TEXT NOT NULL,
    phone TEXT NOT NULL
);


INSERT INTO user(username, password_hash, mail, phone)
VALUES
    ('Connor McGregor', 'pbkdf2:sha256:260000$CJMluKeLDlJj1d5I$6853957e3a4688930ce611334d1febdc488982c5bedbe46cefbc21f0560a8bfb', 'cMcGregor@gmail.com', '54 025 3654'),
    ('Michael OHalloran', 'pbkdf2:sha256:260000$Am1z6BAunLhetSOj$2c8114efdaf54abc9b1cee70d7445fcc3ae76182f606a63a0c8c32f4ec8726b4', 'mOHalloran@gmail.com', '24 358 7412'),
    ('Bennet Riordan', 'pbkdf2:sha256:260000$dE0fpnXOnKF4ZVEX$1d167ce5496f7b73de56e908f22caf366ec62ea32aba474f39f393b7fab0c420', 'bRiordan@gmail.com', '68 235 1414'),
    ('Fintan Lukes', 'pbkdf2:sha256:260000$kLgctXnvaRLRjUD3$754508bdeb7975bdd7b3f640c6f5b8fa721469f6d6f7474ade35035860aeba84', 'fLukes@gmail.com', '36 220 0147'),
    ('Conor Murphy', 'pbkdf2:sha256:260000$IvBcEYWvAm9PUdR7$1aa0d18dbb36b518888f51bd117f7113613faab1bec73715a4543cfab5d1b75a', 'cMurphy@gmail.com', '66 588 252'),
    ('Daniel Steve', 'pbkdf2:sha256:260000$79Z8zulkQd4Rnf30$a0f58026370b19dc7d3ce27ec2e1f8c4ed5ec704cf205e62b063e15a5dca8ec8', 'dSteve@gmail.com', '00 353 699')
;

DROP TABLE IF EXISTS car;

CREATE TABLE car
(
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model_set TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    owner INTEGER,
    image_URL TEXT,
    FOREIGN KEY (owner) REFERENCES user(user_id)
);


INSERT INTO car(brand, model_set, model, year, owner, image_URL)
VALUES
    ('BMW', 'iX', 'iX6', 2015, 1, 'BMW IX6.jpg'),
    ('Mercedes', 'Class A', 'A45', 2012, 1, 'MERCEDES A45.jpg'),
    ('Audi', 'A1-A4', 'A1', 2016, 1, 'AUDI A1.jpg'),
    ('Seat', 'Leon', 'Leon Cupra',2021, 2, 'SEAT LEON CUPRA.jpg'),
    ('BMW', 'E90-E93', 'E90', 1995, 3, 'BMW E90.jpg'),
    ('Audi', 'TT', 'TT S', 2019, 4, 'AUDI TT.jpg'),
    ('Mercedes', 'Class B', '4matic', 2018, 5, 'MERCEDES 4MATIC.jpg'),
    ('Mazda', 'RX', 'RX7', 2012, 6, 'MAZDA RX7.jpg'),
    ('Dodge', 'Challenger', 'SRT', 2012, 6, 'DODGE SRT.jpg')
;

DROP TABLE IF EXISTS piece;

CREATE TABLE piece
(
    piece_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    car_brand TEXT NOT NULL,
    car_model_set TEXT NOT NULL,
    car_model TEXT NOT NULL,
    car_year INTEGER NOT NULL,
    piece_year INTEGER NOT NULL,
    owner INTEGER,
    price REAL,
    image_URL TEXT,
    FOREIGN KEY (car_brand) REFERENCES car(brand),
    FOREIGN KEY (car_model_set) REFERENCES car(model_set),
    FOREIGN KEY (car_model) REFERENCES car(model),
    FOREIGN KEY (owner) REFERENCES user(user_id)
);

INSERT INTO piece(name, car_brand, car_model_set, car_model, car_year, piece_year, owner, price, image_URL)
VALUES
  ('Rim', 'BMW', 'E90-E93', 'E90', 2014, 2013, 1, 300, 'BMW rim.png'),
  ('Grilles', 'Audi', 'A1-A4', 'A2', 2007, 2018, 2, 50, 'AUDI grilles.jpg'),
  ('Grilles', 'BMW', 'E30-E90', 'E90', 2015, 3, 2018, 65, 'BMW grilles.jpg'),
  ('Rear wing', 'Ford', 'Mustang', 'GT', 2011, 2011, 4, 215, 'FORD rear wing.jpg'),
  ('Suspension', 'Mercedes', 'Class C', 'CLC', 2020, 2021, 5, 80, 'MERCEDES suspension.jpg'),
  ('Rear wing', 'BMW', 'E46', 'E46', 2016, 2017, 6, 30, 'BMW rear wing.jpg'),
  ('Splitter', 'Audi', 'A1-A4', 'A1', 2016, 2016, 2, 200, 'AUDI splitter.jpg')
;

DROP TABLE IF EXISTS need;

CREATE TABLE need
(
    need_id INTEGER PRIMARY KEY AUTOINCREMENT,
    piece_needed INTEGER NOT NULL,
    wanter INTEGER NOT NULL,
    FOREIGN KEY (piece_needed) REFERENCES piece(piece_id),
    FOREIGN KEY (wanter) REFERENCES user(user_id)
);


INSERT INTO need(piece_needed, wanter)
VALUES
  (1, 1),
  (2, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 3),
  (4, 5),
  (3, 4)
;