import sqlite3
from entities.book_reference import BookReference
from entities.article_reference import ArticleReference
from entities.inproceedings_reference import InProceedingsReference


class ReferenceRepository:
    """Class that handles all database actions

        Arguments:
            -connection: database connection
    """

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

    def create_article(self, article):
        """Saves article reference into database.

        Args:
            article (_type_): ArticleReference
        """

        cursor = self._connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO article_references
                (ref_key, author, title, journal, year, volume, pages)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (article.ref_key, article.author, article.title,
                 article.journal, article.year, article.volume,
                 article.pages)
            )

            self._connection.commit()
        except (AttributeError, sqlite3.Error) as e:
            # Handle exceptions
            print(e)
            return False
        finally:
            # Close the cursor
            cursor.close()

        return True

    def create_inproceedings(self, inproceedings):
        """Saves inproceedings reference into database.

        Args:
            article (_type_): InProceedingsReference
        """

        cursor = self._connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO inproceedings_references
                (ref_key, author, title, booktitle, year)
                VALUES (?, ?, ?, ?, ?)""",
                (inproceedings.ref_key, inproceedings.author, inproceedings.title,
                 inproceedings.booktitle, inproceedings.year)
            )

            self._connection.commit()
        except (AttributeError, sqlite3.Error) as e:
            # Handle exceptions
            print(e)
            return False
        finally:
            # Close the cursor
            cursor.close()

        return True

    def create_tag(self, tag_name):
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO reference_tags (tag_name) VALUES (?)""",
                (tag_name,)
            )
            self._connection.commit()
        except (AttributeError, sqlite3.Error) as e:
            # Handle exceptions
            print(e)
            return False
        finally:
            # Close the cursor
            cursor.close()

        return True

    def create_tag_relation(self, tag_key, ref_key):
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """INSERT INTO tag_relations (tag_id, ref_key) VALUES (?, ?)""",
                (tag_key, ref_key)
            )

            self._connection.commit()
        except (AttributeError, sqlite3.Error) as e:
            # Handle exceptions
            print(e)
            return False
        finally:
            # Close the cursor
            cursor.close()

        return True

    def get_all(self):
        """Finds all references from database.

        Returns:
            Returns a list of references
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM book_references")

        books = cursor.fetchall()

        reference_list = []

        for book in books:
            reference_list.append(BookReference(
                book[0], book[1], book[2], book[3], book[4]))

        cursor.execute("SELECT * FROM article_references")

        articles = cursor.fetchall()

        for article in articles:
            reference_list.append(ArticleReference(
                article[0], article[1], article[2], article[3],
                article[4], article[5], article[6]))

        cursor.execute("SELECT * FROM inproceedings_references")

        inproceedings = cursor.fetchall()

        for inproc in inproceedings:
            reference_list.append(InProceedingsReference(inproc[0], inproc[1],
                                          inproc[2], inproc[3], inproc[4]))


        return reference_list

    def get_reference_by_ref_key(self, ref_key):
        """Finds a reference by ref_key from the database.

        Returns:
            Returns a single BookReference or ArticleReference
            or None if not found.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM book_references WHERE ref_key = ?", (ref_key,))

        book = cursor.fetchone()

        if book:
            # If a row is found, create a BookReference object
            return BookReference(book[0], book[1], book[2], book[3], book[4])

        cursor.execute(
            "SELECT * FROM article_references WHERE ref_key = ?", (ref_key,))

        article = cursor.fetchone()

        if article:
            # If a row is found, create an ArticleReference object
            return ArticleReference(article[0], article[1], article[2],
                                    article[3], article[4], article[5],
                                    article[6])

        cursor.execute(
            "SELECT * FROM inproceedings_references WHERE ref_key = ?", (ref_key,))

        inproceedings = cursor.fetchone()

        if inproceedings:
            return InProceedingsReference(inproceedings[0], inproceedings[1],
                                          inproceedings[2], inproceedings[3],
                                          inproceedings[4])

        # If no row is found, return None
        return None

    def delete_reference_by_ref_key(self, ref_key):
        """Deletes a reference by ref_key from the database.

        Returns:
            Returns True if the book was successfully deleted, False otherwise.
        """
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM book_references WHERE ref_key = ?", (ref_key,))
            self._connection.commit()

            # If nothing was deleted from book_references, try article_references
            if cursor.rowcount == 0:
                cursor.execute(
                    "DELETE FROM article_references WHERE ref_key = ?", (ref_key,))
                self._connection.commit()

            # try inproceedings last
            if cursor.rowcount == 0:
                cursor.execute(
                    "DELETE FROM inproceedings_references WHERE ref_key = ?", (ref_key,))
                self._connection.commit()

            #save amount of deleted rows because teg_relations will change it
            deleted_rows = cursor.rowcount

            # If a reference was deleted, delete that references tag relations
            if cursor.rowcount > 0:
                cursor.execute(
                    "DELETE FROM tag_relations WHERE ref_key = ?", (ref_key,))
                self._connection.commit()

            # Check if any rows were affected (i.e., if the reference was found and deleted)
            return deleted_rows > 0

        except (AttributeError, sqlite3.Error) as e:
            print(e)
            return False
        finally:
            cursor.close()

    def delete_all_test_references(self):
        cursor = self._connection.cursor()

        cursor.execute(
            "DELETE FROM book_references WHERE ref_key LIKE 'test%'")
        cursor.execute(
            "DELETE FROM article_references WHERE ref_key LIKE 'test%'")
        cursor.execute(
            "DELETE FROM inproceedings_references WHERE ref_key LIKE 'test%'")
        cursor.execute(
            "DELETE FROM tag_relations WHERE ref_key LIKE 'test%'")
        self._connection.commit()

    def delete_all_references(self):
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM book_references")
        cursor.execute("DELETE FROM article_references")
        cursor.execute("DELETE FROM inproceedings_references")
        cursor.execute("DELETE FROM tag_relations")

        self._connection.commit()

    def get_tag_id(self, tag_name):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM reference_tags WHERE tag_name = ?", (tag_name,))

        tag = cursor.fetchone()
        if tag:
            return tag[0]
        return None

    def get_tagged(self, tag_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM book_references B, tag_relations T "
            "WHERE T.tag_id = ? AND B.ref_key = T.ref_key",
            (tag_id,))

        books = cursor.fetchall()

        reference_list = []

        for book in books:
            reference_list.append(BookReference(
                book[0], book[1], book[2], book[3], book[4]))

        cursor.execute(
            "SELECT * FROM article_references A, tag_relations T "
            "WHERE T.tag_id = ? AND A.ref_key = T.ref_key",
            (tag_id,)
        )


        articles = cursor.fetchall()

        for article in articles:
            reference_list.append(ArticleReference(
                article[0], article[1], article[2], article[3],
                article[4], article[5], article[6]))

        cursor.execute(
            "SELECT * FROM inproceedings_references A, tag_relations T "
            "WHERE T.tag_id = ? AND A.ref_key = T.ref_key",
            (tag_id,)
        )

        inproceedings = cursor.fetchall()

        for inproc in inproceedings:
            reference_list.append(InProceedingsReference(
                inproc[0], inproc[1],
                inproc[2], inproc[3],
                inproc[4]
            ))

        return reference_list

    def get_tags(self):
        """Finds all tags from database.

        Returns:
            Returns tags and the count of connected references
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT T.tag_name, COUNT(R.ref_key) "
            "FROM reference_tags T, tag_relations R "
            "WHERE T.id = R.tag_id "
            "GROUP BY T.tag_name"
            )
        tags = cursor.fetchall()
        tag_list = []
        for tag in tags:
            if tag[0] is not None:
                tag_list.append({'name':tag[0], 'count':tag[1]})
        return tag_list
