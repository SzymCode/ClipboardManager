import os
import threading
import tkinter as tk
from tkinter import RIGHT, Y, LEFT, BOTH, END, Tk, Scrollbar, Listbox, Menu, Event
import pyperclip


class ClipboardManager:
    def __init__(self):
        self.window: Tk = tk.Tk()
        self.window.resizable(False, False)
        self.window.iconbitmap("images/favicon.ico")
        self.is_copied_from_window: bool = False
        self.BG_COLOR: str = "#e3e3e3"

        scrollbar: Scrollbar = tk.Scrollbar()
        scrollbar.pack(side=RIGHT, fill=Y)

        self.clip_list: Listbox = tk.Listbox(self.window, bg=self.BG_COLOR, width=24, yscrollcommand=scrollbar.set)
        self.clip_list.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.clip_list.yview)

        self.selection: None = self.clip_list.curselection()

        self.popup_menu: Menu = tk.Menu(self.window, tearoff=0)
        self.popup_menu.add_command(label="Delete",
                                    command=lambda: self.delete())
        self.popup_menu.add_command(label="Open saving file",
                                    command=lambda: os.system("history.txt"))

        self.clip_list.bind("<Button-3>", self.do_popup)
        self.clip_list.bind("<Double-Button-1>", self.double_click)

        if not os.path.exists("history.txt"):
            self.HistoryFile = open("history.txt", "a+")

    def place_window(self, width: int = 165, height: int = 115) -> None:
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = screen_width - (width + 10.5)
        y = screen_height - (height + 73.5)
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def clip(self) -> None:
        if not (pyperclip.waitForNewPaste() == "") and not self.is_copied_from_window:
            clipboard = pyperclip.waitForPaste().replace('\r', '')
            header = f"{clipboard}"
            self.clip_list.insert(0, header)
            with open('history.txt', 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f"{clipboard}" + '\n$CLIP_END$\n' + content)

        else:
            if self.is_copied_from_window:
                self.is_copied_from_window = False

    def double_click(self, event) -> None:
        self.selection = self.clip_list.curselection()
        if self.selection:
            self.is_copied_from_window = True
            index = self.selection[0]
            data = self.clip_list.get(index)
            pyperclip.copy(f"{data}")

    def read(self) -> None:
        with open("history.txt") as f:
            result = ""
            for line in f:
                if f"{'$CLIP_END$'}" in line:
                    self.clip_list.insert(0, result)
                    result = ''
                else:
                    result += line

    def delete(self) -> None:
        self.selection = self.clip_list.curselection()
        if self.selection:
            index = self.selection[0]
            self.clip_list.delete(index)
            result = ""
            with open("history.txt") as f:
                for line in f:
                    result += line

            with open("history.txt", "w") as f:
                for line in self.clip_list.get(0, END):
                    f.write(line + '\n$CLIP_END$\n')

    def do_popup(self, event: Event) -> None:
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def run(self) -> None:
        self.window.mainloop()


if __name__ == "__main__":
    clipboard_manager = ClipboardManager()
    clipboard_manager.place_window()
    clipboard_manager.read()


    def background():
        while True:
            clipboard_manager.clip()

    b = threading.Thread(name='background', target=background)
    b.start()

    clipboard_manager.run()