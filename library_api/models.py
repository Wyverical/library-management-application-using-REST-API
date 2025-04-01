# library_api/models.py
from . import db
from datetime import datetime
from passlib.hash import bcrypt

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = bcrypt.hash(password)
        self.role = role

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(50), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(120))
    quantity = db.Column(db.Integer, default=1)

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    date_borrowed = db.Column(db.DateTime, default=datetime.utcnow)
    date_returned = db.Column(db.DateTime, nullable=True)
