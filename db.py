import sqlite3
from logger import get_logger

logger = get_logger(__name__)

def get_db_conn():
    return sqlite3.connect("library.db", check_same_thread=False)

def create_table():
    try:
        with get_db_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Book (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    price REAL,
                    copies INTEGER
                )
                """
            )
        logger.info("Table Book ensured.")
    except Exception as e:
        logger.error(f"Table creation failed: {e}")

def add_book(book):
    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Book (title, price, copies) VALUES (?, ?, ?)",
                (book["title"], book["price"], book["copies"])
            )
            conn.commit()
            logger.info(f"Added book {book['title']}")
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Add book failed: {e}")
        return None

def update_book(book_id, updated_fields):
    """
    Update fields of a book identified by book_id.
    updated_fields: dict, e.g. {"title": "New Title", "price": 123.0}
    """
    try:
        if not updated_fields:
            logger.warning("No fields to update.")
            return 0

        set_clause = ", ".join([f"{field} = ?" for field in updated_fields])
        values = list(updated_fields.values())
        values.append(book_id)

        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE Book SET {set_clause} WHERE id = ?",
                values
            )
            conn.commit()
            logger.info(f"Updated book id={book_id} with {updated_fields}")
            return cursor.rowcount
    except Exception as e:
        logger.error(f"Update book failed: {e}")
        return None

def delete_book(book_id):
    """Delete a book by ID."""
    try:
        logger.debug(f"Attempting to delete book with id={book_id} (type: {type(book_id)})")
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Book WHERE id = ?", (book_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"No book found with id={book_id}")
            else:
                logger.info(f"Deleted book id={book_id}")
            return cursor.rowcount
    except Exception as e:
        logger.error(f"Delete book failed: {e}")
        return None

def get_books():
    """Retrieve all books."""
    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Book")
            books = cursor.fetchall()
            logger.info("Fetched all books")
            return books
    except Exception as e:
        logger.error(f"Get books failed: {e}")
        return []
