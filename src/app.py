class App:
    
    def __init__(self, io):
        # self.reference_service =
        self.list = []
        self.io = io

    def run(self):

        while True:
            
            command = self.io.read("Command (add or list)")

            if not command:
                break

            if command == "add":
                # Lisätään viite

                # Kysytään viitteen tyyppiä
                rType = "book"
                
                self.add_reference(rType)
            
            if command == "list":
                self.list_references()

    def add_reference(self, rType):
        # Haetaan vaaditut kentät jostain :D
        list_of_fields = ["title", "author", "year", "publisher"]
        
        # rd = Reference Dictionary, Yhden viiteen tiedot dictionaryssä
        rd = {}
        
        # Luetaan käyttäjän syöte jokaiseen vaadittuun kenttään
        for f in list_of_fields:
            rd[f] = self.io.read(f"Add {f} of the {rType}: ")

        self.list.append(rd)
        print("ADDED!")

    def list_references(self):
    
        for r in self.list:
            print(r)
        

