class BibTexWriter:
    """A Class to write references into a file
       
    Arguments:
        - file_io object with a write method
    """
    def __init__(self, file_io):
        self.file_io = file_io

    def write_references_to_file(self, filename, references, over_write=True):
        """
        Given a filename, list of reference objects and optional over_write parameter,
        Return True if writing to file succeeded, otherwise False
        """
        try:
            for i, ref in enumerate(references):
                #in any case, do not overwrite after the initial reference
                if i > 0:
                    over_write = False
                self.file_io.write(filename, ref.create_bib_string(), over_write)
            return True
        except OSError:
            return False
