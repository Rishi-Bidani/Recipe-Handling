import tkinter as tk
from tkinter import ttk

"""
This will will be used for opening up a recipe from the 
list box under Search recipes
"""

WIDTH = 900
HEIGHT = 700
titleFont = ("Arial", 16, "bold")


class CreateVerticalScrollRegion:
    def __init__(self, frame, canvascolor, scrollSide=tk.RIGHT):
        self.frame = frame
        self.canvascolor = canvascolor
        self.scrollSide = scrollSide

        self.canvas = tk.Canvas(self.frame)
        self.canvasFrame = tk.Frame(self.canvas)
        self.yscroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)

        self.yscroll.pack(side=self.scrollSide, fill="y")
        self.canvas.pack(side=self.scrollSide, fill="both", expand="yes")
        self.canvas.config(bg=self.canvascolor)
        self.canvasFrame.config(bg=self.canvascolor)
        self.canvas.configure(yscrollcommand=self.yscroll.set)
        self.canvas.create_window((0, 0), window=self.canvasFrame, anchor="nw")

    def bindScrollAction(self):
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def removeScroll(self):
        self.yscroll.pack_forget()

    def returnFrame(self):
        return self.canvasFrame


class ListCheck:
    def __init__(self, win, relX=0.1, relY=0.05, relW=0.5, relH=0.5):
        self.win = win
        self.listcheck_frame = tk.Frame(self.win)
        self.listcheck_frame.config(bg="white")

        self.scrollReg = CreateVerticalScrollRegion(self.listcheck_frame, "white", tk.LEFT)
        self.mainFrame = self.scrollReg.returnFrame()

        # self.canvas = tk.Canvas(self.listcheck_frame)
        # self.yscroll = ttk.Scrollbar(self.listcheck_frame, orient="vertical", command=self.canvas.yview)
        # self.mainFrame = tk.Frame(self.canvas)
        self.relX = relX
        self.relY = relY
        self.relW = relW
        self.relH = relH
        self.listcheck_frame.place(relx=self.relX, rely=self.relY, relwidth=self.relW, relheight=self.relH)

    def createWin(self, items):
        if items <= 10:
            self.scrollReg.removeScroll()
        else:
            self.scrollReg.bindScrollAction()

    # def createWin(self, items):
    #     self.yscroll.pack(side=tk.RIGHT, fill="y")
    #     self.canvas.pack(side=tk.LEFT, fill="both", expand="yes")
    #     self.canvas.config(bg="white")
    #     self.canvas.configure(yscrollcommand=self.yscroll.set)
    #     self.mainFrame.config(bg="white")
    #     if items <= 10:
    #         # self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    #         pass
    #     else:
    #         self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    #     self.canvas.create_window((0, 0), window=self.mainFrame, anchor="nw")
    #
    #     self.listcheck_frame.place(relx=self.relX, rely=self.relY, relwidth=self.relW, relheight=self.relH)

    def insertRow(self, text):
        c1 = tk.Checkbutton(self.mainFrame, text=text, onvalue=1, offvalue=0)
        c1.pack(side=tk.TOP, anchor="w", expand="yes")
        # canvasWidth = (self.relW*(self.canvas.winfo_screenwidth()/4))
        canvasWidth = 500
        c1.configure(font=("Arial", 16), bg="white", wraplength=canvasWidth, justify="left", pady=10)


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
        self.topframe.place(x=0, y=0, relwidth=1, relheight=0.08)

        self.leftframe.place(x=0, rely=0.05, relheight=(1 - 0.05), relwidth=0.4)
        # self.leftframe.config(bg="red")

        self.rightframe.place(relx=0.4, rely=0.05, relwidth=0.6, relheight=(1 - 0.05))

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
        # ing_list = self.ingredients[0][0].split("\n")
        ing_list = [i.strip() for i in self.ingredients[0][0].split("\n") if len(i) > 1]
        # print(ing_list)
        lc.createWin(len(ing_list))

        for i in range(len(ing_list)):
            lc.insertRow(f"{ing_list[i]}")
        # for i in range(30):
        #     lc.insertRow(f"testt ttttt tttttt tttttttt tttttt ttttttttttttttttttttttttt{i}")

    def new_window(self):
        self.gui.geometry(f"{WIDTH}x{HEIGHT}")
        self.gui.title(self.title)
        self.gui.mainloop()

# a = DisplayRecipe("Soup", "b", "c")
# a.ready()
