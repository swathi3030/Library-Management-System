from flask import Flask, jsonify, request
from db import create_table, add_book, get_books, update_book, delete_book
from email_notify import send_new_book_email
from stock_value import calculate_total_stock_value

app = Flask(__name__)
create_table()

# CREATE
@app.route("/books", methods=["POST"])
def add_book_endpoint():
    data = request.json
    book_id = add_book(data)
    if book_id:
        send_new_book_email(data['title'], "swathimanjappa9.com")
        return jsonify({"id": book_id}), 201
    return jsonify({"error": "Could not add book"}), 500

# READ (All books)
@app.route("/books", methods=["GET"])
def get_books_endpoint():
    books = get_books()
    return jsonify({"books": books})

# UPDATE
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book_endpoint(book_id):
    data = request.json
    updated = update_book(book_id, data)
    if updated:
        return jsonify({"message": f"Book with id {book_id} updated."}), 200
    return jsonify({"error": f"Update failed for id {book_id}."}), 400

# DELETE
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_endpoint(book_id):
    deleted = delete_book(book_id)
    if deleted:
        return jsonify({"message": f"Book with id {book_id} deleted."}), 200
    return jsonify({"error": f"No book found with id {book_id}."}), 404

# STOCK VALUE
@app.route("/stock_value", methods=["GET"])
def stock_value():
    total_val = calculate_total_stock_value()
    return jsonify({"total_stock_value": total_val})

# MAIN
if __name__ == "__main__":
    app.run(debug=True)
