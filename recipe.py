import tkinter as tk
from tkinter import *
from tkinter import ttk
import pickle
import os
from os import path

gui = Tk()

gui.geometry("700x700")
title = Label(gui, text="Recipes")
title.config(font=("Courier", 44))
title.place(x="225", y="10")

entries_ingred = []
entries_quantity = []
ing = []
qty = []

recipeNames = []
ingredients = {}
fullRecipe = {'ingredients': "", 'procedure': ""}

current_recipe_name = ""


# --------------------------------------

# if path.exists('RecipeNames.pickle'):
#     with open("RecipeNames.pickle", "rb") as r:
#         recipeNames = pickle.load(r)
#         print(recipeNames)
#
# if not path.exists('RecipeNames.pickle'):
#     with open("RecipeNames.pickle", "wb") as r:
#         recipeNames = []
#         pickle.dump(recipeNames, r)
#

# ----------------------------------------


def mainpage():
    forget()
    restart()
    button_search.place(x="150", y="350")
    button_input.place(x="400", y="350")


def enter():
    button_search.place_forget()
    button_input.place_forget()
    title_enter.place(x="140", y="10")

    recipe_name.place(x="70", y="190")
    recipe_name_input.place(x="270", y="196", width="350", height="25")

    num_ingredients.place(x="70", y="300")
    num_ingredients_input.place(x="470", y="305", height="25", width="150")

    submit.place(x="290", y="420")


def enter_all():
    global current_recipe_name
    counter = 1
    # --------- remove previous layout ---------
    title.place_forget()
    title_enter.place_forget()
    recipe_name.place_forget()
    recipe_name_input.place_forget()
    num_ingredients.place_forget()
    num_ingredients_input.place_forget()
    submit.place_forget()
    # -------------------------------------------

    r_name = recipe_name_input.get()
    current_recipe_name = r_name

    # ------------ you can only enter 15 ingredients -------
    num_ing = int(num_ingredients_input.get())
    if num_ing > 15:
        num_ing = 15
    else:
        pass
    # -------------------------------------------------------

    # ---------------- check if recipe exists ---------------
    if r_name not in recipeNames:
        recipeNames.append(r_name)
        save(current_recipe_name)
    elif counter <= 5:
        r_name += f"({counter})"
        if r_name not in recipeNames:
            recipeNames.append(r_name)
            current_recipe_name = r_name
            save(current_recipe_name)
        else:
            counter += 1
    else:
        gui.destroy()
    # -----------------
    # -----------------------------------------

    # --------------- current layout -----------
    ingredient_label.place(x="50", y="30")
    quantity_label.place(x="500", y="30")
    submit_ingredients.place(x="300", y="500")

    # ------------ place the entries
    for i in range(num_ing):
        en = Entry(gui)
        en2 = Entry(gui)
        dist = (100 + (40 * i))
        en.place(x="50", y=f"{dist}")
        en2.place(x="500", y=f"{dist}")
        entries_ingred.append(en)
        entries_quantity.append(en2)
    # ========================================


def enter_ingredients():
    r_name = recipe_name_input.get()
    # ---------- ingredients without empty strings-----
    for entry in entries_ingred:
        ing.append(entry.get())
    new_ing = list(filter(None, ing))
    # --- quantity with empty string
    for entry in entries_quantity:
        qty.append(entry.get())
    new_qty = list(filter(None, qty))
    # ===================================================

    # print(listOfTuples(new_ing, new_qty))
    ing_and_qty = listOfTuples(new_ing, new_qty)
    fullRecipe['ingredients'] = ing_and_qty
    save(current_recipe_name)
    procedure()


def procedure():
    # --------------- remove previous layout ---------------
    forget()
    for entries in entries_ingred:
        entries.place_forget()
    for entries2 in entries_quantity:
        entries2.place_forget()
    # -------------------------------------------------------
    textfield.place(x="20", y="100")
    procedure_label.place(x="220", y="20")
    button_save.place(x="250", y="600")


def listOfTuples(l1, l2):
    return list(map(lambda x, y: (x, y), l1, l2))


def temp_save():
    temp_procedure = []
    proc = textfield.get("1.0", "end-1c")
    temp_procedure.append(proc)
    fullRecipe['procedure'] = temp_procedure
    print(fullRecipe)
    save(current_recipe_name)
    mainpage()


def save(recipe_file):
    p = ".pickle"
    with open("RecipeNames.pickle", "wb") as r:
        pickle.dump(recipeNames, r)

    recipe_file += p
    with open(f'{recipe_file}', "wb") as rf:
        pickle.dump(fullRecipe, rf)


