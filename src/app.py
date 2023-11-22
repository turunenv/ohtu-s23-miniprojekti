class App:
    
    def __init__(self, io, rs):
        self.list = []
        self.io = io
        self.reference_service = rs

    def run(self):

        while True:
            
            # Kysytään käyttäjältä komentoa
            command = self.io.read("Command (add or list)")

            if not command:
                break

            # Lisätään viite
            if command == "add":
                self.add_reference()
            
            # Listataan viitteet
            if command == "list":
                self.list_references()

    def add_reference(self):

        # Kysytään viitteen tyyppiä
        source_type = self.io.read("Give source type: ")

        # Haetaan lista viitetyypin pakollisista kentistä
        list_of_fields = self.reference_service.get_fields_of_reference_type(source_type)
        
        # Jos viitetyyppiä ei löydy serviceltä, ilmoitetaan käyttäjälle ja aloitetaan alusta
        if not list_of_fields:
            self.io.write("ERROR: Source type not supported!")
            return
        
        # Alustetaan dictionary, johon viitteen tiedot talletetaan
        # Viitetyyppi lisätään
        rd = {}
        rd["type"] = source_type

        # Luetaan käyttäjän syöte jokaiseen vaadittuun kenttään
        for f in list_of_fields:

            input = self.io.read(f"Add {f} of the {source_type}: ")

            while f == "ref_key" and self.reference_service.ref_key_taken(input):
                self.io.write("This ref_key is already taken!!")
                input = self.io.read(f"Add {f} of the {source_type}: ")

            # Validoidaan syöte
            while input.strip() == "":
                self.io.write("This field is required!")
                input = self.io.read(f"Add {f} of the {source_type}: ")

            rd[f] = input

        # Lähetetään viite servicen avulla tietokantaan
        if self.reference_service.create_reference(rd):
            self.io.write("ADDED!")


    def list_references(self):

        # Haetaan kaikki talletetut viitteet serviceltä tulostetaan ne komentoriville
        self.list = self.reference_service.get_all()
        for r in self.list:
            self.io.write(r)
        

