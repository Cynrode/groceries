import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import Menu
from functools import partial


# Creates connection to database
class MainGui:
    def __init__(self, master):
        myFrame = tk.Frame(master)
        myFrame.pack
        top = tk.Frame(master)
        body = tk.Frame(master)
        bottom = tk.Frame(master)

        # Status bar
        self.statusBar = tk.Label(master, text='Working on it', bd=1, relief='sunken', anchor='w')

        master.geometry("625x550")
        master.title("Recipes to Groceries List")

        # Creating Menu Bar
        self.menubar = Menu(master)
        master.config(menu=self.menubar)
        file_menu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label='Exit',
            command=master.destroy,
        )
        # top
        self.instructions = tk.Label(top, text='We put the instructions here',
                                     font=25, padx=5, pady=5)
        # body
        self.recipesTitle = tk.Label(body, text='Recipes', font=("Arial", 15))
        self.groceryTitle = tk.Label(body, text='Grocery List', font=("Arial", 15))
        self.addRecipe = partial(addRecipe, )
        self.recListbox = tk.Listbox(body)
        self.recListbox.bind('<Double-Button-1>', addRecipe)
        self.glbList = []
        self.glbVar = tk.Variable(value='')
        self.grocListbox = tk.Listbox(body, listvariable=self.glbVar)
        # buttons
        self.add_recipe = tk.Button(body, text='Add Recipe')
        self.remove_recipe = tk.Button(body, text='Remove Recipe')
        self.add_item = tk.Button(body, text='Add Item')
        self.remove_item = tk.Button(body, text='Remove Item')
        # bottom
        self.frame = tk.Frame(bottom)
        self.textInfo = tk.Text(bottom, width=7, height=7)
        self.saveBut = tk.Button(bottom, text='Save')

        # grid
        # Top
        top.grid(row=0, column=0, sticky='nsew')
        self.instructions.grid(row=0, column=0, sticky='nw')

        body.grid(row=1, column=0, columnspan=2, sticky='nsew')
        # Left-side
        self.recipesTitle.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.recListbox.grid(row=1, column=0, columnspan=2, sticky='nsew',
                             padx=10)
        self.add_recipe.grid(row=2, column=0, sticky='e',
                             padx=5, pady=5)
        self.remove_recipe.grid(row=2, column=1, sticky='w',
                                padx=5, pady=5)
        # Right-side
        self.groceryTitle.grid(row=0, column=2, columnspan=2, sticky='ew')
        self.grocListbox.grid(row=1, column=2, columnspan=2, sticky='nsew',
                              padx=10)
        self.add_item.grid(row=2, column=2, sticky='e',
                           padx=5, pady=5)
        self.remove_item.grid(row=2, column=3, sticky='w',
                              padx=5, pady=5)

        # bottom
        bottom.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.textInfo.grid(row=0, column=1, columnspan=2, sticky='nsew')
        self.saveBut.grid(row=1, column=0, columnspan=3, pady=5)
        self.statusBar.grid(row=3, column=0, columnspan=2, sticky='we')

        # Geometry for dynamic resizing
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, weight=1)
        body.columnconfigure(3, weight=1)
        body.rowconfigure(1, weight=1)

        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.columnconfigure(2, weight=1)
        bottom.rowconfigure(0, weight=1)
        bottom.rowconfigure(1, weight=1)

        master.rowconfigure(1, weight=1)
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)


def read_dbinit_file():
    recipeList = []
    print('')
    with open('seedRecipes.txt') as file:
        # iterate through each line in the file
        for line in file:
            # separates each line into items using the ',' as a delimiter, strips the trailing space and saves it as
            # variable point
            recipe = line.strip('\n').split(',')
            recipeList.append(recipe)
    return recipeList


def create_connection():
    dbname = 'Grocery_DB'
    conn = None
    print(f'Establishing connection to {dbname}', end="... ")
    try:
        conn = sqlite3.connect(dbname)
    except Error as e:
        print(e)
    print('\t\tConnected')
    return conn


