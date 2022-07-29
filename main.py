from my_Functions import *

# Header
# HawkP13
# Programmer: David Hawk
# Email: dhawk3@cnm.edu
# Purpose: Help my wife and I create shopping list based around planned dinner recipes

def loadConn():
    return (conn, app)


# Start GUI
root = tk.Tk()
app = MainGui(root)

conn = create_connection(app)
create_project(conn, app)
db_init_fileList = read_dbinit_file(app)
addRecipe(conn, db_init_fileList, app)
loadRecipes(app, lookAtDB(conn, app))
Errors = reportErrors(app)


pullRecord = partial(pullRecord, app, conn)
app.recListbox.bind('<Double-Button-1>', pullRecord)

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