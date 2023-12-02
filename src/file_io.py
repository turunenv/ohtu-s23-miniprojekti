class FileIO:
    def write(self, filename, content, over_write=True):
        mode = "w" if over_write else "a"

        with open(filename, mode, encoding="utf-8") as file:
            file.write(content)