# verifies if table 'TblPoints' exists. If not, it creates it.
def create_project(conn):
    print('Verifying table initialization', end="... ")
    curs = conn.cursor()
    x = 'description TEXT NULL'
    for i in range(15):
        x += f',ingredient{i+1} TEXT NULL'
    sqlCmd = f'CREATE TABLE IF NOT EXISTS Recipes(title TEXT NOT NULL PRIMARY KEY,{x})'
    curs.execute(sqlCmd)


def lookAtDB(conn):
    curs = conn.cursor()
    curs.execute('SELECT * FROM Recipes ORDER BY description ASC')
    recipeRows = curs.fetchall()
    return recipeRows


def pullRecTitles(conn):
    curs = conn.cursor()
    sqlCmd = (f"SELECT title FROM Recipes ORDER BY description DESC")
    curs.execute(sqlCmd)
    titles = curs.fetchall()
    return titles


def pullRecIngredients(conn, recipeTitle='*'):
    curs = conn.cursor()
    x = 'ingredient1'
    for i in range(14):
        x += f',ingredient{i+1}'
    curs.execute(f'SELECT {x} WHERE title = "{recipeTitle}"')
    ingredientList = curs.fetchall()
    return ingredientList


def addRecipe(conn, recipeListFile):
    curs = conn.cursor()
    dbRecTitles = pullRecTitles(conn)
    recipeFileTitles = ([recipe[0] for recipe in recipeListFile])
    # Using list comprehension, we compile recipe titles into one list
    dbTitles = [title for title, in dbRecTitles]
    for recipeFileTitle in recipeFileTitles:
        # print(f'recipeFileTitle: {recipeFileTitle}'
        #      f'\ndbTitles: {dbTitles}\n')
        if recipeFileTitle in dbTitles:
            print(f'{recipeFileTitle} is already in the database')
            continue
        else:
            print(f'trying to add recipe {recipeFileTitle}')
            for recipe in recipeListFile:
                ingredientColumns = 'ingredient1'
                numArgs = '?,?,?'
                for j in range(1, len(recipe)-2):
                    ingredientColumns += f',ingredient{j + 1}'
                    numArgs += f',?'
                insert = f'INSERT INTO Recipes(title, description, {ingredientColumns})'
                sqlCmd = f'{insert} VALUES({numArgs})'
                curs.execute(sqlCmd, recipe)
                conn.commit()

    #rowUpdateStatement(len(dbList), curs, conn)


# A statement that prints when database is asked to update information
def rowUpdateStatement(numb, curs, conn):
    numChanges = len(lookAtDB(conn)) - numb
    if numChanges > 0:
        print("\t\t\t\tRecords inserted successfully into Recipes table:", numChanges, "\n")
    else:
        print("\t\t\t\tNo new records were added to Recipes table\n")


# loads recipes from database into the recipes listbox
def loadRecipes(master, recipeRows):
    for i in recipeRows:
        master.recListbox.insert(tk.END, i[0])


def pullRecord(master, conn, self):
    conn.text_factory = str
    curs = conn.cursor()
    name = [master.recListbox.get(tk.ANCHOR)]
    sqlCom = '''SELECT * FROM Recipes WHERE title = (?)'''
    curs.execute(sqlCom, name)
    record = curs.fetchone()
    addGroceries(record, conn, master)


tempList = []
def addGroceries(record, conn, master):
    listbox = []
    temptemplist = []
    glbList = []
    value = ['NULL', record[0], record[1]]
    for i in record:
        if i in value:
            continue
        else:
            if i is not None:
                listbox.append(i)
    for i in listbox:
        tempList.append(i)
    tempSet = set(tempList)
    for i in tempSet:
        temptemplist.append(f'{i} ({tempList.count(i)})')
    for i in temptemplist:
        glbList.append(i)
    master.glbVar.set(glbList)
