
import regex as re

class SubtitleFileParser:

    def __init__(self, input_filename):
        self.filename = input_filename
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename)
        return self

    def get_line(self):
        line = self.file.readline()
        return line

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        self.file = None