from entities.book_reference import BookReference
from entities.article_reference import ArticleReference
from entities.inproceedings_reference import InProceedingsReference


class ReferenceService:
    def __init__(self, reference_repository):
        self.fields_from_type = {
            "book": ["ref_key", "author", "title", "year", "publisher", ],
            "article": ["ref_key", "author", "title", "journal", "year", "volume", "pages"],
            "inproceedings": ["ref_key", "author", "title", "booktitle", "year"]
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

            case "inproceedings":
                inproceedings = InProceedingsReference(
                    content["ref_key"],
                    content["author"],
                    content["title"],
                    content["booktitle"],
                    content["year"],
                )

                return self._reference_repository.create_inproceedings(inproceedings)


    def get_all(self):
        return self._reference_repository.get_all()

    def get_reference_by_ref_key(self, ref_key):
        return self._reference_repository.get_reference_by_ref_key(ref_key)

    def delete_reference_by_ref_key(self, ref_key):
        return self._reference_repository.delete_reference_by_ref_key(ref_key)

    def ref_key_taken(self, key):
        ref_list = map(lambda x: x.ref_key, self.get_all())
        return key in ref_list

    def add_tag_relation(self, tag_name, ref_key):
        if not self.ref_key_taken(ref_key):
            return False, "Not an existing reference"
        newtag = "Existing tag"
        tag_id = self._reference_repository.get_tag_id(tag_name)
        if tag_id is None:
            val = self._reference_repository.create_tag(tag_name)
            if val is True:
                newtag = "New tag created"
            tag_id = self._reference_repository.get_tag_id(tag_name)
            if tag_id is None:
                return False, "Something went wrong with creating the tag"
        return self._reference_repository.create_tag_relation(tag_id, ref_key), newtag

    def get_tag_id(self, tag_name):
        tag_id = self._reference_repository.get_tag_id(tag_name)
        if tag_id is None:
            return False, "Not an existing tag"
        return True, tag_id

    def get_tagged(self, tag_id):
        return self._reference_repository.get_tagged(tag_id)
