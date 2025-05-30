import tkinter as tk
from tkinter import filedialog
from datetime import timedelta
from src.synchronizer import Synchronizer

def format_time(seconds):
    td = timedelta(seconds=abs(seconds))
    prefix = '-' if seconds < 0 else ''
    return f"{prefix}{str(td)}"

class TimeSynchronizerGUIController:

    TEXT_FONT = ("Segoe UI", 14)

    def __init__(self):
        root = tk.Tk()
        root.geometry("700x500")
        root.title("Subtitle Time Synchronizer")

        self.root = root
        self.synchronizer = Synchronizer()
        self.slider_length = 500

        self.input_file_label = tk.Label(root, text="No input file chosen", font=self.TEXT_FONT, anchor="w", fg="gray")
        self.input_file_label.pack(padx=15, pady=(30, 5))

        self.input_file_btn = tk.Button(root, text="Choose Input File", font=self.TEXT_FONT, command=self.choose_input_file)
        self.input_file_btn.pack(pady=(0, 80))

        self.output_file_label = tk.Label(root, text="No output file chosen", font=self.TEXT_FONT, anchor="w", fg="gray")
        self.output_file_label.pack(padx=10, pady=(0, 5))

        self.output_file_btn = tk.Button(root, text="Choose Output File", font=self.TEXT_FONT, command=self.choose_output_file)
        self.output_file_btn.pack(pady=(0, 50))

        self.start_time_scroll = tk.Scale(root, label="Start time of delayed subtitles", font=self.TEXT_FONT, 
                                          from_=-7200, to=7200, orient="horizontal", length=self.slider_length, 
                                          showvalue=False, resolution=1, command=self.update_start_time)
        self.start_time_scroll.pack(pady=(0, 10))

        self.start_time_label = tk.Label(root, text="00:00:00", font=self.TEXT_FONT)
        self.start_time_label.place(x=20, y=self.start_time_scroll.winfo_y() - 20)

        self.time_delay_scroll = tk.Scale(root, label="Delayed time", font=self.TEXT_FONT, from_=-7200, to=7200,
                                          orient="horizontal", length=self.slider_length, showvalue=False,
                                          resolution=1, command=self.update_delay)
        self.time_delay_scroll.pack(pady=(10, 50))

        self.time_delay_label = tk.Label(root, text="00:00:00", font=self.TEXT_FONT)
        self.time_delay_label.place(x=20, y=self.time_delay_scroll.winfo_y())

        self.synchronize_btn = tk.Button(root, text="Synchronize", font=self.TEXT_FONT, command=self.synchronize)
        self.synchronize_btn.pack(pady=(10, 10))

        self.root.after_idle(lambda: self.update_delay(self.time_delay_scroll.get()))
        self.root.after_idle(lambda: self.update_start_time(self.start_time_scroll.get()))
        root.mainloop()

    @classmethod
    def convert_seconds(cls, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return hours, minutes, seconds

    def choose_input_file(self):
        file_path = filedialog.askopenfilename(title="Select Input File")
        if file_path:
            self.input_file_label.config(text=file_path)
            self.synchronizer.input_file = file_path

    def choose_output_file(self):
        file_path = filedialog.asksaveasfilename(title="Select Output File")
        if file_path:
            self.output_file_label.config(text=file_path)
            self.synchronizer.output_file = file_path

    def update_start_time(self, value):
        seconds = int(value)
        time_str = format_time(seconds)
        self.start_time_label.config(text=time_str)

        scroll_widget_x = self.start_time_scroll.winfo_rootx() - self.root.winfo_rootx()
        relative_pos = (seconds + 7200) / 14400
        thumb_x = scroll_widget_x + relative_pos * self.slider_length
        label_width = self.start_time_label.winfo_reqwidth()

        self.start_time_label.place(x=thumb_x - label_width / 2,
                                    y=self.start_time_scroll.winfo_y() - 20)

        self.synchronizer.subtitle_delay_start_t = self.convert_seconds(abs(seconds))

    def update_delay(self, value):
        seconds = int(value)
        time_str = format_time(seconds)
        self.time_delay_label.config(text=time_str)

        scroll_widget_x = self.time_delay_scroll.winfo_rootx() - self.root.winfo_rootx()
        relative_pos = (seconds + 7200) / 14400
        thumb_x = scroll_widget_x + relative_pos * self.slider_length
        label_width = self.time_delay_label.winfo_reqwidth()

        self.time_delay_label.place(x=thumb_x - label_width / 2,
                                    y=self.time_delay_scroll.winfo_y() - 20)

        self.synchronizer.subtitle_delay = self.convert_seconds(abs(seconds))
        self.synchronizer.mode = 1 if seconds > 0 else -1

    def synchronize(self):
        self.synchronizer.process()

if __name__ == "__main__":
    TimeSynchronizerGUIController()
