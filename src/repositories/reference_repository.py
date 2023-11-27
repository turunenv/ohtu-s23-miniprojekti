import sqlite3
from entities.book_reference import BookReference


class ReferenceRepository:

    def __init__(self, connection):
        self._connection = connection

    def create_book(self, book):
        """Saves book reference into database.

        Args:
            book (_type_): BookReference
        """
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO book_references"
                "(ref_key, author, title, year, publisher) VALUES (?, ?, ?, ?, ?)",
                (book.ref_key, book.author, book.title, book.year, book.publisher)
            )

            self._connection.commit()
        except (AttributeError, sqlite3.Error) as e:
            print(e)
            return False

        return True

    def get_all(self):
        """Finds all references from database.

        Returns:
            Returns a list of BookReferences
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * from book_references")

        books = cursor.fetchall()

        books_list = []

        for book in books:
            books_list.append(BookReference(
                book[0], book[1], book[2], book[3], book[4]))

        return books_list

    def get_book_by_ref_key(self, ref_key):
        """Finds a reference by ref_key from the database. Works only with books atm

        Returns:
            Returns a single BookReference or None if not found.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM book_references WHERE ref_key = ?", (ref_key,))

        book = cursor.fetchone()

        if book:
            # If a row is found, create a BookReference object
            return BookReference(book[0], book[1], book[2], book[3], book[4])

        # If no row is found, return None
        return None

    def delete_book_by_ref_key(self, ref_key):
        """Deletes a book by ref_key from the database.

        Returns:
            Returns True if the book was successfully deleted, False otherwise.
        """
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM book_references WHERE ref_key = ?", (ref_key,))
            self._connection.commit()

            # Check if any rows were affected (i.e., if the book was found and deleted)
            return cursor.rowcount > 0

        except (AttributeError, sqlite3.Error) as e:
            # Handle exceptions (e.g., database error)
            print(e)
            return False
        finally:
            # Close the cursor
            cursor.close()

    def delete_all_books(self):
        cursor = self._connection.cursor()

        cursor.execute("DELETE from book_references")
        self._connection.commit()
