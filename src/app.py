import tkinter as tk
from tkinter import filedialog
from datetime import timedelta
from synchronizer import Synchronizer

def format_time(seconds):
    td = timedelta(seconds=abs(seconds))
    prefix = '-' if seconds < 0 else ''
    return f"{prefix}{str(td)}"

class TimeSynchronizerGUIController:
    def __init__(self):
        root = tk.Tk()
        root.geometry("600x400")
        self.synchronizer = Synchronizer()
        self.root = root
        root.title("Time Scrollbar App")
        
        self.input_file_label = tk.Label(root, text="No file chosen")
        self.input_file_label.pack(pady=(30, 0))
        self.input_file_btn = tk.Button(root, text="Choose Input File", command=self.choose_input_file)
        self.input_file_btn.pack(pady=10)

        self.output_file_label = tk.Label(root, text="No file chosen")
        self.output_file_label.pack(pady=0)
        self.output_file_btn = tk.Button(root, text="Choose Output File", command=self.choose_output_file)
        self.output_file_btn.pack(pady=10)


        # slider for start time of delayed subtitles
        self.slider_length = 400
        self.start_time_scroll = tk.Scale(root, label="Start time of delayed subtitles", from_=-7200, to=7200, orient="horizontal", length=self.slider_length,
                               command=self.update_start_time, showvalue=False, resolution=1)
        self.start_time_scroll.pack(pady=20)

        self.start_time_label = tk.Label(root, text="00:00:00", font=("Arial", 10))
        self.start_time_label.place(x=20, y=self.start_time_scroll.get()-10)

        self.root.after(100, self.update_start_time, self.start_time_scroll.get())

        # slider for delay
        self.time_delay_scroll = tk.Scale(root, label="Delayed time", from_=-7200, to=7200, orient="horizontal", length=self.slider_length,
                               command=self.update_delay, showvalue=False, resolution=1)
        self.time_delay_scroll.pack(pady=20)

        self.time_delay_label = tk.Label(root, text="00:00:00", font=("Arial", 10))
        self.time_delay_label.place(x=20, y=self.time_delay_scroll.get()-10)


        self.root.after(100, self.update_delay, self.time_delay_scroll.get())

        self.synchronize_btn = tk.Button(root, text="Synchronize", command=self.synchronize)
        self.synchronize_btn.pack(pady=20)
        self.root.mainloop()

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
        range_span = 14400  # total seconds from -7200 to +7200
        relative_pos = (seconds + 7200) / range_span
        thumb_x = scroll_widget_x + relative_pos * self.slider_length

        label_width = self.start_time_label.winfo_reqwidth()
        self.start_time_label.place(x=thumb_x - label_width / 2,
                               y=self.start_time_scroll.winfo_y() - 20)
        self.synchronizer.subtitle_delay_start_t = self.convert_seconds(seconds)


    def update_delay(self, value):
        seconds = int(value)
        time_str = format_time(seconds)
        self.time_delay_label.config(text=time_str)

        scroll_widget_x = self.time_delay_scroll.winfo_rootx() - self.root.winfo_rootx()
        range_span = 14400  # from -7200 to +7200
        relative_pos = (seconds + 7200) / range_span
        thumb_x = scroll_widget_x + relative_pos * self.slider_length

        label_width = self.time_delay_label.winfo_reqwidth()
        self.time_delay_label.place(x=thumb_x - label_width / 2,
                                    y=self.time_delay_scroll.winfo_y() - 20)

        self.synchronizer.subtitle_delay = self.convert_seconds(abs(seconds))
        self.synchronizer.mode = 1 if seconds > 0 else -1


    def synchronize(self):
        self.synchronizer.process()

if __name__ == "__main__":
    app = TimeSynchronizerGUIController()
