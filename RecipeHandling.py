import tkinter as tk
from tkinter import *
from tkinter import ttk
import pickle
import os
from os import path
from functools import partial

gui = Tk()
gui.geometry("700x700")
pagenumber = 1
InputOrSearch = False


class LabelWidget:
    def __init__(self, window, text, font, size, wraplength=None):
        self.window = window
        self.text = text
        self.font = font
        self.size = size
        self.wraplength = wraplength

    def Call(self):
        var = Label(self.window, text=self.text, wraplength=self.wraplength)
        var.config(font=(f'{self.font}', self.size))
        return var


class Input():
    recipeNames = []
    ingredients = {}
    fullRecipe = {'ingredients': "", 'procedure': ""}
    recipeNameInput = ""
    numOfIngredients = int()
    entriesOfIngredients = []
    entriesOfQuantity = []
    tempIngredients = []
    tempQuantity = []

    def __init__(self, screen):
        self.screen = screen

    def CheckPage(self, page, recipename=None, numofingredients=None, procedure=None):
        global InputOrSearch
        if page == 1:
            self.Clear()
            Input.recipeNames = []
            Input.ingredients = {}
            Input.fullRecipe = {'ingredients': "", 'procedure': ""}
            Input.recipeNameInput = ""
            Input.numOfIngredients = int()
            Input.entriesOfIngredients = []
            Input.entriesOfQuantity = []
            Input.tempIngredients = []
            Input.tempQuantity = []
            MainScreen()
        elif page == 2:
            self.Clear()
            self.InfoPage()
        elif page == 3:
            Input.recipeNameInput = recipename.get()
            Input.numOfIngredients = int(numofingredients.get())
            self.IngredientsAndQuantitiesPage(Input.recipeNameInput, Input.numOfIngredients)
        elif page == 4:
            procedure_list = [procedure.get("1.0", "end-1c")]
            Input.fullRecipe['procedure'] = procedure_list
            print(Input.fullRecipe)
            self.Save(Input.recipeNameInput)
            self.CheckPage(1)
        elif page == "4a":
            self.Clear()
            self.Procedure()
        else:
            InputOrSearch = True
            print(InputOrSearch)

    def Clear(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

    def Save(self, recipe_file):
        p = ".pickle"
        with open("RecipeNames.pickle", "wb") as r:
            pickle.dump(self.recipeNames, r)

        recipe_file += p
        with open(f'{recipe_file}', "wb") as rf:
            pickle.dump(self.fullRecipe, rf)

    def ListOfTuples(self, l1, l2):
        return list(map(lambda x, y: (x, y), l1, l2))

    def InfoPage(self):  # Page 2
        title_infoPage = LabelWidget(self.screen, "Enter Recipes", "Courier", 44)
        title_infoPage.Call().place(x="140", y="10")

        recipe_name = LabelWidget(self.screen, "Recipe Name: ", "Courier", 18)
        recipe_name.Call().place(x="70", y="190")

        recipe_name_input = Entry(self.screen)
        recipe_name_input.place(x="270", y="196", width="350", height="25")

        num_ingredients = LabelWidget(self.screen, "Enter Number of Ingredients: ", "Courier", 18)
        num_ingredients.Call().place(x="70", y="300")

        num_ingredients_input = Entry(self.screen)
        num_ingredients_input.place(x="470", y="305", height="25", width="150")

        submit = Button(self.screen, text="Next", padx="50", pady="20", bg="lightgrey",
                        command=partial(self.CheckPage, 3, recipe_name_input, num_ingredients_input))
        submit.place(x="290", y="420")

    def IngredientsAndQuantitiesPage(self, thisRecipeName, numofingredients):  # Page 3
        self.Clear()
        counter = 1
        # ---------------- layout ------------------------

        ingredient_label = LabelWidget(self.screen, "Ingredients", "Courier", 24)
        quantity_label = LabelWidget(self.screen, "Quantity", "Courier", 24)

        submit_ingredients = Button(self.screen, text="Next", padx="50", pady="20", bg="lightgrey",
                                    command=self.EnterIngredients)
        # ------------------end layout -------------------

        # ------------ you can only enter 15 ingredients -------
        numofingredients = int(numofingredients)
        if numofingredients > 15:
            numofingredients = 15
        else:
            pass
        # -------------------------------------------------------
        if thisRecipeName not in Input.recipeNames:
            Input.recipeNames.append(thisRecipeName)
            self.Save(thisRecipeName)
        elif counter <= 5:
            thisRecipeName += f"({counter})"
            if thisRecipeName not in Input.recipeNames:
                Input.recipeNames.append(thisRecipeName)
                # current_recipe_name = thisRecipeName
                Input.recipeNameInput = thisRecipeName
                self.Save(Input.recipeNameInput)
            else:
                counter += 1
        else:
            gui.destroy()

        # --------------- current layout -----------
        ingredient_label.Call().place(x="50", y="30")
        quantity_label.Call().place(x="500", y="30")
        submit_ingredients.place(x="300", y="500")

        # ----- place the entries
        for i in range(numofingredients):
            entriesforingredients = Entry(gui)
            entriesforquantity = Entry(gui)
            distance = (100 + (40 * i))
            entriesforingredients.place(x="50", y=f"{distance}")
            entriesforquantity.place(x="500", y=f"{distance}")
            Input.entriesOfIngredients.append(entriesforingredients)
            Input.entriesOfQuantity.append(entriesforquantity)
        # ===================== end =====================

    def EnterIngredients(self):  # Creates and saves a list of tuples of the ingredients

        # ---------- ingredients without empty strings-----
        for entry in Input.entriesOfIngredients:
            Input.tempIngredients.append(entry.get())
        ingredients = list(filter(None, Input.tempIngredients))
        # --- quantity with empty string
        for entry in Input.entriesOfQuantity:
            Input.tempQuantity.append(entry.get())
        quantity = list(filter(None, Input.tempQuantity))
        # ===================================================

        ingredientsAndquantity = self.ListOfTuples(ingredients, quantity)
        Input.fullRecipe['ingredients'] = ingredientsAndquantity
        self.Save(Input.recipeNameInput)
        # self.Procedure()
        self.CheckPage("4a")

    def Procedure(self):

        textfield = Text(gui, height=30, width=82)
        textfield.place(x="20", y="100")

        procedure_label = LabelWidget(self.screen, "Procedure", "Courier", 40)
        procedure_label.Call().place(x="220", y="20")

        button_save = Button(gui, text="Next", padx="50", pady="20", bg="lightgrey",
                             command=partial(self.CheckPage, 4, procedure=textfield))
        button_save.place(x="250", y="600")


class Search:
    searchpage = 1

    def __init__(self, screen):
        self.screen = screen

    def CheckPage(self, page, optmenu=None):
        if page == 1:
            self.Clear()
            self.search_menu()
        elif page == 2:
            self.choose_file()
        elif page == 3:
            print(optmenu.get())
            self.display(optmenu)

    def Clear(self):
        for widget in self.screen.winfo_children():
            widget.destroy()

    def search_menu(self):
        browse_all_files_button = Button(gui, text="Choose File", padx="50", pady="20", bg="lightgrey",
                                         command=partial(self.CheckPage, 2))
        browse_all_files_button.place(x=300, y=300)

    def choose_file(self):
        self.Clear()

        folder = os.getcwd()
        filelist = [fname for fname in os.listdir(folder) if fname.endswith('.pickle')]

        optionsmenu = ttk.Combobox(gui, values=filelist, state='readonly')
        optionsmenu.place(x=300, y=300)

        display_button = Button(gui, text="Show Recipe", padx="50", pady="20", bg="lightgrey",
                                command=partial(self.CheckPage, 3, optionsmenu))
        display_button.place(x=300, y=500)

    def display(self, optionsmenu):
        root = Tk()
        root.geometry("1000x700")

        recipename = optionsmenu.get()
        recipetitle = LabelWidget(root, f'{recipename}', "Courier", 18)
        recipetitle.Call().place(x=450, y=17)

        with open(f'{recipename}', "rb") as thisfile:
            fullDict = pickle.load(thisfile)

        # ------------- dict => list ------------------
        fullDictIngred = fullDict['ingredients']
        fullDictProc = fullDict['procedure']
        # ---------------------------------------------

        labelIngredients = LabelWidget(root, "Ingredients: ", "Courier", 20)
        labelIngredients.Call().place(x=20, y=50)

        text = (', '.join(f"({', '.join(str(x) for x in item)})" for item in fullDictIngred))
        text_label = LabelWidget(root, text, "Courier", 12, 700)
        text_label.Call().place(x="220", y="60")

        # ------------------ procedure label ------------------
        labelProcedure = LabelWidget(root, "Procedure: ", "Courier", 20)
        labelProcedure.Call().place(x=20, y=200)
        # -----------------------------------------------------
        # -------------- procedure text -----------------------
        proc_text_label = ""
        for i in fullDictProc:
            proc_text_label_temp = Label(root, text=i, wraplength=900)
            proc_text_label = proc_text_label_temp
        proc_text_label.config(font=("Courier", 12))
        proc_text_label.place(x=70, y=250)
        # -----------------------------------------------------


inputscreen = Input(gui)
searchscreen = Search(gui)


def MainScreen():  # Page 1
    global pagenumber

    if path.exists('RecipeNames.pickle'):
        with open("RecipeNames.pickle", "rb") as r:
            Input.recipeNames = pickle.load(r)

    if not path.exists('RecipeNames.pickle'):
        with open("RecipeNames.pickle", "wb") as r:
            Input.recipeNames = []
            pickle.dump(Input.recipeNames, r)

    button_search = Button(gui, text="Search", padx="50", pady="25", bg="lightgrey",
                           command=partial(searchscreen.CheckPage, 1))

    button_input = Button(gui, text="Input", padx="50", pady="25", bg="lightgrey",
                          command=partial(inputscreen.CheckPage, 2))

    button_search.config(font=("Courier", 10))
    button_input.config(font=("Courier", 10))

    button_search.place(x="150", y="350")
    button_input.place(x="400", y="350")


MainScreen()

gui.mainloop()
