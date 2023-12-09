import re
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from services.doi_service import DOIService
class App:

    def __init__(self, io, rs, bib):
        self.list = []
        self.io = io
        self.reference_service = rs
        self.bibtex_writer = bib
        self.doi_service = DOIService(io)

    def run(self):
        console = Console()
        while True:
            console.print("")
            console.print(
                "Type \"help\" to list commands and their descriptions", style = 'deep_sky_blue4')

            command = Prompt.ask("Command: ", choices =["help", "add", "list", "delete", "file", "doi", "tag", "search", "exit"])

            if command == "exit":
                break

            if command == "help":
                console.print("")
                console.print(
                    'To EXIT the program simply select exit in the starting menu', style = 'deep_sky_blue4')
                console.print(
                    f'{"add:":<9} Add a new reference by provinding the required information',style = 'deep_sky_blue4')
                console.print(f'{"list:":<9} List all stored references',style = 'deep_sky_blue4')
                console.print(
                    f'{"delete:":<9} Delete a reference using its reference key', style = 'deep_sky_blue4')
                console.print(
                    f'{"tag:":<9} Enter a tag name and a reference key to tag a reference', style = 'deep_sky_blue4')
                console.print(f'{"search:":<9} Enter tag name to search tagged references', style = 'deep_sky_blue4')
                console.print(f'{"cancel:":<9} Return to the starting menu', style = 'deep_sky_blue4')
                console.print(
                    f'{"file:":<9} Enter a file name to create a .bib file of all references', style = 'deep_sky_blue4')
                console.print(
                    f'{"doi:":<9} Add a new reference using DOI identifier or full DOI URL', style = 'deep_sky_blue4')
                console.print("\nValid inputs:", style = 'deep_sky_blue4')
                console.print(f'   {"year: ":<10} Year must consist of only numbers', style = 'deep_sky_blue4')
                console.print(f'   {"volume: ":<10} Volume must consist of only numbers', style = 'deep_sky_blue4')
                console.print(f'   {"pages: ":<10} Pages must consist of numbers separated by \"--\"', style = 'deep_sky_blue4')

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
        console = Console()
        console.print("")
        #console.print("Type \"cancel\" to cancel")
        types = ["book", "article", "cancel"]
        source_type = Prompt.ask("Give source type: ", choices = types)
        #if not self.validate_input("source_type", source_type):
        #    return

        #list_of_fields = self.reference_service.get_fields_of_reference_type(
        #    source_type)
        if source_type == "cancel":
        #if not list_of_fields:
        #    self.io.write("ERROR: Source type not supported!")
            return
        list_of_fields = self.reference_service.get_fields_of_reference_type(
            source_type)
        rd = {}
        rd["type"] = source_type

        for f in list_of_fields:

            user_input = Prompt.ask(f"Add {f} of the {source_type}: ")

            #if user_input == "cancel":
            #    return

            while f == "ref_key" and self.reference_service.ref_key_taken(user_input):
                #saisko tähän listan kielletyistä prompteista?
                console.print("This ref_key is already taken!!", style = "red")
                user_input = Prompt.ask(f"Add {f} of the {source_type}: ")
                if user_input == "cancel":
                    return
            while not self.validate_input(f, user_input):
                console.print("Invalid input! Please check help-menu for instructions", style = "red")
                user_input = Prompt.ask(f"Add {f} of the {source_type}: ")
                if user_input == "cancel":
                    return

            rd[f] = user_input

        if self.reference_service.create_reference(rd):
            self.print_success("ADDED!")

    def list_references(self):
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

    def write_columns(self, reference):
        console = Console()
        field_names = reference.get_field_names()
        field_lengths = reference.get_field_lengths()
        column_amount = len(field_names)

        columns = ""

        for i in range(column_amount):
            columns += f'{field_names[i]:<{field_lengths[i]}} '

        console.print(f"\n {columns}", style = 'bold magenta')
        console.print(f'{"":{"-"}>115}', style = 'magenta')

    def delete_reference(self):
        console = Console()
        console.print("Type \"cancel\" to cancel", style = 'deep_sky_blue4')

        source_ref_key = Prompt.ask("Give source reference key")

        if source_ref_key == "cancel":
            return

        if source_ref_key and self.reference_service.ref_key_taken(source_ref_key):
            console.print(
                "Are you sure you want to delete the following reference:")

            reference = self.reference_service.get_book_by_ref_key(
                source_ref_key)

            self.write_columns(reference)
            console.print(reference)
        else:
            console.print("Incorrect reference key!", style = 'red')
            return

        confirmation = Prompt.ask("Confirm deletion?", choices = ['yes', 'no'])
        if confirmation == "yes":
            if self.reference_service.delete_book_by_ref_key(source_ref_key):
                self.print_success("DELETED!")
            #else:
            #    self.io.write(
            #        "Something went wrong with deleting the reference")
        else:
            console.print("Deletion cancelled")

    def get_doi_reference(self):
        console = Console()
        ref_key = Prompt.ask("Give ref_key for this reference")

        if not self.validate_input("ref_key", ref_key):
            return

        while self.reference_service.ref_key_taken(ref_key):
            console.print("This ref_key was already taken!", style = 'red')
            ref_key = Prompt.ask("Give a ref_key for this reference")
            if not self.validate_input("ref_key", ref_key):
                return

        doi_string = Prompt.ask("Give DOI identifier or full URL")
        if not self.validate_input("doi_string", doi_string):
            return

        reference = self.doi_service.get_doi(doi_string, ref_key)

        if not reference:
            return

        console.print("\nDo you want to add the following reference?", style = 'deep_sky_blue4')
        for field, value in reference.items():
            console.print(f'{field[:15]:<15}: {value}')

        for field, value in reference.items():
            if not self.validate_input(field, value):
                console.print("DOI has invalid values and can not be added", style = 'red')
                console.print(f"-->  {field} : {value}")
                return

        confirmation = Prompt.ask("Confirm addition", choices = ['yes', 'no'])
        if confirmation == "yes":
            if self.reference_service.create_reference(reference):
                self.print_success("ADDED!")


    def create_bib_file(self):
        console = Console()
        filename = Prompt.ask("Give the name of file")

        if not filename:
            console.print("File creation cancelled", style = red)
            return

        if not filename.endswith(".bib"):
            filename += ".bib"

        references = self.reference_service.get_all()

        file_write_success = self.bibtex_writer.write_references_to_file(
            filename,
            references
        )

        if file_write_success:
            self.print_success(
                f"{len(references)} references succesfully written to {filename}"
            )

        else:
            console.print(f"There was an error creating file {filename}.", style = 'red')

    def create_tag(self):
        console = Console()
        console.print("")
        console.print("Type \"cancel\" to cancel", style = 'deep_sky_blue4')

        tag_name = Prompt.ask("Give tag name")
        if tag_name == "cancel":
            return

        ref_key = Prompt.ask(
            "Give ref_key of the reference you want to tag")
        if ref_key == "cancel":
            return

        val = self.reference_service.add_tag_relation(tag_name, ref_key)
        if val[0] is False:
            console.print(val[1], style = 'red')
        else:
            console.print(val[1], style = 'deep_sky_blue4')
            self.print_success("TAGGED!")

    def search_tags(self):
        console = Console()
        console.print("")
        console.print("Type \"cancel\" to cancel", style = 'deep_sky_blue4')

        tag_name = Prompt.ask("Give tag name")
        if tag_name in ('cancel', ''):
            return

        tag_id = self.reference_service.get_tag_id(tag_name)
        if tag_id[0] is False:
            console.print(tag_id[1], style = 'red')
            return
        tag_id = tag_id[1]

        self.list = self.reference_service.get_tagged(tag_id)

        if len(self.list) == 0:
            console.print("No references are using the tag", style = 'deep_sky_blue4')
            return

        field_names = []

        for r in self.list:
            if r.get_field_names() != field_names:
                console.print(f'\n\n{r.ref_type.upper()}S', style = 'deep_sky_blue4')
                field_names = r.get_field_names()
                self.write_columns(r)

            console.print(r, style = 'deep_sky_blue4')


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

    def print_success(self, message:str):
        """Function, that prints the user a confirmation of a successful event
            Args:
                message: Message, that will be printed
        """
        print("\n")
        console = Console()
        grid = Table.grid(expand=True)
        grid.add_column(max_width=35)
        grid.add_column(justify="left")
        grid.add_column(width=20)
        grid.add_row(f"[deep_sky_blue4] {message}", "[bold magenta]READY[green4]:heavy_check_mark:", "")
        console.print(grid)
        print("\n")
