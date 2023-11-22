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
        cursor.execute(
            "INSERT INTO book_references (ref_key, author, title, year, publisher) VALUES (?, ?)",
            (book.ref_key, book.author, book.title, book.year, book.publisher)
        )

        self._connection.commit()


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
            books_list.append(BookReference(book[0], book[1], book[2], book[3], book[4]))

        return books_list
