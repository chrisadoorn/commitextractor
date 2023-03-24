from tkinter import *
from tkinter import filedialog
from configparser import ConfigParser

root = Tk()
root.grid_columnconfigure(2, minsize=100)  # Here
def saveToCommitExtractorini():
    # Get the configparser object
    config_object = ConfigParser()

    # 3 sections in the config file, let's call them USERINFO and SERVERCONFIG
    config_object["postgresql"] = {
        "host": hostName.get(),
        "port": portport.get(),
        "database": databaseName.get(),
        "user": userName.get(),
        "paswword": paswword.get(),
        "schema": scheme.get()
    }

    config_object["process"] = {
        "run_parallel": numberProcesses.get()
    }

    config_object["ghsearch"] = {
        "import": "0",
        "importfile": root.ImportFile.get(),
        "extensions": extensionfile.get()
    }

    # Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)


def openFileDialog():
    root.ImportFile = filedialog.askopenfilename(initialdir="",title="Select GHSearch Json", filetypes=(("Json Files", "*.json"),))
    myLabelImportFile=Label(root,text = root.ImportFile).grid(row=12, column=1)

#creating inputfields & labels
myLabelPostGresQl = Label(root, text = "PostGresQl setting", font='Helvetica 14 bold')
myLabelHostName = Label(root, text = "hostname")
hostName = Entry(root)
myLabelDatabaseName = Label(root, text = "databasename")
databaseName = Entry(root)
myLabelPort = Label(root, text = "port")
port = Entry(root)
myLabelUsername = Label(root, text = "username")
userName = Entry(root)
myLabelPassword = Label(root, text = "password")
paswword = Entry(root)
myLabelscheme = Label(root, text = "scheme")
scheme = Entry(root)
myLabelNumberProcessors = Label(root, text = "number of processors")

myLabelProcessSettings = Label(root, text = "Processor setting", font='Helvetica 14 bold')
numberProcesses = Entry(root)

myLabelFileSettings = Label(root, text = "File setting", font='Helvetica 14 bold')
myButtonImportFile = Button(root,text = "Select GHSearsch Json file", command=openFileDialog, fg = "blue")
myLabelExtensionfile = Label(root, text = "extensions (seperated with spaces)", width=35)
extensionfile = Entry(root)

#place in window
myLabelPostGresQl.grid(row=0, column=0)
myLabelHostName.grid(row=1, column=0)
hostName.grid(row=1,column=1)
myLabelDatabaseName.grid(row=2, column=0)
databaseName.grid(row=2,column=1)
myLabelPort.grid(row=3, column=0)
port.grid(row=3,column=1)
myLabelUsername.grid(row=4, column=0)
userName.grid(row=4,column=1)
myLabelPassword.grid(row=5, column=0)
paswword.grid(row=5,column=1)
myLabelscheme.grid(row=6, column=0)
scheme.grid(row=6,column=1)

empty = Label(root, text='     ')
empty.grid(row=7, column=0)

myLabelProcessSettings.grid(row=8, column=0)
myLabelNumberProcessors.grid(row=9, column=0)
numberProcesses.grid(row=9,column=1)

empty2 = Label(root, text='     ')
empty2.grid(row=10, column=0)
myLabelFileSettings.grid(row=11, column=0)
myButtonImportFile.grid(row=12,column=0)
myLabelExtensionfile.grid(row=13, column=0)
extensionfile.grid(row=13,column=1)

myButton = Button(root,text = "Save to ini file", command=saveToCommitExtractorini, fg = "blue")
myButton.grid(row=16,column=1)

root.mainloop()

