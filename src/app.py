class App:

    def __init__(self, io, rs):
        self.list = []
        self.io = io
        self.reference_service = rs

    def run(self):

        while True:
            self.io.write("")
            self.io.write(
                "Type \"help\" to list commands and their descriptions")

            command = self.io.read("Command (add or list or delete)")

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

            if command == "add":
                self.add_reference()

            elif command == "list":
                self.list_references()

            elif command == "delete":
                self.delete_reference()

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
            # JOS RIVIN KOLUMNIT =! EDELLISEN RIVIN KOLUMNIT
            if r.get_field_names() != field_names:
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
