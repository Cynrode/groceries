import sqlite3
import tkinter as tk
from tkinter import Menu
from functools import partial
from tkinter import messagebox

# Global Variables
globalGroceryList = []
Errors = []


class MainGui(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        myFrame = tk.Frame(master)
        top = tk.Frame(master)
        body = tk.Frame(master)
        bottom = tk.Frame(master)
        textInfo = tk.Frame(bottom, highlightbackground='grey', highlightthickness=1,
                            background='white', border=2, height=5, width=7)

        # Status bar
        self.statusVar = tk.StringVar()
        self.statusVar.set("Initial Value")
        self.statusBar = tk.Label(master, textvariable=self.statusVar, bd=1, relief='sunken', anchor='w')

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
        self.instructions = tk.Label(top, text='Double click recipes to add ingredients to your shopping list\n',
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
        self.add_recipe = tk.Button(body, text='Add Recipe', command=lambda: (Window(master)))
        self.remove_recipe = tk.Button(body, text='Remove Recipe', command=lambda: (removeRecipe(self)))
        self.add_item = tk.Button(body, text='Add Item', command=ErrorWindow)
        self.remove_item = tk.Button(body, text='Remove Item', command=ErrorWindow)
        # bottom
        # self.frame = tk.Frame(bottom)
        self.saveBut = tk.Button(bottom, text='Save', command=ErrorWindow)
        # textInfo Frame
        self.TIdescriptVar = tk.StringVar()
        self.TIdescriptVar.set("Description: ")
        self.TIdescription = tk.Label(textInfo, textvariable=self.TIdescriptVar)

        self.TIingredVar = tk.StringVar()
        self.TIingredVar.set("Ingredients: ")
        self.TIingredients = tk.Label(textInfo, textvariable=self.TIingredVar)

        self.TIlinkVar = tk.StringVar()
        self.TIlinkVar.set("Recipe Link: ")
        self.TIlink = tk.Label(textInfo, textvariable=self.TIlinkVar)

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
        textInfo.grid(row=0, column=1, columnspan=2, sticky='nsew')
        self.saveBut.grid(row=1, column=0, columnspan=3, pady=5)
        self.statusBar.grid(row=3, column=0, columnspan=2, sticky='we')

        # textInfo Frame
        self.TIdescription.grid(row=0)
        self.TIingredients.grid(row=1)
        self.TIlink.grid(row=2)

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


class Window(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.grab_set()
        self.recipeLabel = tk.Label(self, text='Recipe Name', anchor='w')
        self.recipeField = tk.Entry(self)
        self.ingredientLabels = {}
        self.ingredientEntrys = {}
        self.submitButton = tk.Button(self, text='Submit', command=lambda: (recipeCapture(self, )))
        for i in range(1, 16):
            name = ('ingredient' + str(i))
            self.ingredientLabels[name] = tk.Label(self, text='Ingredient'+str(i),
                                                   anchor='w')
            self.ingredientLabels[name].grid(column=0, row=i+1, padx=7, stick='ew')
            self.ingredientEntrys[name] = tk.Entry(self)
            self.ingredientEntrys[name].grid(column=1, row=i+1, padx=10, sticky='ew')

        self.recipeLabel.grid(row=0, column=0, padx=10, sticky='ew')
        self.recipeField.grid(row=0, column=1, padx=10)
        self.submitButton.grid(row=17, column=0, columnspan=2, pady=10)



def ErrorWindow():
    tk.messagebox.showinfo("Error", "This feature is currently in development")


def recipeCapture(self):
    newRecipe = [self.recipeField.get()]
    listOfList_LazyProgramming = []
    if newRecipe[0] == "":
        newRecipe.pop(0)
        tk.messagebox.showinfo("Error", "The recipe must have a title")
    else:
        newRecipe.append('NULL')
        for i in range(1, 16):
            name = ('ingredient' + str(i))
            if self.ingredientEntrys[name].get() == '':
                continue
            else:
                newRecipe.append(self.ingredientEntrys[name].get())
    listOfList_LazyProgramming.append(newRecipe)
    addRecipe(listOfList_LazyProgramming)
    close_win(self)
    loadRecipes(self)
    return


def close_win(self):
    print(self.master)
    self.destroy()


def read_dbinit_file(master):
    recipeList = []
    global Errors
    try:
        master.statusVar.set('Reading startup recipes')
        with open('seedRecipes.txt') as file:
            # iterate through each line in the file
            for line in file:
                # separates each line into items using the ',' as a delimiter, strips the trailing space and saves it as
                # variable point
                recipe = line.strip('\n').split(',')
                recipeList.append(recipe)
        master.statusVar.set('Starter recipe list created')
        return recipeList
    except FileNotFoundError:
        Errors.append('SeedRecipes.txt file is missing')
    except:
        Errors.append('Error reading startup recipes')


def create_connection():
    try:
        dbname = 'Grocery_DB'
        conn = sqlite3.connect(dbname)
        return conn
    except:
        Errors.append('Error connecting to the database')


# verifies if table 'TblPoints' exists. If not, it creates it.
def create_project(conn, master):
    global Errors
    try:
        master.statusVar.set('Verifying table initialization')
        curs = conn.cursor()
        x = 'description TEXT NULL'
        for i in range(15):
            x += f',ingredient{i + 1} TEXT NULL'
        sqlCmd = f'CREATE TABLE IF NOT EXISTS Recipes(title TEXT NOT NULL PRIMARY KEY,{x})'
        curs.execute(sqlCmd)
        master.statusVar.set('Table verified/created')
    except:
        Errors.append('Error initializing table')


def lookAtDB():
    global Errors
    conn = create_connection()
    try:
        curs = conn.cursor()
        curs.execute('SELECT * FROM Recipes ORDER BY description ASC')
        recipeRows = curs.fetchall()
        return recipeRows
    except:
        Errors.append('Error looking at the database')


def pullRecTitles():
    try:
        conn = create_connection()
        curs = conn.cursor()
        sqlCmd = (f"SELECT title FROM Recipes ORDER BY description DESC")
        curs.execute(sqlCmd)
        titles = curs.fetchall()
        return titles
    except:
        Errors.append('Error retrieving recipe titles')


def pullRecIngredients(conn, gui, recipeTitle='*'):
    try:
        gui.statusVar.set(f'Retrieving recipe ingredients for {recipeTitle}')
        curs = conn.cursor()
        x = 'ingredient1'
        for i in range(14):
            x += f',ingredient{i + 1}'
        curs.execute(f'SELECT {x} WHERE title = "{recipeTitle}"')
        ingredientList = curs.fetchall()
        gui.statusVar.set(f'List of ingredients for {recipeTitle} retrieved')
        return ingredientList
    except:
        Errors.append(f'Error retrieving ingredients for {recipeTitle}')


def addRecipe(listOfRecipes):
    global Errors
    try:
        conn = create_connection()
        curs = conn.cursor()
        # Using list comprehension, we compile recipe titles from our recipefileseed into one list to prevent
        # duplication
        rfTitles = [recipe[0] for recipe in listOfRecipes]
        # We create a dictionary from our recipes passed to the function (setup this way in case we want to pass files
        # with several recipes inside) as a dictionary (hash map) and then use the recipe title as our key. This follows
        # our database design built to use recipe title as the primary key. In the future, we can build this around a
        # more complex primary key, such as title + author.
        recipeDict = {rfTitles[i]: listOfRecipes[i] for i in range(len(listOfRecipes))}
        # Pull all recipe titles from our database
        dbRecTitles = pullRecTitles()
        # Using list comprehension, we compile recipe titles from our database into one list to prevent duplication
        dbTitles = [title for title, in dbRecTitles]
        for title in rfTitles:
            if title in dbTitles:
                continue
            else:
                recipe = recipeDict.get(title)
                ingredientColumns = 'ingredient1'
                numArgs = '?,?,?'
                for j in range(1, len(recipe) - 2):
                    ingredientColumns += f',ingredient{j + 1}'
                    numArgs += f',?'
                insert = f'INSERT INTO Recipes(title, description, {ingredientColumns})'
                sqlCmd = f'{insert} VALUES({numArgs})'
                curs.execute(sqlCmd, recipe)
                conn.commit()
    except UnboundLocalError:
        Errors.append(f'recipeListFile failed to load')
    except IndexError:
        Errors.append(IndexError)
        print(IndexError)
    except sqlite3.IntegrityError:
        Errors.append(f'{title} failed to process. Recipe already exists in DB')


# loads recipes from database into the recipes listbox
def loadRecipes(master):
    recipeRows = lookAtDB()
    dbRecipeLoad = []
    global Errors
    try:
        master.statusVar.set('Loading recipes from database into GUI')
        master.recListbox.delete(0, tk.END)
        for i in recipeRows:
            master.recListbox.insert(tk.END, i[0])
    except:
        Errors.append('Error reading recipes from database')


def pullRecord(master, conn, self):
    name = [master.recListbox.get(tk.ANCHOR)]
    try:
        conn.text_factory = str
        curs = conn.cursor()
        master.statusVar.set(f'Fetching recipe from database for {name}')
        sqlCom = '''SELECT * FROM Recipes WHERE title = (?)'''
        curs.execute(sqlCom, name)
        selectedRecipe = curs.fetchone()
        addGroceries(selectedRecipe, master)
    except:
        Errors.append(f'Failed to fetch {name}')


def addGroceries(selectedRecipe, master):
    try:
        master.statusVar.set(f'Adding ingredients from {selectedRecipe[0]} recipe to the grocery list')
        tempTemplist = []
        glbList = []
        # used to pull out information from recipe record that aren't ingredients with following if statement
        notIngredients = ['NULL', selectedRecipe[0], selectedRecipe[1]]
        for i in selectedRecipe:
            if i in notIngredients:
                continue
            else:
                if i is not None:
                    globalGroceryList.append(i)
        # tempSet creates a set that removes redundant entries in our globalGroceryList to prepare formatting for our
        # grocery listbox display
        tempSet = set(globalGroceryList)
        for i in tempSet:
            tempTemplist.append(f'{i} ({globalGroceryList.count(i)})')
        for i in tempTemplist:
            glbList.append(i)
        master.glbVar.set(glbList)
    except:
        Errors.append(f'Error adding ingredients from {selectedRecipe[0]} recipe to grocery list')
    finally:
        Errors.append(f'Ingredients for {selectedRecipe[0]} added successfully')


def reportErrors(master):
    if len(Errors) < 1:
        master.statusVar.set('Program loaded successfully.')
    else:
        ErrorStatus = []
        i = 0
        while i <= len(Errors):
            if len(ErrorStatus) < 1:
                ErrorStatus.append(Errors[0])
                Errors.pop(0)
                i += 1
            else:
                ErrorStatus.append(Errors[0])
                Errors.pop(0)
                i += 1
        master.statusVar.set(', '.join(ErrorStatus))


def removeRecipe(master):
    name = [master.recListbox.get(tk.ANCHOR)]
    conn = create_connection()
    try:
        conn.text_factory = str
        curs = conn.cursor()
        master.statusVar.set(f'Deleting recipe from database for {name[0]}')
        curs.execute('DELETE FROM Recipes WHERE title=?', name)
        conn.commit()
        loadRecipes(master)
    except:
        Errors.append(f'Failed to delete {name}')
