from entities.book_reference import BookReference

class ReferenceService:
    def __init__(self):
        self.fields_from_type = {
            "book": ["ref_key", "author", "title", "year", "publisher", ]
        }

    def get_fields_of_reference_type(self, type):
        if not type in self.fields_from_type:
            return []
        
        return self.fields_from_type[type]
    
    def create_reference(self, content):
        pass
