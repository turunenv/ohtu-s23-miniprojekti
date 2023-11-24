class App:

    def __init__(self, io, rs):
        self.list = []
        self.io = io
        self.reference_service = rs

    def run(self):

        while True:

            command = self.io.read("Command (add or list or delete)")

            if not command:
                break

            if command == "add":
                self.add_reference()

            elif command == "list":
                self.list_references()

            elif command == "delete":
                self.delete_reference()

    def add_reference(self):

        self.io.write("Type \"cancel\" to cancel")

        source_type = self.io.read("Give source type: ")

        list_of_fields = self.reference_service.get_fields_of_reference_type(source_type)

        if source_type == "cancel":
            return

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

            while user_input.strip() == "":
                self.io.write("This field is required!")
                user_input = self.io.read(f"Add {f} of the {source_type}: ")

            rd[f] = user_input

        if self.reference_service.create_reference(rd):
            self.io.write("ADDED!")


    def list_references(self):

        self.list = self.reference_service.get_all()
        r = "REF_KEY"
        a = "AUTHOR"
        t = "TITLE"
        y = "YEAR"
        p = "PUBLISHER"
        self.io.write(f"{r:10} {a:25} {t:20} {y:5} {p:15}")
        for r in self.list:
            self.io.write(r)

    def delete_reference(self):
        self.io.write("Type \"cancel\" to cancel")

        source_ref_key = self.io.read("Give source reference key: ")

        if source_ref_key == "cancel":
            return

        if source_ref_key and self.reference_service.ref_key_taken(source_ref_key):
            self.io.write("Are you sure you want to delete the following reference:")

            self.source_fields = self.reference_service.get_book_by_ref_key(source_ref_key)
            r = "REF_KEY"
            a = "AUTHOR"
            t = "TITLE"
            y = "YEAR"
            p = "PUBLISHER"
            self.io.write(f"{r:10} {a:25} {t:20} {y:5} {p:15}")
            self.io.write(self.source_fields)
        else: 
            self.io.write("Incorrect reference key!")
            return


        confirmation = self.io.read("(Y to continue)")
        if confirmation.lower() == "y":
            if self.reference_service.delete_book_by_ref_key(source_ref_key):
                self.io.write("DELETED!")
                return
            else: 
                self.io.write("Something went wrong with deleting the reference")
                return
        else:
            self.io.write("Deletion canceled")

