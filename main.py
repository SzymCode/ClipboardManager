import threading
import tkinter as tk
from tkinter import RIGHT, Y, LEFT, BOTH

import pyperclip

BG_COLOR = "#e3e3e3"


class ClipboardManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.iconbitmap("images/favicon.ico")
        self.is_copied_from_window = False

        scrollbar = tk.Scrollbar()
        scrollbar.pack(side=RIGHT, fill=Y)
        self.clip_list = tk.Listbox(self.window, bg=BG_COLOR, width=24, yscrollcommand=scrollbar.set)

        self.clip_list.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.clip_list.yview)

        self.selection = self.clip_list.curselection()

    def place_window(self, width=165, height=115):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = screen_width - (width + 10.5)
        y = screen_height - (height + 73.5)
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def clip(self):
        if not (pyperclip.waitForNewPaste() == "") and not self.is_copied_from_window:
            clipboard = pyperclip.waitForPaste()
            header = f" {clipboard}"
            self.clip_list.insert(0, header)

        else:
            if self.is_copied_from_window:
                self.is_copied_from_window = False

    def callback(self, event):
        self.selection = self.clip_list.curselection()
        if self.selection:
            self.is_copied_from_window = True
            index = self.selection[0]
            data = self.clip_list.get(index)
            pyperclip.copy(f"{data}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    clipboard_manager = ClipboardManager()
    clipboard_manager.place_window()
    clipboard_manager.clip_list.bind("<<ListboxSelect>>", clipboard_manager.callback)

    def background():
        while True:
            clipboard_manager.clip()


    b = threading.Thread(name='background', target=background)

    b.start()
    clipboard_manager.run()