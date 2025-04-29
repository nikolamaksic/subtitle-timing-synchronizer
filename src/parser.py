
import regex as re
from datetime import datetime
class SubtitleFileParser:
    TIMING_PATTERN = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s-->\s(\d{2}:\d{2}:\d{2},\d{3})")

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.file = None

    def __enter__(self):
        self.file = open(self.input_file_path, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        if not line:
            raise StopIteration

        match = self.TIMING_PATTERN.search(line)
        if match:
            return line, match.group(1), match.group(2)
        return line, None, None