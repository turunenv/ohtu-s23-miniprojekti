from entities.book_reference import BookReference
from entities.article_reference import ArticleReference


class ReferenceService:
    def __init__(self, reference_repository):
        self.fields_from_type = {
            "book": ["ref_key", "author", "title", "year", "publisher", ],
            "article": ["ref_key", "author", "title", "journal", "year", "volume", "pages"]
        }
        self._reference_repository = reference_repository

    def get_fields_of_reference_type(self, reference_type):
        if not reference_type in self.fields_from_type:
            return []

        return self.fields_from_type[reference_type]

    def create_reference(self, content):
        match content["type"]:
            case "book":
                book = BookReference(
                    content["ref_key"],
                    content["author"],
                    content["title"],
                    content["year"],
                    content["publisher"]
                )

                return self._reference_repository.create_book(book)

            case "article":
                article = ArticleReference(
                    content["ref_key"],
                    content["author"],
                    content["title"],
                    content["journal"],
                    content["year"],
                    content["volume"],
                    content["pages"]
                )

                return self._reference_repository.create_article(article)


    def get_all(self):
        return self._reference_repository.get_all()

    def get_book_by_ref_key(self, ref_key):
        return self._reference_repository.get_book_by_ref_key(ref_key)

    def delete_book_by_ref_key(self, ref_key):
        return self._reference_repository.delete_book_by_ref_key(ref_key)

    def ref_key_taken(self, key):
        ref_list = map(lambda x: x.ref_key, self.get_all())
        return key in ref_list
