import threading
import tkinter as tk
from tkinter import *

import pyperclip

BG_COLOR = "#e3e3e3"


class ClipboardManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.iconbitmap("images/favicon.ico")

        scrollbar = Scrollbar()
        scrollbar.pack(side=RIGHT, fill=Y)
        self.mylist = Listbox(self.window, bg=BG_COLOR, width=24, yscrollcommand=scrollbar.set)

        self.mylist.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.mylist.yview)

    def place_window(self, width=165, height=115):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = screen_width - (width + 10.5)
        y = screen_height - (height + 73.5)
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def clip(self):
        if not (pyperclip.waitForNewPaste() == ""):
            clipboard = pyperclip.waitForPaste()
            header = f" {clipboard}"
            self.mylist.insert(0, header)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    clipboard_manager = ClipboardManager()
    clipboard_manager.place_window()

    def background():
        while True:
            clipboard_manager.clip()


    b = threading.Thread(name='background', target=background)

    b.start()
    clipboard_manager.run()