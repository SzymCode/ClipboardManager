import tkinter as tk


class Clipboard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)

    def place_window(self, width=200, height=115):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = screen_width - (width + 10.5)
        y = screen_height - (height + 73.5)
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    clipboard = Clipboard()
    clipboard.place_window()
    clipboard.run()