def forget():
    title.place_forget()
    button_save.place_forget()
    button_input.place_forget()
    button_search.place_forget()
    title_enter.place_forget()
    recipe_name.place_forget()
    recipe_name_input.place_forget()
    num_ingredients.place_forget()
    num_ingredients_input.place_forget()
    submit.place_forget()
    quantity_label.place_forget()
    ingredient_label.place_forget()
    submit_ingredients.place_forget()
    textfield.place_forget()
    procedure_label.place_forget()
    browse_all_files_button.place_forget()
    display_button.place_forget()
    optmenu.place_forget()

    # recipe_name_input.delete(1.0, tk.END)
    # num_ingredients_input.delete(1.0, tk.END)
    textfield.delete(1.0, tk.END)


def restart():
    global entries_ingred
    global entries_quantity
    global ing
    global qty
    global recipeNames
    global fullRecipe
    global current_recipe_name

    entries_ingred = []
    entries_quantity = []
    ing = []
    qty = []

    recipeNames = []

    fullRecipe = {'ingredients': "", 'procedure': ""}

    current_recipe_name = ""
    # -----------------------------------------------
    if path.exists('RecipeNames.pickle'):
        with open("RecipeNames.pickle", "rb") as r:
            recipeNames = pickle.load(r)
            print(recipeNames)

    if not path.exists('RecipeNames.pickle'):
        with open("RecipeNames.pickle", "wb") as r:
            recipeNames = []
            pickle.dump(recipeNames, r)
    # --------------------------------------------------


def search_menu():
    forget()
    browse_all_files_button.place(x=300, y=300)


def choose_file():
    forget()
    optmenu.place(x=300, y=300)
    display_button.place(x=300, y=500)


def display():
    forget()
    print("reached")
    fullDict = ""
    recipename = optmenu.get()
    recipetitle = Label(gui, text=f'{recipename}')
    recipetitle.config(font=("Courier", 18))
    recipetitle.place(x=320, y=20)
    with open(f'{recipename}', "rb") as thisfile:
        fullDict = pickle.load(thisfile)
    fullDictIngred = fullDict['ingredients']
    fullDictProc = fullDict['procedure']
    print(fullDictProc)
    print(fullDictIngred)


# -------- mainpage ----------------
button_search = Button(gui, text="Search", padx="50", pady="25", bg="lightgrey", command=search_menu)
button_input = Button(gui, text="Input", padx="50", pady="25", bg="lightgrey", command=enter)
button_search.config(font=("Courier", 10))
button_input.config(font=("Courier", 10))
# --------------end mainpage--------------

# ---------------- enter ---------------
title_enter = Label(gui, text="Enter Recipes")
title_enter.config(font=("Courier", 44))

recipe_name = Label(gui, text="Recipe Name: ")
recipe_name.config(font=("Courier", 18))
recipe_name_input = Entry(gui)

num_ingredients = Label(gui, text="Enter Number of Ingredients: ")
num_ingredients.config(font=("Courier", 18))
num_ingredients_input = Entry(gui)

submit = Button(gui, text="Next", padx="50", pady="20", bg="lightgrey", command=enter_all)
# ----------------- end enter -----------------

# ---------------- enter_all ------------------------
ingredient_label = Label(gui, text="Ingredients")
quantity_label = Label(gui, text="Quantity")
ingredient_label.config(font=("Courier", 24))
quantity_label.config(font=("Courier", 24))
submit_ingredients = Button(gui, text="Next", padx="50", pady="20", bg="lightgrey", command=enter_ingredients)
# ------------------end enter_all -------------------

# ----------------- procedure -------------
textfield = Text(gui, height=30, width=82)
button_save = Button(gui, text="Next", padx="50", pady="20", bg="lightgrey", command=temp_save)
procedure_label = Label(gui, text="Procedure")
procedure_label.config(font=("Courier", 40))
# -----------------------------------------


# =========================================================================


# ----------------------- search -----------------------------------------
browse_all_files_button = Button(gui, text="Choose File", padx="50", pady="20", bg="lightgrey", command=choose_file)
display_button = Button(gui, text="Show Recipe", padx="50", pady="20", bg="lightgrey", command=display)
folder = os.getcwd()
filelist = [fname for fname in os.listdir(folder) if fname.endswith('.pickle')]
optmenu = ttk.Combobox(gui, values=filelist, state='readonly')




mainpage()
gui.mainloop()

