

from datetime import datetime, timedelta, time
import os
from parser import SubtitleFileParser

# start_time = datetime.strptime(start_time_str, '%H:%M:%S,%f')
# end_time = datetime.strptime(end_time_str, '%H:%M:%S,%f')
class Synchronizer:

    def __init__(self, subtitle_delay_start_t: tuple = (0,0,0), subtitle_delay: \
         tuple = (0,0,0), mode=1, input_file=None, output_file=None):
        self.subtitle_delay = subtitle_delay
        minute, second, microsecond = subtitle_delay_start_t
        self.subtitle_delay_start_t = time(hour=0, minute=minute, second=second, microsecond=microsecond)
        self.mode = mode
        self.input_file = input_file
        self._output_file  = output_file or self.create_output_file()

    @property
    def output_file(self):
        return self._output_file 

    @output_file.setter
    def output_file(self, value):
        print(value)
        self._output_file  = value or self.create_output_file()

    def create_output_file(self):
        if not self.input_file:
            return None
        folder, filename = os.path.split(self.input_file)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_synchronized{ext}"
        return os.path.join(folder, new_filename)

    def get_datetime(self, t):
        return datetime.strptime(t, '%H:%M:%S,%f')

    def datetime_str_format(self, t_str):
        return f"{t_str.strftime('%H:%M:%S')},{int(t_str.microsecond / 1000):03d}"

    def get_delayed_line(self, start_t, end_t):
        m, s, ms = self.subtitle_delay

        new_start_t = self.datetime_str_format(start_t + \
            (self.mode)*timedelta(minutes=m, seconds=s, milliseconds=ms))
        new_end_t = self.datetime_str_format(end_t + \
            (self.mode)*timedelta(minutes=m, seconds=s, milliseconds=ms))
        new_line = f"{new_start_t} --> {new_end_t}\n"
        return new_line

    def get_updated_line(self, start_t, end_t, line):
        if start_t and end_t:
            start_time = self.get_datetime(start_t)
            end_time = self.get_datetime(end_t)
            if start_time.time() > self.subtitle_delay_start_t:
                new_line = self.get_delayed_line(start_time, end_time)
                return new_line
        return line

    def process(self):
        if not self._output_file:
            self._output_file = self.create_output_file()
        
        file_parser = SubtitleFileParser(self.input_file)
        with open(self._output_file, "w") as out_f:
            with file_parser as parser:
                for line, start_t, end_t in parser:
                    new_line = self.get_updated_line(start_t, end_t, line)
                    out_f.write(new_line)



