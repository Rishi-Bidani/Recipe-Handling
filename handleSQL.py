import sqlite3
import os

''''
This file will handle all the sql related tasks
It will also create the database under APPDATA/Local9RecipeManager on windows
'''


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
         title           TEXT   UNIQUE             NOT NULL,
         ingredients     TEXT     NOT NULL,
         procedure        TEXT);''')

# conn.execute('''CREATE TABLE IF NOT EXISTS tags
#          (id INT PRIMARY  KEY     NOT NULL,
#          tag              TEXT    NOT NULL,
#          titles           TEXT);
# ''')

class SQLQueries:
    def __init__(self, query):
        self.query = query

    def insertIntoTable(self):
        cur = conn.cursor()
        cur.execute(self.query)
        conn.commit()
        cur.close()

    def selectFromTable(self):
        cur = conn.cursor()
        cur.execute(self.query)
        returnData = cur.fetchall()
        cur.close()
        return returnData
