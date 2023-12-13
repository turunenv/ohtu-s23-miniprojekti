import requests

class DOIService:
    def __init__(self, io):
        self.io = io
        self.base_url = 'https://doi.org/'
        self.headers = {'accept': 'application/vnd.citationstyles.csl+json'}
        self.timeout = 3

    def get_doi(self, doi, ref_key):
        url = self.resolve_url(doi)
        data = self.retrieve_data(url)
        reference = {}

        if not bool(data):
            return reference

        try:
            reference_type = data["type"]

            if reference_type == "journal-article":
                reference = self.create_article(data, ref_key)
            elif reference_type == "book":
                reference = self.create_book(data, ref_key)
            elif "proceedings" in reference_type:
                reference = self.create_inproceedings(data, ref_key)
            else:
                self.io.write("This reference type is not supported")
        except KeyError as e:
            self.io.write(e)
            self.io.write("Reference could not be created:")
            self.io.write(f'{" ":<4}Some necessary information was missing')
        return reference

    def retrieve_data(self, url):
        data = {}
        try:
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            data = r.json()
        except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
            self.io.write('DOI not found')
        except Exception: #pylint: disable=broad-exception-caught
            self.io.write("There was an unexpected network error")

        return data

    def resolve_url(self, doi):
        if "doi.org" in doi:
            return doi
        if doi[0] == "/":
            return self.base_url + doi[1:]
        return self.base_url + doi

    def create_article(self, data, ref_key):
        author, title, journal, year, volume, pages = ("",)*6

        if not "author" in data:
            author = "Undefined"
        else:
            for i in data["author"]:
                if "given" in i and "family" in i:
                    author += i["family"] + ", " + i["given"] + " and "
                else:
                    author += i["family"] + " and "
            author = author[:-5]

        title = data["title"]

        if "publisher" in data:
            journal = data["publisher"]
        elif "container-title" in data:
            journal = data["container-title"]

        if "volume" in data:
            volume = data["volume"]
        else:
            volume = "1"

        year = str(data["published"]["date-parts"][0][0])

        pages = data["page"].replace("-", "--")
        if "--" not in pages:
            pages = pages + "--" + pages

        article = {
            "type": "article", "ref_key": ref_key, "author": author,
            "title": title, "journal": journal, "year": year,
            "volume": volume, "pages": pages
        }

        return article

    def create_book(self, data, ref_key):
        author, title, year, publisher = ("",)*4

        if "author" not in data:
            author = "Undefined"
        else:
            for i in data["author"]:
                author += i["family"] + ", " + i["given"] + " and "
            author = author[:-5]

        title = data["title"]
        year = str(data["published"]["date-parts"][0][0])
        publisher = data["publisher"]

        book = {
            "type": "book","ref_key": ref_key, "author": author,
            "title": title, "year": year, "publisher": publisher
        }
        return book

    def create_inproceedings(self, data, ref_key):
        author, title, year, booktitle = ("",)*4

        if "author" not in data:
            author = "Undefined"
        else:
            for i in data["author"]:
                author += i["family"] + ", " + i["given"] + " and "
            author = author[:-5]

        title = data["title"]
        year = str(data["created"]["date-parts"][0][0])
        booktitle = data["container-title"]

        inproceedings = {
            "type": "inproceedings","ref_key": ref_key, "author": author,
            "title": title, "year": year, "booktitle": booktitle
        }
        return inproceedings
