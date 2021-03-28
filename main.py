import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
from os import path
from functools import partial
import sqlite3

# gui = Tk()
HEIGHT = 700
WIDTH = 900

conn = sqlite3.connect('recipes.db')

conn.execute('''CREATE TABLE IF NOT EXISTS recipes
         (id INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         title           TEXT    NOT NULL,
         ingredients     TEXT     NOT NULL,
         procedure        TEXT);''')

# conn.execute('''CREATE TABLE IF NOT EXISTS tags
#          (id INT PRIMARY  KEY     NOT NULL,
#          tag              TEXT    NOT NULL,
#          titles           TEXT);
# ''')

buttonFont = ("Arial", 10, "bold")
headingFont = ("Arial", 24, "bold")
titleFont = ("Arial", 16, "bold")


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.titleEntry = Entry(self)
        self.textIngredients = Text(self)
        self.textProcedure = Text(self)
        self.displayPage()

    def displayPage(self):
        label = tk.Label(self, text="Enter Recipe")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)

        recipeTitleLabel = tk.Label(self, text="Recipe Title: ")
        recipeTitleLabel.place(x=20, rely=0.1)
        recipeTitleLabel.configure(font=titleFont)

        self.titleEntry.place(x=160, rely=0.1, relwidth=0.5, height=25)

        IngredientsLabel = tk.Label(self, text="Ingredients")
        IngredientsLabel.place(x=20, rely=0.18)
        IngredientsLabel.configure(font=titleFont)

        scroll = Scrollbar(self, command=self.textIngredients.yview)
        self.textIngredients.configure(yscrollcommand=scroll.set)

        self.textIngredients.place(x=20, rely=0.23, relwidth=0.5, relheight=0.25)

        procedureLabel = tk.Label(self, text="Procedure: ")
        procedureLabel.place(x=20, rely=0.5)
        procedureLabel.configure(font=titleFont)

        scroll = Scrollbar(self, command=self.textProcedure.yview)

        self.textProcedure.configure(yscrollcommand=scroll.set)
        self.textProcedure.place(x=20, rely=0.55, relwidth=0.9, relheight=0.4)

        saveCommand = partial(self.getTextInfo, self.titleEntry, self.textIngredients, self.textProcedure)
        saveButton = Button(self, text="Save", command=saveCommand)
        saveButton.configure(font=buttonFont)
        saveButton.place(relx=0.87, rely=0.01, relwidth=0.1, relheight=0.05)

    def getTextInfo(self, title, ingredients, procedure):
        title = title.get()
        ingredients = ingredients.get("1.0", 'end-1c')
        procedure = procedure.get("1.0", 'end-1c')
        print(title, ingredients, procedure)
        if len(title) > 5 and \
                (len(ingredients) - (ingredients.count(' ') + ingredients.count('\n')) > 10):
            self.clearInputBoxes()
            self.insertIntoTable(title, ingredients, procedure)
        else:
            messagebox.showwarning("Empty Insert",
                                   "Title should be longer than 5 characters \n "
                                   "Ingredients should have more than 10 characters")

    def insertIntoTable(self, title, ingredients, procedure):
        cur = conn.cursor()
        cur.execute('INSERT INTO "recipes" ("title", "ingredients", "procedure") VALUES(?,?,?);',
                    (title, ingredients, procedure))
        conn.commit()
        cur.close()

    def clearInputBoxes(self):
        self.titleEntry.delete(0, 'end')
        self.textIngredients.delete("1.0","end")
        self.textProcedure.delete("1.0","end")


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Search Recipes")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Favourites")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)


class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Recents")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        sidebar = tk.Frame(gui, width=WIDTH / 5, bg='#9ddfd3', height=2 * HEIGHT, borderwidth=2)
        sidebar.place(x=0, y=0)

        p1.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        p2.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        p3.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        p4.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)

        b1 = Button(text="Add Recipe", width=20, height=5, command=p1.lift)
        b2 = Button(text="Search Recipe", width=20, height=5, command=p2.lift)
        b3 = Button(text="Favourites", width=20, height=5, command=p3.lift)
        b4 = Button(text="Recents", width=20, height=5, command=p4.lift)

        p1.show()

        b1.place(in_=sidebar, anchor="c", relx=0.5, rely=0.15)
        b2.place(in_=sidebar, anchor="c", relx=0.5, rely=0.225)
        b3.place(in_=sidebar, anchor="c", relx=0.5, rely=0.30)
        b4.place(in_=sidebar, anchor="c", relx=0.5, rely=0.375)
        b1.configure(font=buttonFont, relief="solid", borderwidth=2)
        b2.configure(font=buttonFont, relief="solid", borderwidth=2)
        b3.configure(font=buttonFont, relief="solid", borderwidth=2)
        b4.configure(font=buttonFont, relief="solid", borderwidth=2)


if __name__ == "__main__":
    gui = Tk()
    gui.geometry(f"{WIDTH}x{HEIGHT}")
    gui.title("Recipe Manger")
    main = MainView(gui)
    main.pack(side="top", fill="both", expand=True)
    gui.mainloop()
