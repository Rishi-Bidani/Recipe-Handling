from tkinter import *
from tkinter import messagebox
import os
from functools import partial
import sqlite3

HEIGHT = 700
WIDTH = 900

if os.name == "nt":
    path = os.getenv("LOCALAPPDATA")
    directory = "RecipeManager"
    pathWithDir = os.path.join(path, directory)
    try:
        os.mkdir(pathWithDir)
    except OSError as e:
        # Expected Error:
        # [WinError 183] Cannot create a file when that file already exists:
        # 'C:\\Users\\username\\AppData\\Local\\RecipeManager'
        pass

    conn = sqlite3.connect(os.path.join(pathWithDir,'recipes.db'))

else:
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
        label = Label(self, text="Search Recipes")
        label.place(relwidth=1, anchor=NW)
        label.configure(font=headingFont)
        self.titles = []
        self.displayPage()

    def displayPage(self):
        self.queryRecipeTitles()
        listbox = Listbox(self, bg="white", fg="green",
                          font="Helvetica", highlightcolor="green")
        for i in range(len(self.titles)):
            listbox.insert(i+1, self.titles[i][0])
        listbox.yview()
        listbox.place(x=20, rely=0.1, relheight=0.8, relwidth=0.5)

    def queryRecipeTitles(self):
        cur = conn.cursor()
        cur.execute("SELECT title FROM recipes ORDER BY title ASC")
        rows = cur.fetchall()
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
        page1Lift = partial(self.liftWhichPage, 1)
        page2Lift = partial(self.liftWhichPage, 2)
        page3Lift = partial(self.liftWhichPage, 3)
        page4Lift = partial(self.liftWhichPage, 4)

        b1 = Button(text="Add Recipe", width=20, height=5, command=page1Lift)
        b2 = Button(text="Search Recipe", width=20, height=5, command=page2Lift)
        b3 = Button(text="Favourites", width=20, height=5, command=page3Lift)
        b4 = Button(text="Recents", width=20, height=5, command=page4Lift)

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
