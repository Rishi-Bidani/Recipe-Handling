import tkinter as tk
# from tkhtmlview import HTMLLabel
# from main import LabelWidget
"""
This will will be used for opening up a recipe from the 
list box under Search recipes
"""


WIDTH = 900
HEIGHT = 700
titleFont = ("Arial", 16, "bold")


class DisplayRecipe:
    def __init__(self, title, ingredients, procedure):
        self.title = title
        self.ingredients = ingredients
        self.procedure = procedure
        self.gui = tk.Tk()
        self.topframe = tk.Frame(self.gui)
        self.leftframe = tk.Frame(self.gui)
        self.rightframe = tk.Frame(self.gui)

    def ready(self):
        self.createFrames()
        self.titleLabels()
        self.new_window()

    def createFrames(self):
        # self.topframe.pack(side="top")
        self.topframe.place(x=0,y=0, relwidth=1, relheight=0.08)

        self.leftframe.place(x=0, rely=0.05, relheight=(1-0.05), relwidth=0.4)
        # self.leftframe.config(bg="red")

        self.rightframe.place(relx=0.4, rely=0.05, relwidth=0.6, relheight=(1-0.05))

    def titleLabels(self):
        recipeTitleLabel = tk.Label(self.topframe, text=self.title)
        recipeTitleLabel.pack()
        recipeTitleLabel.config(font=titleFont, fg="red")

        ingTitleLabel = tk.Label(self.leftframe, text="Ingredients")
        # ingTitleLabel.place(anchor="n")
        ingTitleLabel.pack(side="left", anchor="n", padx=20)
        ingTitleLabel.config(font=titleFont)
        
        procTitleLabel = tk.Label(self.rightframe, text="Procedure")
        procTitleLabel.pack(side="left", anchor="nw", padx=20)
        procTitleLabel.config(font=titleFont)

    def new_window(self):
        self.gui.geometry(f"{WIDTH}x{HEIGHT}")
        self.gui.title(self.title)
        # html_label = HTMLLabel(gui,
        #                        html=""
        #                             f"<h1 style='color: red; text-align: center'>{self.title}</H1>"
        #                             f"<div style='text-align:right'> {self.ingredients} </div>"
        #                             "")
        # html_label.pack(fill="both", expand=True)
        # html_label.fit_height()
        self.gui.mainloop()


# a = DisplayRecipe("Soup", "b", "c")