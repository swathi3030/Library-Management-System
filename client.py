import requests

BASE_URL = "http://127.0.0.1:5000"

def show_menu():
    print("\n========= Book Store Menu =========")
    print("1. Add a new book")
    print("2. View all books")
    print("3. Update a book")
    print("4. Delete a book")
    print("5. Calculate total stock value")
    print("6. Exit")
    print("===================================")

def add_book():
    try:
        title = input("Enter book title: ")
        price = float(input("Enter price: "))
        copies = int(input("Enter number of copies in stock: "))

        data = {
            "title": title,
            "price": price,
            "copies": copies
        }

        response = requests.post(f"{BASE_URL}/books", json=data)
        if response.status_code == 201:
            print(f"✅ Book added successfully with ID: {response.json()['id']}")
        else:
            print("❌ Failed to add book. Server response:", response.text)
    except Exception as e:
        print("❌ Error:", str(e))

def view_books():
    try:
        response = requests.get(f"{BASE_URL}/books")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:", data)  # Add this line for debugging
            
            books = data.get("books", [])
            if books:
               pass
            else:
                print("📚 No books found.")
        else:
            print("❌ Failed to fetch books. Server response:", response.text)
    except Exception as e:
        print("❌ Error:", str(e))


def update_book():
    try:
        book_id = int(input("Enter ID of the book to update: "))
        title = input("Enter new title: ")
        price = float(input("Enter new price: "))
        copies = int(input("Enter new number of copies: "))

        data = {
            "title": title,
            "price": price,
            "copies": copies
        }

        response = requests.put(f"{BASE_URL}/books/{book_id}", json=data)
        if response.status_code == 200:
            print("✅ Book updated successfully.")
        else:
            print("❌ Failed to update book. Server response:", response.text)
    except Exception as e:
        print("❌ Error:", str(e))

def delete_book():
    try:
        book_id = int(input("Enter ID of the book to delete: "))
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        if response.status_code == 200:
            print("✅ Book deleted successfully.")
        else:
            print("❌ Failed to delete book. Server response:", response.text)
    except Exception as e:
        print("❌ Error:", str(e))

def get_stock_value():
    try:
        response = requests.get(f"{BASE_URL}/stock_value")
        if response.status_code == 200:
            value = response.json().get("total_stock_value", 0)
            print(f"💰 Total Stock Value: ₹{value}")
        else:
            print("❌ Failed to calculate stock value. Server response:", response.text)
    except Exception as e:
        print("❌ Error:", str(e))

def start_client():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            update_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            get_stock_value()
        elif choice == '6':
            print("👋 Exiting the application. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    start_client()
