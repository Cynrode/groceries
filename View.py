from Controller import *

# Header
# HawkP13
# Programmer: David Hawk
# Email: dhawk3@cnm.edu
# Purpose: Help my wife and I create shopping list based around planned dinner recipes


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
        self.recListbox.bind('<Button-1>', )

        self.glbList = []
        self.glbVar = tk.Variable(value='')
        self.grocListbox = tk.Listbox(body, listvariable=self.glbVar)
        # buttons
        self.add_recipe = tk.Button(body, text='Add Recipe', command=self.createRecipeButton)
        self.remove_recipe = tk.Button(body, text='Remove Recipe', command=lambda: (removeRecipe(self)))
        self.add_item = tk.Button(body, text='Add Item', command=ErrorWindow)
        self.remove_item = tk.Button(body, text='Remove Item', command=ErrorWindow)
        # bottom
        # self.frame = tk.Frame(bottom)
        self.saveBut = tk.Button(bottom, text='Save', command=ErrorWindow)
        # textInfo Frame
        self.TItitleVar = tk.StringVar()
        self.TItitleVar.set("Recipe: ")
        self.TItitle = tk.Label(textInfo, textvariable=self.TItitleVar)

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
        self.TItitle.grid(row=0, sticky='w')
        self.TIingredients.grid(row=1, sticky='w')
        self.TIlink.grid(row=2, sticky='w')

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

    def createRecipeButton(self):
        self.window = Window(self)

def updateTextInfo(self):
    textInfoTuple = pullRecIngredients(app.recListbox.get(tk.ANCHOR))
    textInfoList = [x for x in textInfoTuple[0]]
    app.TItitleVar.set('Recipe: ' + textInfoList[0])
    ingredientString = textInfoList[2]
    i = 3
    while i < len(textInfoList):
        if textInfoList[i] is None:
            break
        else:
            ingredientString += f', {str(textInfoList[i])}'
        i += 1
    app.TIingredVar.set('Ingredients: ' + ingredientString)


class Window(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        def __init__(self, parent):
            super().__init__(parent)
        self.grab_set()
        self.recipeLabel = tk.Label(self, text='Recipe Name', anchor='w')
        self.recipeField = tk.Entry(self)
        self.ingredientLabels = {}
        self.ingredientEntrys = {}
        self.submitButton = tk.Button(self, text='Submit', command=self.captureNupdate)
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


    def captureNupdate(self):
        recipeCapture(self)
        loadRecipes(app)


# Start GUI
root = tk.Tk()
app = MainGui(root)

conn = create_connection()
create_project(conn, app)
db_init_fileList = read_dbinit_file(app)
addRecipe(db_init_fileList)
loadRecipes(app)
Errors = reportErrors(app)


pullRecord = partial(pullRecord, app, conn)
app.recListbox.bind('<Double-Button-1>', pullRecord)
app.recListbox.bind('<<ListboxSelect>>', updateTextInfo)



#End GUI
root.mainloop()
"""4.	Your program must incorporate the following:
    a.	Use of loops and conditionals (while loops and if then for example)
    b.	Use of exception handling when getting user input where applicable.
    c.	Ability to save and retrieve data using either files and/or databases.
        For example: if you make a game, save the high score. PICK ONE OR THE OTHER. DATABASE OR FILE
    d.	Ability to get input from the user
    e.	Ability to display information
    f.	Exhibit a reasonable level of complexity (Minimum 50-100 lines of code), Minimum of 3 Data Types in the code) .
        It should be comparable to the last few programing assignments you have completed.
        Don’t select too difficult a project!
    g.	Should, if possible, be related to your degree major.

5.	IMPORTANT: If you use other sources (such as on-line tutorials) to create your program you must reference,
    in your comments, what you used. Include the name of the organization/person who authored the tutorial and provide
    a url to the website or a reference to the book used. Your project should involve some modifications to this work
    and state what modification you made.

DUE August 7th ,2022 at 11:59 pm."""