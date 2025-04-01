# library_api/routes/books.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from library_api.models import Book
from library_api import db
from library_api.utils import is_admin

books_bp = Blueprint("books", __name__)

@books_bp.route("", methods=["POST"])
@jwt_required()
def create_book():
    if not is_admin():
        return jsonify({"msg": "Admin privilege required"}), 403
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400
    title = data.get("title")
    author = data.get("author")
    isbn = data.get("isbn")
    published_year = data.get("published_year")
    category = data.get("category", "")
    quantity = data.get("quantity", 1)
    if not all([title, author, isbn, published_year]):
        return jsonify({"msg": "Missing required book fields"}), 400
    new_book = Book(
        title=title,
        author=author,
        isbn=isbn,
        published_year=published_year,
        category=category,
        quantity=quantity,
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"msg": f"Book '{title}' created"}), 201

@books_bp.route("", methods=["GET"])
@jwt_required()
def list_books():
    title = request.args.get("title")
    author = request.args.get("author")
    isbn = request.args.get("isbn")
    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if isbn:
        query = query.filter(Book.isbn.ilike(f"%{isbn}%"))
    books = query.all()
    output = []
    for book in books:
        output.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "published_year": book.published_year,
            "category": book.category,
            "quantity": book.quantity,
        })
    return jsonify(output), 200

@books_bp.route("/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    if not is_admin():
        return jsonify({"msg": "Admin privilege required"}), 403
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.isbn = data.get("isbn", book.isbn)
    book.published_year = data.get("published_year", book.published_year)
    book.category = data.get("category", book.category)
    book.quantity = data.get("quantity", book.quantity)
    db.session.commit()
    return jsonify({"msg": f"Book '{book_id}' updated"}), 200

@books_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    if not is_admin():
        return jsonify({"msg": "Admin privilege required"}), 403
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"msg": f"Book '{book_id}' deleted"}), 200
