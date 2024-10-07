from datetime import datetime


class Author:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
        self.books = set()

    def add_book(self, book):
        self.books.add(book)

    def __str__(self):
        return self.name


class Book:
    def __init__(self, isbn, title, author, year, copies, genre):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.available_copies = copies
        self.genre = genre

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.borrowed_books = []

    def borrow_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)

        else:
            print("You cant borrow the same book twice bro")
        pass

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
        else:
            print("This book is not borrowed by you")
        pass

    def get_borrowed_books(self):
        return self.borrowed_books
        pass


class LibraryManagementSystem:
    def __init__(self):
        self.books = {}  # Dictionary: ISBN -> Book object
        self.authors = {}  # Dictionary: name -> Author object
        self.customers = {}  # Dictionary: customerID -> Customer object
        self.genre_classification = {}  # Dictionary: Genre -> {set of ISBNs}
        self.waitlist = {}  # Dictionary: ISBN -> [list of customerIDs]

    def add_book(self, isbn, title, author_name, author_birth_year, year, copies, genre):
        if isbn in self.books:
            print("A book already exists with this isbn: %s")
            return

        if author_name not in self.authors:
            author = Author(author_name, author_birth_year)
            self.authors[author_name] = author
        else:
            author = self.authors[author_name]

        book = Book(isbn, title, author, year, copies, genre)
        self.books[isbn] = book
        author.add_book(book)

        if genre not in self.genre_classification:
            self.genre_classification[genre] = set()
        self.genre_classification[genre].add(isbn)

    def register_customer(self, name, email):
        customer_id = len(self.customers) + 1
        customer = Customer(customer_id, name, email)
        self.customers[customer_id] = customer

        print(f"Customer {name} registered with id number {customer_id}")
        return customer_id

    def borrow_book(self, isbn, customer_id):
        if isbn not in self.books:
            print("Book not found")

        if customer_id not in self.customers:
            print("Customer not found")

        book = self.books[isbn]
        customer = self.customers[customer_id]

        if book.available_copies > 0:
            book.available_copies -= 1
            customer.borrowed_books(book)

            print(f"Book '{book.title}' has been borrowed successfully")

        else:
            print(f"'{book.title}' is unavailable, you have been put on a waitlist")
            self.add_to_waitlist(isbn, customer_id)
        pass

    def return_book(self, isbn, customer_id):
        if isbn not in self.books:
            print("Book not found")
            return

        if customer_id not in self.customers:
            print("Customer not found")
            return

        book = self.books[isbn]
        customer = self.customers[customer_id]

        if book in customer.borrowed_books:
            customer.return_book(book)
            book.available_copies += 1
            print(f"Book '{book.title}' has been returned successfully")
        else:
            print("This book is not borrowed by you")

    def search_books(self, query):
        results = []
        for book in self.books.values():
            if query in book.title or query in book.author.name or query == book.isbn:
                results.append(book)
        return results

    def display_available_books(self):
        for book in self.books.values():
            if book.available_copies > 0:
                print(book)

    def display_customer_books(self, customer_id):
        if customer_id not in self.customers:
            print("Customer not found")
            return

        customer = self.customers[customer_id]
        for book in customer.borrowed_books:
            print(book)

    def recommend_books(self, customer_id):
        if customer_id not in self.customers:
            print("Customer not found")
            return

        customer = self.customers[customer_id]
        genres = {book.genre for book in customer.borrowed_books}
        recommendations = [book for book in self.books.values() if
        book.genre in genres and book not in customer.borrowed_books]
        return recommendations

    def add_to_waitlist(self, isbn, customer_id):
        if isbn not in self.books:
            print("Book not found")
            return

        if customer_id not in self.customers:
            print("Customer not found")
            return

        if isbn not in self.waitlist:
            self.waitlist[isbn] = []
        self.waitlist[isbn].append(customer_id)

    def check_late_returns(self, days_threshold=14):
        for customer in self.customers.values():
            for book in customer.borrowed_books:
                if (datetime.datetime.now() - book.borrow_date).days > days_threshold:
                    print(f"Customer {customer.name} has a late return: {book.title}")

    def run(self):
        while True:
            print("1. Add book")
            print("2. Register customer")
            print("3. Borrow book")
            print("4. Return book")
            print("5. Search books")
            print("6. Display available books")
            print("7. Display customer books")
            print("8. Recommend books")
            print("9. Add to waitlist")
            print("10. Check late returns")
            print("11. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                isbn = input("Enter ISBN: ")
                title = input("Enter title: ")
                author_name = input("Enter author name: ")
                author_birth_year = int(input("Enter author birth year: "))
                year = int(input("Enter book year: "))
                copies = int(input("Enter number of copies: "))
                genre = input("Enter genre: ")
                self.add_book(isbn, title, author_name, author_birth_year, year, copies, genre)
            elif choice == "2":
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                self.register_customer(name, email)
            elif choice == "3":
                isbn = input("Enter ISBN: ")
                customer_id = int(input("Enter customer ID: "))
                self.borrow_book(isbn, customer_id)
            elif choice == "4":
                isbn = input("Enter ISBN: ")
                customer_id = int(input("Enter customer ID: "))
                self.return_book(isbn, customer_id)
            elif choice == "5":
                query = input("Enter search query: ")
                results = self.search_books(query)
                for book in results:
                    print(book)
            elif choice == "6":
                self.display_available_books()
            elif choice == "7":
                customer_id = int(input("Enter customer ID: "))
                self.display_customer_books(customer_id)
            elif choice == "8":
                customer_id = int(input("Enter customer ID: "))
                recommendations = self.recommend_books(customer_id)
                for book in recommendations:
                    print(book)
            elif choice == "9":
                isbn = input("Enter ISBN: ")
                customer_id = int(input("Enter customer ID: "))
                self.add_to_waitlist(isbn, customer_id)
            elif choice == "10":
                days_threshold = int(input("Enter days threshold: "))
                self.check_late_returns(days_threshold)
            elif choice == "11":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.run()