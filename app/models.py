from app import db

#This is creating the database model. It stores the id, details on the book and links with the Account database
#All of these fields are assigned as nullable=False meaning they all have to have entries
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    #Initializes the fields in the database
    def __init__(self, name, author, status, account_id):
        self.name = name
        self.author = author
        self.status = status
        self.account_id = account_id

#This is creating the database model. It stores the id, details on the reviews and links with the Account database
#All of these fields are assigned as nullable=False meaning they all have to have entries
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    #Initializes the fields in the database
    def __init__(self, title, book_name, author, description, poster_id):
        self.title = title
        self.book_name = book_name
        self.author = author
        self.description = description
        self.poster_id = poster_id

#This is creating the database model. It stores the id, details on the user and links with the Revies and Books database
#All of these fields are assigned as nullable=False meaning they all have to have entries
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    books = db.relationship('Books', backref='account_book')
    reviews = db.relationship('Reviews', backref='account_rev')

    #Initializes the fields in the database
    def __init__(self, username, password, first_name, last_name, number, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.number = number
        self.email = email
