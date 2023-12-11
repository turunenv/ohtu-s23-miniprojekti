from console_io import ConsoleIO
from app import App
from database_connection import get_db_connection
from services.reference_service import ReferenceService
from repositories.reference_repository import ReferenceRepository
from file_io import FileIO
from bibtex_writer import BibTexWriter
from services.doi_service import DOIService #pylint: disable=ungrouped-imports


def main():
    console_io = ConsoleIO()
    connection = get_db_connection()
    reference_repository = ReferenceRepository(connection)
    reference_service = ReferenceService(reference_repository)
    bibtex_writer = BibTexWriter(FileIO())
    doi_service = DOIService(console_io)
    app = App(console_io, reference_service, bibtex_writer, doi_service)

    app.run()


if __name__ == "__main__":
    main()
