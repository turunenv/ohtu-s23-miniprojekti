import re
from services.doi_service import DOIService
class App:

    def __init__(self, io, rs, bib):
        self.list = []
        self.io = io
        self.reference_service = rs
        self.bibtex_writer = bib
        self.doi_service = DOIService(io)

    def run(self):

        while True:
            self.io.write("")
            self.io.write(
                "Type \"help\" to list commands and their descriptions")

            command = self.io.read("Command (add or list or delete or file or tag or search)")

            if not command:
                break

            if command == "help":
                self.io.write("")
                self.io.write(
                    'To EXIT the program simply press enter in the starting menu')
                self.io.write(
                    f'{"add:":<9} Add a new reference by provinding the required information')
                self.io.write(f'{"list:":<9} List all stored references')
                self.io.write(
                    f'{"delete:":<9} Delete a reference using its reference key')
                self.io.write(
                    f'{"tag:":<9} Enter a tag name and a reference key to tag a reference')
                self.io.write(f'{"search:":<9} Enter tag name to search tagged references')
                self.io.write(f'{"cancel:":<9} Return to the starting menu')
                self.io.write(
                    f'{"file:":<9} Enter a file name to create a .bib file of all references')
                self.io.write(
                    f'{"doi:":<9} Add a new reference using DOI identifier or full DOI URL')
                self.io.write("\nValid inputs:")
                self.io.write(f'   {"year: ":<10} Year must consist of only numbers')
                self.io.write(f'   {"volume: ":<10} Volume must consist of only numbers')
                self.io.write(f'   {"pages: ":<10} Pages must consist of numbers separated by \"--\"')

            if command == "add":
                self.add_reference()

            elif command == "list":
                self.list_references()

            elif command == "delete":
                self.delete_reference()

            elif command == "file":
                self.create_bib_file()

            elif command == "doi":
                self.get_doi_reference()

            elif command == "tag":
                self.create_tag()

            elif command == "search":
                self.search_tags()

    def add_reference(self):
        self.io.write("")
        self.io.write("Type \"cancel\" to cancel")

        source_type = self.io.read("Give source type: ")
        if not self.validate_input("source_type", source_type):
            return

        list_of_fields = self.reference_service.get_fields_of_reference_type(
            source_type)

        if not list_of_fields:
            self.io.write("ERROR: Source type not supported!")
            return

        rd = {}
        rd["type"] = source_type

        for f in list_of_fields:

            user_input = self.io.read(f"Add {f} of the {source_type}: ")

            if user_input == "cancel":
                return

            while f == "ref_key" and self.reference_service.ref_key_taken(user_input):
                self.io.write("This ref_key is already taken!!")
                user_input = self.io.read(f"Add {f} of the {source_type}: ")
                if user_input == "cancel":
                    return
            while not self.validate_input(f, user_input):
                self.io.write("Invalid input! Please check help-menu for instructions")
                user_input = self.io.read(f"Add {f} of the {source_type}: ")
                if user_input == "cancel":
                    return

            rd[f] = user_input

        if self.reference_service.create_reference(rd):
            self.io.write("ADDED!")

    def list_references(self):
        self.io.write("")
        self.list = self.reference_service.get_all()

        if len(self.list) == 0:
            return

        field_names = []

        for r in self.list:
            if r.get_field_names() != field_names:
                self.io.write(f'\n\n{r.ref_type.upper()}S')
                field_names = r.get_field_names()
                self.write_columns(r)

            self.io.write(r)

    def delete_reference(self):
        self.io.write("Type \"cancel\" to cancel")

        source_ref_key = self.io.read("Give source reference key: ")

        if source_ref_key == "cancel":
            return

        if source_ref_key and self.reference_service.ref_key_taken(source_ref_key):
            self.io.write(
                "Are you sure you want to delete the following reference:")

            reference = self.reference_service.get_book_by_ref_key(
                source_ref_key)

            self.write_columns(reference)
            self.io.write(reference)
        else:
            self.io.write("Incorrect reference key!")
            return

        confirmation = str(self.io.read("(Y to continue)"))
        if confirmation.lower() == "y":
            if self.reference_service.delete_book_by_ref_key(source_ref_key):
                self.io.write("DELETED!")
            else:
                self.io.write(
                    "Something went wrong with deleting the reference")
        else:
            self.io.write("Deletion cancelled")

    def get_doi_reference(self):
        ref_key = self.io.read("Give ref_key for this reference: ")

        if not self.validate_input("ref_key", ref_key):
            return

        while self.reference_service.ref_key_taken(ref_key):
            self.io.write("This ref_key was already taken!")
            ref_key = self.io.read("Give a ref_key for this reference: ")
            if not self.validate_input("ref_key", ref_key):
                return

        doi_string = self.io.read("Give DOI identifier or full URL: ")
        if not self.validate_input("doi_string", doi_string):
            return

        reference = self.doi_service.get_doi(doi_string, ref_key)

        if not reference:
            return

        self.io.write("\nDo you want to add the following reference?")
        for field, value in reference.items():
            self.io.write(f'{field[:15]:<15}: {value}')

        for field, value in reference.items():
            if not self.validate_input(field, value):
                self.io.write("DOI has invalid values and can not be added")
                self.io.write("-->" + field + ":" + value)
                return

        confirmation = str(self.io.read("(Y to continue)"))
        if confirmation.lower() == "y":
            if self.reference_service.create_reference(reference):
                self.io.write("ADDED!")



    def write_columns(self, reference):
        field_names = reference.get_field_names()
        field_lengths = reference.get_field_lengths()
        column_amount = len(field_names)

        columns = ""

        for i in range(column_amount):
            columns += f'{field_names[i]:<{field_lengths[i]}} '

        self.io.write("\n" + columns)
        self.io.write(f'{"":{"-"}>115}')

    def create_bib_file(self):
        filename = self.io.read("Give the name of file:")

        if not filename:
            self.io.write("File creation cancelled")
            return

        if not filename.endswith(".bib"):
            filename += ".bib"

        references = self.reference_service.get_all()

        file_write_success = self.bibtex_writer.write_references_to_file(
            filename,
            references
        )

        if file_write_success:
            self.io.write(
                f"{len(references)} references succesfully written to {filename}"
            )

        else:
            self.io.write(f"There was an error creating file {filename}.")

    def create_tag(self):
        self.io.write("")
        self.io.write("Type \"cancel\" to cancel")

        tag_name = self.io.read("Give tag name: ")
        if tag_name == "cancel":
            return

        ref_key = self.io.read(
            "Give ref_key of the reference you want to tag: ")
        if ref_key == "cancel":
            return

        val = self.reference_service.add_tag_relation(tag_name, ref_key)
        if val[0] is False:
            self.io.write(val[1])
        else:
            self.io.write(val[1])
            self.io.write("TAGGED!")

    def search_tags(self):
        self.io.write("")
        self.io.write("Type \"cancel\" to cancel")

        tag_name = self.io.read("Give tag name: ")
        if tag_name in ('cancel', ''):
            return

        tag_id = self.reference_service.get_tag_id(tag_name)
        if tag_id[0] is False:
            self.io.write(tag_id[1])
            return
        tag_id = tag_id[1]
        print(tag_id)

        self.list = self.reference_service.get_tagged(tag_id)

        if len(self.list) == 0:
            self.io.write("No references are using the tag")
            return

        field_names = []

        for r in self.list:
            if r.get_field_names() != field_names:
                self.io.write(f'\n\n{r.ref_type.upper()}S')
                field_names = r.get_field_names()
                self.write_columns(r)

            self.io.write(r)


    def validate_input(self, field, user_input):
        if user_input.strip() == "" or user_input == "cancel":
            return False

        match field:
            case "year":
                return re.match("^[0-9]+$", user_input)
            case "volume":
                return re.match("^[0-9]+$", user_input)
            case "pages":
                return re.match("^[0-9]+--[0-9]+$", user_input)
            case _:
                return True
