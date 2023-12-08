from pybtex.database import BibliographyData, Entry

class Reference:
    """Abstract superclass that the other references inherit from
    """

    def __init__(self, ref_type):
        self.ref_type = ref_type
        self.ref_key = None  # given in the subclasses

    def create_bib_string(self):
        bib_data = BibliographyData({
            self.ref_key: Entry(self.ref_type, [
                (field.lower(),
                 str(getattr(self, field.lower()))) for field in self.get_field_names()])
        })
        return bib_data.to_string('bibtex')

    # this gets overwritten by the subclasses
    def get_field_names(self):
        return []
