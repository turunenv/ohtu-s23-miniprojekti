from entities.book_reference import BookReference
from repositories.reference_repository import ReferenceRepository

class ReferenceService:
    def __init__(self, reference_repository):
        self.fields_from_type = {
            "book": ["ref_key", "author", "title", "year", "publisher", ]
        }
        self._reference_repository = reference_repository

    def get_fields_of_reference_type(self, type):
        if not type in self.fields_from_type:
            return []
        
        return self.fields_from_type[type]
    
    def create_reference(self, content):
        match content.type:
            case "book":
                book = BookReference(content)

                self._reference_repository.create_book(book)

    def get_all(self):
        return self._reference_repository.get_all()
