class App:

    def __init__(self, io, rs, bib):
        self.list = []
        self.io = io
        self.reference_service = rs
        self.bibtex_writer = bib

    def run(self):

        while True:
            self.io.write("")
            self.io.write(
                "Type \"help\" to list commands and their descriptions")

            command = self.io.read("Command (add or list or delete or file)")

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
                self.io.write(f'{"cancel:":<9} Return to the starting menu')
                self.io.write(
                    f'{"file:":<9} Enter a file name to create a .bib file of all references')

            if command == "add":
                self.add_reference()

            elif command == "list":
                self.list_references()

            elif command == "delete":
                self.delete_reference()

            elif command == "file":
                self.create_bib_file()

            elif command == "tag":
                self.create_tag()

    def add_reference(self):
        self.io.write("")
        self.io.write("Type \"cancel\" to cancel")

        source_type = self.io.read("Give source type: ")
        if source_type == "cancel":
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

            while user_input.strip() == "":
                self.io.write("This field is required!")
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
                self.io.write(f'\n\n{r.type.upper()}S')
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
        
        ref_key = self.io.read("Give ref_key of the reference you want to tag: ")
        if ref_key == "cancel":
            return

        val = self.reference_service.add_tag_relation(tag_name, ref_key)
        if val[0] is False:
            self.io.write(val[1])
        else: 
            self.io.write(val[1])
            self.io.write("TAGGED!")
        
        
        
