import sqlite3
from tkinter import *
from tkinter import messagebox
import os
from functools import partial
import handleSQL
from handleSQL import SQLQueries
import displayRecipe
from displayRecipe import DisplayRecipe

HEIGHT = 700
WIDTH = 900

buttonFont = ("Arial", 10, "bold")
headingFont = ("Arial", 24, "bold")
titleFont = ("Arial", 16, "bold")


class LabelWidget:
    def __init__(self, screen, text, font, x=0, y=0, relx=0.0, rely=0.0):
        self.screen = screen
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.relx = relx
        self.rely = rely

    def placeLabel(self):
        thisLabel = Label(self.screen, text=self.text)
        thisLabel.place(x=self.x, y=self.y, relx=self.relx, rely=self.rely)
        thisLabel.configure(font=self.font)


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.titleEntry = Entry(self)
        self.textIngredients = Text(self)
        self.textProcedure = Text(self)
        self.displayLabels()
        self.displayPage()

    def displayLabels(self):
        label = Label(self, text="Enter Recipe")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)

        # Label for Recipe Title
        LabelWidget(self, "Recipe Title: ", titleFont,
                    x=20, rely=0.1).placeLabel()

        # Label for Ingredients
        LabelWidget(self, "Ingredients: ", titleFont,
                    x=20, rely=0.18).placeLabel()

        # Label for Procedure
        LabelWidget(self, "Procedure: ", titleFont,
                    x=20, rely=0.5).placeLabel()

    def displayPage(self):

        self.titleEntry.place(x=160, rely=0.1, relwidth=0.5, height=25)

        scroll = Scrollbar(self, command=self.textIngredients.yview)
        self.textIngredients.configure(yscrollcommand=scroll.set)

        self.textIngredients.place(x=20, rely=0.23, relwidth=0.5, relheight=0.25)

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
        # print(title, ingredients, procedure)
        if len(title) > 5 and \
                (len(ingredients) - (ingredients.count(' ') + ingredients.count('\n')) > 10):
            self.insertIntoTable(title, ingredients, procedure)
        else:
            messagebox.showwarning("Empty Insert",
                                   "Title should be longer than 5 characters \n "
                                   "Ingredients should have more than 10 characters")

    def insertIntoTable(self, title, ingredients, procedure):
        insertQuery = SQLQueries("INSERT INTO '{0}' ('title', 'ingredients', 'procedure') VALUES('{1}','{2}','{3}')". \
                                 format("recipes", title, ingredients, procedure))
        try:
            insertQuery.insertIntoTable()
            self.clearInputBoxes()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate", "Please Insert A unique Recipe Title")

    def clearInputBoxes(self):
        self.titleEntry.delete(0, 'end')
        self.textIngredients.delete("1.0", "end")
        self.textProcedure.delete("1.0", "end")


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="Search Recipes")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)
        self.titles = []
        self.listbox = Listbox(self, bg="white", fg="green",
                               font="Helvetica", highlightcolor="green")
        self.displayPage()

    def displayPage(self):
        self.queryRecipeTitles()
        self.listbox.delete(0, 'end')
        for i in range(len(self.titles)):
            self.listbox.insert(i + 1, self.titles[i][0])
        self.listbox.bind('<Double-1>', lambda x: self.listBoxSearch())
        self.listbox.yview()
        self.listbox.place(x=20, rely=0.1, relheight=0.8, relwidth=0.5)

    def listBoxSearch(self):
        cs = self.listbox.curselection()[0]
        # print(self.listbox.get(cs))
        disp = DisplayRecipe(self.listbox.get(cs), "Ing", "Procedure")
        disp.ready()

    def queryRecipeTitles(self):
        selectQuery = SQLQueries("SELECT title FROM recipes ORDER BY title ASC")
        rows = selectQuery.selectFromTable()
        # for i in rows:
        #     if i not in self.titles:
        #         self.titles.append(i)
        #     else:
        #         pass
        self.titles.extend(list(i for i in rows if i not in self.titles))


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="Favourites")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)


class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="Recents")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.sidebar = Frame(gui, width=WIDTH / 5, bg='#9ddfd3', height=2 * HEIGHT, borderwidth=2)
        self.sidebar.place(x=0, y=0)
        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.p3 = Page3(self)
        self.p4 = Page4(self)

        self.p1.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        self.p2.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        self.p3.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        self.p4.place(x=WIDTH / 5, y=0, relwidth=(1 - (1 / 5)), relheight=1)
        self.p1.show()
        self.sideNavButtons()

    def sideNavButtons(self):
        page1lift = partial(self.liftWhichPage, 1)
        page2lift = partial(self.liftWhichPage, 2)
        page3lift = partial(self.liftWhichPage, 3)
        page4lift = partial(self.liftWhichPage, 4)

        b1 = Button(text="Add Recipe", width=20, height=5, command=page1lift)
        b2 = Button(text="Search Recipe", width=20, height=5, command=page2lift)
        b3 = Button(text="Favourites", width=20, height=5, command=page3lift)
        b4 = Button(text="Recents", width=20, height=5, command=page4lift)

        b1.place(in_=self.sidebar, anchor="c", relx=0.5, rely=0.15)
        b2.place(in_=self.sidebar, anchor="c", relx=0.5, rely=0.225)
        b3.place(in_=self.sidebar, anchor="c", relx=0.5, rely=0.30)
        b4.place(in_=self.sidebar, anchor="c", relx=0.5, rely=0.375)
        b1.configure(font=buttonFont, relief="solid", borderwidth=2)
        b2.configure(font=buttonFont, relief="solid", borderwidth=2)
        b3.configure(font=buttonFont, relief="solid", borderwidth=2)
        b4.configure(font=buttonFont, relief="solid", borderwidth=2)

    def liftWhichPage(self, page):
        if page == 1:
            self.p1.lift()
        elif page == 2:
            self.p2.displayPage()
            self.p2.lift()
        elif page == 3:
            self.p3.show()
        elif page == 4:
            self.p4.show()
        else:
            pass


if __name__ == "__main__":
    gui = Tk()
    gui.geometry(f"{WIDTH}x{HEIGHT}")
    gui.title("Recipe Manger")
    main = MainView(gui)
    main.pack(side="top", fill="both", expand=True)
    gui.mainloop()
