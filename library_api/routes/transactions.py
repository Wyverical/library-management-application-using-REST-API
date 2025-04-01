# library_api/routes/transactions.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from library_api.models import Transaction, Book, User
from library_api import db
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/borrow", methods=["POST"])
@jwt_required()
def borrow_book():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400
    book_id = data.get("book_id")
    if not book_id:
        return jsonify({"msg": "book_id is required"}), 400
    book = Book.query.get_or_404(book_id)
    if book.quantity < 1:
        return jsonify({"msg": "Book not available"}), 400
    book.quantity -= 1
    transaction = Transaction(user_id=user.id, book_id=book.id)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"msg": f"Book '{book.title}' borrowed"}), 200

@transactions_bp.route("/return", methods=["POST"])
@jwt_required()
def return_book():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400
    book_id = data.get("book_id")
    if not book_id:
        return jsonify({"msg": "book_id is required"}), 400
    transaction = Transaction.query.filter_by(user_id=user.id, book_id=book_id, date_returned=None).first()
    if not transaction:
        return jsonify({"msg": "No active borrow transaction found"}), 400
    transaction.date_returned = datetime.utcnow()
    book = Book.query.get(book_id)
    book.quantity += 1
    db.session.commit()
    return jsonify({"msg": f"Book '{book.title}' returned"}), 200
