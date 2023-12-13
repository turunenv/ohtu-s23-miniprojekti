from .reference import Reference


class InProceedingsReference(Reference):
    """Class that describes a reference of type In Proceedings

        Mandatory arguments:
            -ref_key, author, title, booktitle, year
    """

    def __init__(self, ref_key, author, title, booktitle, year):
        super().__init__("inproceedings")

        self.ref_key = ref_key
        self.author = author
        self.title = title
        self.booktitle = booktitle
        self.year = year
        self.type = "inproceedings"

    def get_field_names(self):
        field_list = ["REF_KEY", "AUTHOR", "TITLE", "BOOKTITLE", "YEAR"]

        return field_list

    # HAETAAN KENTTIEN PITUUDET TAULUKOSSA TULOSTUSTA VARTEN
    def get_field_lengths(self):
        return [10, 25, 25, 25, 6]

    def __str__(self):
        string = f"{self.ref_key[:10]:<10} {self.author[:25]:<25} "
        string += f"{self.title[:25]:<25} {self.booktitle[:25]:<25} {self.year:<6} "

        newline = len(self.author) > 25 or len(self.title) > 25
        if len(self.booktitle) > 25 or len(self.ref_key) > 10:
            newline = True
        if newline:
            string += (
                f"\n{self.ref_key[10:20]:<10} {self.author[25:50]:<25}")
            string += (
                f" {self.title[25:50]:<25} {self.booktitle[25:50]:<25}")
        return string
