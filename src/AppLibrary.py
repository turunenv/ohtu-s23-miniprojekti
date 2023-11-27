from stub_io import StubIO
from database_connection import get_db_connection
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService
from app import App


class AppLibrary:
    def __init__(self):
        self._io = StubIO()
        self._reference_repository = ReferenceRepository(get_db_connection())
        self._reference_service = ReferenceService(self._reference_repository)

        self._app = App(self._io, self._reference_service)

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
        self._reference_repository.delete_all_books()
        
    def run_application(self):
        self._app.run()
