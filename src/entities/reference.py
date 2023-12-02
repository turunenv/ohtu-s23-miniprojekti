class Reference:
    """Abstract superclass that the other references inherit from
    """
    def __init__(self, ref_type):
        self.ref_type = ref_type
        self.ref_key = None # given in the subclasses

    def create_bib_string(self):
        bibtex_field_indentation = " " * 4

        field_names_capitalized = self.get_field_names()

        #first line of a BibTex reference
        #format: @<ref_type>{<UniqueRefKey>,
        bib_str = f"@{self.ref_type}{{{self.ref_key},\n"

        #reference body consists of key-value pairs
        #format: <field_name> = <field_value>
        for i, field in enumerate(field_names_capitalized):
            field = field.lower()
            value = getattr(self, field)

            next_line = f"{bibtex_field_indentation}{field} = \"{value}\""

            #add the comma, unless it is the last field
            if i < len(field_names_capitalized) - 1:
                next_line += ","


            bib_str += f"{next_line}\n"

        #add closing curly brace and ending newline
        bib_str += "}}\n"

        return bib_str

    # this gets overwritten by the subclasses
    def get_field_names(self):
        return []
    