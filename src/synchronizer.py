

from datetime import datetime, timedelta
import os
from .parser import SubtitleFileParser

# start_time = datetime.strptime(start_time_str, '%H:%M:%S,%f')
# end_time = datetime.strptime(end_time_str, '%H:%M:%S,%f')
class Synchronizer:

    def __init__(self, title_delay, input_file, output_file=None):
        self.title_delay = title_delay
        self.input_file = input_file
        self.output_file = output_file or self.create_output_file(input_file)
        self.file_parser = SubtitleFileParser(self.input_file)

    def create_output_file(self, input_file): 
        folder, filename = os.path.split(input_file)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_fixed{ext}"
        return os.path.join(folder, new_filename)

    def get_delayed_line(self, start_t, end_t):
        start_time = datetime.strptime(start_t, '%H:%M:%S,%f')
        end_time = datetime.strptime(end_t, '%H:%M:%S,%f')
        m, s, ms = self.title_delay

        new_start_t = start_time + timedelta(minutes=m, seconds=s, milliseconds=ms)
        new_end_t = end_time + timedelta(minutes=m, seconds=s, milliseconds=ms)

        new_line = (
            f"{new_start_t.strftime('%H:%M:%S')},{int(new_start_t.microsecond / 1000):03d} --> "
            f"{new_end_t.strftime('%H:%M:%S')},{int(new_end_t.microsecond / 1000):03d}\n"
        )
        return new_line

    def process(self):
        with open(self.output_file, "w") as out_f:
            with self.file_parser as parser:
                for line, start_t, end_t in parser:
                    if start_t and end_t:
                        new_line = self.get_delayed_line(start_t, end_t)
                        out_f.write(new_line)
                    else:
                        out_f.write(line)



