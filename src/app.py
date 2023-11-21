class App:
    
    def __init__(self, io, rs):
        ### self.reference_service =
        self.list = []
        self.io = io
        self.reference_service = rs

    def run(self):

        while True:
            
            command = self.io.read("Command (add or list)")

            if not command:
                break

            if command == "add":
                # Lisätään viite
                self.add_reference()
            
            if command == "list":
                self.list_references()

    def add_reference(self):
        # Kysytään viitteen tyyppiä = source_type
        source_type = self.io.read("Give source type: ")

        list_of_fields = self.reference_service.get_fields_of_reference_type(source_type)
        
        if not list_of_fields:
            print("ERROR: Source type not supported!")
            return
        
        # rd = Reference Dictionary, Yhden viiteen tiedot dictionaryssä
        rd = {}
        
        # Luetaan käyttäjän syöte jokaiseen vaadittuun kenttään
        for f in list_of_fields:
            rd[f] = self.io.read(f"Add {f} of the {source_type}: ")

        ### self.reference_service.add_reference(rd)
        self.list.append(rd)

        print("ADDED!")

    def list_references(self):
        
        ### self.list = self.reference_service.getAll()
        for r in self.list:
            print(r)
        

