import tkinter as tk
from tkhtmlview import HTMLLabel

"""
This will will be used for opening up a recipe from the 
list box under Search recipes
"""


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
        html_label = HTMLLabel(gui,
                               html=""
                                    f"<h1 style='color: red; text-align: center'>{self.title}</H1>"
                                    f"<div style='text-align:right'> {self.ingredients} </div>"
                                    "")
        html_label.pack(fill="both", expand=True)
        html_label.fit_height()
        gui.mainloop()


a = DisplayRecipe("a", "b", "c")