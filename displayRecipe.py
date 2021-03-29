import tkinter as tk

WIDTH = 900
HEIGHT = 700


class DisplayRecipe:
    def __init__(self, title, ingredients, procedure):
        self.title = title
        self.ingredients = ingredients
        self.procedure = procedure
        self.new_window()

    def new_window(self):
        gui = tk.Tk()
        gui.geometry(f"{WIDTH}x{HEIGHT}")
        gui.title(self.title)
        gui.mainloop()




a = DisplayRecipe("a", "b", "c")