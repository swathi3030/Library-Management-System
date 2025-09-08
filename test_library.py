import unittest
from db import create_table, add_book, get_books, delete_book

class TestLibraryDB(unittest.TestCase):
    def setUp(self):
        # Ensure table exists
        create_table()

    def test_add_book(self):
        # Prepare test data
        test_book = {
            "title": "Test Driven Development",
            "price": 39.99,
            "copies": 3
        }

        # Call add_book
        book_id = add_book(test_book)
        self.assertIsNotNone(book_id, "Book ID should not be None after insert")

        # Fetch books and check if the new one exists
        books = get_books()
        added_book = next((book for book in books if book["id"] == book_id), None)

        self.assertIsNotNone(added_book, "Added book not found in DB")
        self.assertEqual(added_book["title"], test_book["title"])
        self.assertEqual(added_book["price"], test_book["price"])
        self.assertEqual(added_book["copies"], test_book["copies"])

        # Clean up
        delete_book(book_id)

    def tearDown(self):
        # Any cleanup if needed in the future
        pass

if __name__ == "__main__":
    unittest.main()
