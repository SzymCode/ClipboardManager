import tkinter as tk
from tkinter import *

BG_COLOR = "#e3e3e3"


class ClipboardManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side=RIGHT, fill=Y)

        mylist = Listbox(self.window, bg=BG_COLOR, width=24, yscrollcommand=scrollbar.set)
        for line in range(10):
            mylist.insert(0, "")

        mylist.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=mylist.yview)

    def place_window(self, width=165, height=115):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = screen_width - (width + 10.5)
        y = screen_height - (height + 73.5)
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    clipboard_manager = ClipboardManager()
    clipboard_manager.place_window()
    clipboard_manager.run()