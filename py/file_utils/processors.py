import os

class FileLineProcessor:

    def __init__(self, file_path):
        self.file_path = file_path

    def process_line(self, line):
        pass

    def process_lines(self, lines):
        for line in lines:
            self.process_line(line)

    def process(self):
        rfile = open(self.file_path, "r")
        lines = rfile.readlines()
        rfile.close()
        self.process_lines(lines)

class DirectoryFileProcessor:

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def process_file(self, file_name):
        pass

    def process_entry(self, entry):
        if entry.is_file():
            self.process_file(self.base_directory+"/"+entry.name)

    def process_entries(self, entries):
        for entry in entries:
            self.process_entry(entry)

    def process(self):
        with os.scandir(self.base_directory) as entries:
            self.process_entries(entries)

class FileWriter:
    
    def __init__(self, file_path):
        self.file_path = file_path

    def writeTxt(self,content):
        self.wfile.write(content)

    def end(self):
        self.wfile.flush()
        self.wfile.close()

    def start(self):
        self.wfile = open(self.file_path, "w")