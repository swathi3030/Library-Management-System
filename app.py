"""
app.py - Main Flask application for the Library Management System.

This application provides a RESTful API to manage a collection of books.
Features include:
- Adding, retrieving, updating, and deleting books
- Calculating the total stock value
- Sending email notifications on book addition
- Running a CLI client alongside the Flask server

Modules used:
- db.py: Handles database operations
- email_notify.py: Sends email alerts
- scrapper.py: Calculates stock value
- client.py: CLI interface
"""

from flask import Flask, jsonify, request
from db import create_table, add_book, get_books, update_book, delete_book
from email_notify import send_new_book_email
from scrapper import calculate_total_stock_value
import threading
import client  # CLI client script with start_client()

app = Flask(__name__)
create_table()

# -------------------- API Endpoints --------------------

@app.route("/books", methods=["POST"])
def add_book_endpoint():
    """
    Add a new book to the library database.

    Request JSON:
    {
        "title": "Book Title",
        "price": 100,
        "quantity": 5
    }

    Sends an email notification upon successful addition.

    Returns:
        JSON response with the book ID and HTTP 201 if successful,
        or an error message with HTTP 500 if the addition fails.
    """
    data = request.json
    book_id = add_book(data)
    if book_id:
        send_new_book_email(data['title'], "swathimanjappa9@gmail.com")
        return jsonify({"id": book_id}), 201
    return jsonify({"error": "Could not add book"}), 500

@app.route("/books", methods=["GET"])
def get_books_endpoint():
    """
    Retrieve all books from the library.

    Returns:
        JSON response containing a list of all books.
    """
    books = get_books()
    return jsonify({"books": books})

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book_endpoint(book_id):
    """
    Update an existing book by its ID.

    Request JSON:
    {
        "title": "Updated Title",
        "price": 120,
        "quantity": 3
    }

    Args:
        book_id (int): ID of the book to update.

    Returns:
        JSON response with a success message and HTTP 200 if updated,
        or an error message with HTTP 400 if the update fails.
    """
    data = request.json
    updated = update_book(book_id, data)
    if updated:
        return jsonify({"message": f"Book with id {book_id} updated."}), 200
    return jsonify({"error": f"Update failed for id {book_id}."}), 400

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_endpoint(book_id):
    """
    Delete a book from the library by its ID.

    Args:
        book_id (int): ID of the book to delete.

    Returns:
        JSON response with a success message and HTTP 200 if deleted,
        or an error message with HTTP 404 if the book was not found.
    """
    deleted = delete_book(book_id)
    if deleted:
        return jsonify({"message": f"Book with id {book_id} deleted."}), 200
    return jsonify({"error": f"No book found with id {book_id}."}), 404

@app.route("/stock_value", methods=["GET"])
def stock_value():
    """
    Calculate the total stock value of all books in the library.

    Returns:
        JSON response with the total stock value.
    """
    total_val = calculate_total_stock_value()
    return jsonify({"total_stock_value": total_val})

@app.route("/", methods=["GET"])
def home():
    """
    Home route for the Library Management System API.

    Returns:
        JSON welcome message.
    """
    return jsonify({"message": "Welcome to the Library Management System (Flask Version)"})


# -------------------- Run Flask + Client --------------------

def run_flask():
    """
    Start the Flask application without the debug reloader.

    This runs in a background thread to allow the CLI client
    to run concurrently in the main thread.
    """
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the CLI client (this runs in main thread)
    client.start_client()
