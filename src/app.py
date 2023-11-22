class App:
    
    def __init__(self, io, rs):
        self.list = []
        self.io = io
        self.reference_service = rs

    def run(self):

        while True:
            
            command = self.io.read("Command (add or list)")

            if not command:
                break

            if command == "add":
                self.add_reference()
            
            if command == "list":
                self.list_references()

    def add_reference(self):

        source_type = self.io.read("Give source type: ")

        list_of_fields = self.reference_service.get_fields_of_reference_type(source_type)
        
        if not list_of_fields:
            self.io.write("ERROR: Source type not supported!")
            return
        
        rd = {}
        rd["type"] = source_type

        for f in list_of_fields:

            input = self.io.read(f"Add {f} of the {source_type}: ")

            while f == "ref_key" and self.reference_service.ref_key_taken(input):
                self.io.write("This ref_key is already taken!!")
                input = self.io.read(f"Add {f} of the {source_type}: ")

            while input.strip() == "":
                self.io.write("This field is required!")
                input = self.io.read(f"Add {f} of the {source_type}: ")

            rd[f] = input

        if self.reference_service.create_reference(rd):
            self.io.write("ADDED!")


    def list_references(self):

        self.list = self.reference_service.get_all()
        for r in self.list:
            self.io.write(r)
        

