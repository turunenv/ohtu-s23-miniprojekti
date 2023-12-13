from .reference import Reference


class ArticleReference(Reference):
    """Class that describes an article type reference

        Arguments: 
            -ref_key, author, title, journal, year,
            volume, pages
    """

    def __init__(self, ref_key, author, title, journal, year, volume, pages):  # pylint: disable=too-many-arguments
        super().__init__("article")

        self.ref_key = ref_key
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages
        self.type = "article"

    def get_field_names(self):
        field_list = ["REF_KEY", "AUTHOR", "TITLE",
                      "JOURNAL", "YEAR", "VOLUME", "PAGES"]

        return field_list

    def get_field_lengths(self):
        return [10, 25, 25, 25, 6, 6, 6]

    def __str__(self):
        string = f"{self.ref_key:<10} {self.author[:25]:<25} {self.title[:25]:<25} "
        string += f"{self.journal:<25} {self.year:<6} {self.volume:<6} {self.pages:<8}"
        if len(self.author) > 25 or len(self.title) > 25 or len(self.ref_key) > 10:
            string += f"\n{self.ref_key[10:20]:<10} {self.author[25:50]:<25} {self.title[25:50]:<25}"

        return string
