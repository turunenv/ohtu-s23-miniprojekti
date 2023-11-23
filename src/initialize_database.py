from database_connection import get_db_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists book_references
    """)

    connection.commit()

def create_tables(connection):
    """
    Here we create the tables for all the supported reference types
    """

    cursor = connection.cursor()

    # create the book_references table
    cursor.execute("""
        create table book_references (
            ref_key text primary key,
            author text,
            title text,
            year integer,
            publisher text
        )
    """)

    connection.commit()

def initialize_database():
    connection = get_db_connection()

    drop_tables(connection)
    create_tables(connection)
