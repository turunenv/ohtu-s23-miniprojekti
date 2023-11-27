from stub_io import StubIO
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService
from app import App


class AppLibrary:
    def __init__(self):
        self._io = StubIO()
        self._reference_repository = ReferenceRepository()
        self._reference_service = ReferenceService()

        self._app = App(self._reference_service, self._io)
