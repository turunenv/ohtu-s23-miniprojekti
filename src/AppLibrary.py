from stub_io import StubIO
from database_connection import get_db_connection
from file_io import FileIO
from bibtex_writer import BibTexWriter
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService
from app import App
import os


class AppLibrary:
    def __init__(self):
        self._io = StubIO()
        self._file_io = FileIO()
        self._bib = BibTexWriter(self._file_io)
        self._reference_repository = ReferenceRepository(get_db_connection())
        self._reference_service = ReferenceService(self._reference_repository)

        self._app = App(self._io, self._reference_service, self._bib)

    def input(self, value):
        self._io.add_input(value)

    def output_should_contain(self, value):
        outputs = self._io.outputs

        value_included = filter(
            lambda x: value in x, outputs
        )

        # check if any element in the outputs list contained given value
        if not len(list(value_included)) > 0:
            raise AssertionError(
                    f"expected value '{value}' not found in the outputs: {str(outputs)}"
                )

    def list_all_references(self):
        self._app.list_references()

    def clear_database(self):
        self._reference_repository.delete_all_test_references()

    def run_application(self):
        self._app.run()

    def output_should_not_contain(self, value):
        outputs = self._io.outputs

        if value in outputs:
            raise AssertionError(f"Output \"{value}\" is in {str(outputs)}")
        
    def delete_test_file(self, file):
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"File '{file}' deleted successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"File '{file}' not found.")

