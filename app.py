from flask import Flask, jsonify, request
from db import create_table, add_book, get_books, update_book, delete_book
from email_notify import send_new_book_email
from scrapper import calculate_total_stock_value
import threading
import time
import client  # Your client.py file with start_client()

app = Flask(__name__)
create_table()

# -------------------- API Endpoints --------------------

@app.route("/books", methods=["POST"])
def add_book_endpoint():
    data = request.json
    book_id = add_book(data)
    if book_id:
        send_new_book_email(data['title'], "swathimanjappa9@gmail.com")
        return jsonify({"id": book_id}), 201
    return jsonify({"error": "Could not add book"}), 500

@app.route("/books", methods=["GET"])
def get_books_endpoint():
    books = get_books()
    return jsonify({"books": books})

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book_endpoint(book_id):
    data = request.json
    updated = update_book(book_id, data)
    if updated:
        return jsonify({"message": f"Book with id {book_id} updated."}), 200
    return jsonify({"error": f"Update failed for id {book_id}."}), 400

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_endpoint(book_id):
    deleted = delete_book(book_id)
    if deleted:
        return jsonify({"message": f"Book with id {book_id} deleted."}), 200
    return jsonify({"error": f"No book found with id {book_id}."}), 404

@app.route("/stock_value", methods=["GET"])
def stock_value():
    total_val = calculate_total_stock_value()
    return jsonify({"total_stock_value": total_val})
# HOMEPAGE
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Library Management System (Flask Version)"})

# -------------------- Run Flask + Client --------------------

def run_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Wait a moment for the server to be ready
    time.sleep(1)

    # Start the CLI client (this runs in main thread)
    client.start_client()
