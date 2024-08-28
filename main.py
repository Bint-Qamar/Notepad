import os
from tkinter import *
from tkinter import messagebox, filedialog


def cut():
    text.event_generate("<<Cut>>")

def copy():
    text.event_generate("<<Copy>>")

def paste():
    text.event_generate("<<Paste>>")


# Function to search for a string in the text
def find():
    def find_text():
        
        text.tag_remove('found', '1.0', END)

        search_query = find_entry.get()

        if search_query:
            index = '1.0'
            while True:
                index = text.search(search_query, index, nocase=1, stopindex=END)
                if not index:
                    break
                lastidx = f"{index}+{len(search_query)}c"
                text.tag_add('found', index, lastidx)
                index = lastidx
            text.tag_config('found', foreground='white', background='blue')

        find_popup.title("Find")
        find_popup.geometry("300x100")
        find_popup.maxsize(width=300, height=100)
        find_popup.minsize(width=300, height=100)

    find_popup = Toplevel(root)
    find_entry = Entry(find_popup, width=25)
    Label(find_popup, text="Find what:").pack(side=LEFT, padx=10, pady=10)
    find_entry.pack(side=LEFT, padx=10, pady=10)

    find_button = Button(find_popup, text="Find", command=find_text)
    find_button.pack(side=LEFT, padx=10, pady=10)

    find_popup.transient(root)
    find_popup.grab_set()
    root.wait_window(find_popup)




def replace():
    def replace_text():
        text.tag_remove('found', '1.0', END)
        s = find_entry.get()
        r = replace_entry.get()

        if s and r:
            index = '1.0'
            while True:
                index = text.search(s, index, nocase=1, stopindex=END)
                if not index:
                    break
                lastidx = f"{index}+{len(s)}c"
                text.delete(index, lastidx)
                text.insert(index, r)
                lastidx = f"{index}+{len(r)}c"
                text.tag_add('found', index, lastidx)
                index = lastidx
            text.tag_config('found', foreground='white', background='yellow')
    find_popup = Toplevel(root)
    find_entry = Entry(find_popup, width=25)
    replace_entry = Entry(find_popup, width=25)
    Label(find_popup, text="Find what:").grid()
    find_entry.grid(row = 0,column=1, padx=10, pady=10)
    Label(find_popup, text="Replace with:").grid()
    replace_entry.grid(row = 1,column=1, padx=10, pady=10)

    find_button = Button(find_popup, text="Replace all", command=replace_text)
    find_button.grid( column=1, padx=10, pady=10)

    find_popup.transient(root)
    find_popup.grab_set()
    root.wait_window(find_popup)


def newfile():
    global file
    root.title("Untitled - Notepad")
    file = None
    text.delete(1.0, END)


def openfile():
    global file
    file = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
    if file:
        root.title(os.path.basename(file) + " - Notepad")
        with open(file, "r") as file_content:
            text.delete("1.0", END)
            text.insert(END, file_content.read())


def savefile():
    global file
    if file:
        with open(file, "w") as file_content:
            file_content.write(text.get("1.0", END))
    else:
        saveasfile()


def saveasfile():
    global file
    file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "w") as file_content:
            file_content.write(text.get("1.0", END))
        root.title(os.path.basename(file) + " - Notepad")


def exit_app():
    root.destroy()


def help_info():
    messagebox.showinfo("Help", "This is a notepad created by Khansa. Feel free to use :)")


def create_menu():
    mainmenu = Menu(root)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label='New', command=newfile)
    filemenu.add_command(label='Open', command=openfile)
    filemenu.add_command(label='Save', command=savefile)
    filemenu.add_command(label='Save As', command=saveasfile)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=exit_app)
    mainmenu.add_cascade(label="File", menu=filemenu)

    editmenu = Menu(mainmenu, tearoff=0)
    editmenu.add_command(label='Cut', command=cut)
    editmenu.add_command(label='Copy', command=copy)
    editmenu.add_command(label='Paste', command=paste)
    editmenu.add_command(label='Find', command=find)
    editmenu.add_command(label='Replace', command=replace)
    mainmenu.add_cascade(label="Edit", menu=editmenu)

    mainmenu.add_command(label="Help", command=help_info)
    root.config(menu=mainmenu)


root = Tk()
root.title("Untitled - Notepad")

file = None

create_menu()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

text = Text(root, yscrollcommand=scrollbar.set)
text.pack(expand=True, fill=BOTH)
scrollbar.config(command=text.yview)

root.mainloop()
