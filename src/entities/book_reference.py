class BookReference:
    """Class that describes a reference of type Book

        Mandatory arguments:
            -ref_key, author, title, year, publisher
        Optional arguments:
            -editor, volume, pages
    """

    def __init__(self, ref_key, author, title, year, publisher):
        self.ref_key = ref_key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher
        # self.editor = editor
        # self.volume = volume
        # self.pages = pages

    def get_field_names(self):

        list = ["REF_KEY", "AUTHOR", "TITLE", "YEAR", "PUBLISHER"]
        # LISÄTÄÄN VALINNAISET KENTÄT
        # list += ["EDITOR", "VOLUME", "PAGES"]

        return list

    # HAETAAN KENTTIEN PITUUDET TAULUKOSSA TULOSTUSTA VARTEN
    def get_field_lengths(self):
        return [10, 25, 35, 6, 15]

    def __str__(self):
        return (
            f"{self.ref_key:<10} {self.author:<25} {self.title:<35} {self.year:<6} {self.publisher:<15}"
        )
