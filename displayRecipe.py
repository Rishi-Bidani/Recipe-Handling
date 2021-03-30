import tkinter as tk
from tkinter import ttk
"""
This will will be used for opening up a recipe from the 
list box under Search recipes
"""


WIDTH = 900
HEIGHT = 700
titleFont = ("Arial", 16, "bold")


class ListCheck:
    def __init__(self, win, relX=0.1, relY=0.05, relW=0.5, relH=0.5):
        self.win = win
        self.listcheck_frame = tk.Frame(self.win)
        self.listcheck_frame.config(bg="white")

        self.canvas = tk.Canvas(self.listcheck_frame)
        self.yscroll = ttk.Scrollbar(self.win, orient="vertical", command=self.canvas.yview)

        self.mainFrame = tk.Frame(self.canvas)
        self.relX = relX
        self.relY = relY
        self.relW = relW
        self.relH = relH

    def createWin(self, items):
        self.yscroll.pack(side=tk.RIGHT, fill="y")
        self.canvas.pack(side=tk.LEFT, fill="y")
        self.canvas.config(bg="white")
        self.canvas.configure(yscrollcommand=self.yscroll.set)
        if items <= 10:
            pass
        else:
            self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.mainFrame, anchor="nw")

        self.listcheck_frame.place(relx=self.relX, rely=self.relY, relwidth=self.relW, relheight=self.relH)

    def insertRow(self, text):
        c1 = tk.Checkbutton(self.mainFrame, text=text, onvalue=1, offvalue=0)
        c1.pack(anchor="w", fill="x")
        print(self.mainFrame.winfo_width())
        c1.configure(font=("Arial", 16), bg="white", wraplength=250)


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
        self.ingred_win()
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

    def ingred_win(self):
        lc = ListCheck(self.leftframe, relX=0.05, relW=0.8, relH=0.9)
        lc.createWin(30)
        for i in range(30):
            lc.insertRow(f"testttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt{i}")

    def new_window(self):
        self.gui.geometry(f"{WIDTH}x{HEIGHT}")
        self.gui.title(self.title)
        self.gui.mainloop()


a = DisplayRecipe("Soup", "b", "c")
a.ready()