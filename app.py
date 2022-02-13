from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pandas.io import clipboard


def set_url(event):
    value = event.widget.get()
    if value == '':
        url_search['values'] = url_list
        un_search.set('')
        e.configure(state='normal')
        e.delete(0, END)
        e.insert(0, '')
        e.configure(state='readonly')
    else:
        data = []
        for item in url_list:
            if value.lower() in item.lower():
                data.append(item)

        url_search['values'] = data
        if data and url_search.get() in db.keys():
            un_search.set('')
            un_search['values'] = [*db[url_search.get()]]


def enter_new_keys(event):
    value = event.widget.get()
    if value == '':
        url_search['values'] = url_list
        un_search.set('')
        e.configure(state='normal')
        e.delete(0, END)
        e.insert(0, '')
        e.configure(state='readonly')
    else:
        data = []
        for item in url_list:
            if value.lower() in item.lower():
                data.append(item)

        url_search['values'] = data
        if data and url_search.get() in db.keys():
            un_search.set('')
            un_search['values'] = [*db[url_search.get()]]
        else:
            mb = messagebox.askquestion("askquestion",
                                        "Entered url not in database. Do you want to add?")
            if mb == "yes":
                pass


def set_username(event):
    value = event.widget.get()
    if value == '':
        url_search['values'] = url_list
        un_search['values'] = [*db[url_search.get()]]
        e.configure(state='normal')
        e.delete(0, END)
        e.insert(0, '')
        e.configure(state='readonly')
    else:
        data = []
        for item in [*db[url_search.get()]]:
            if value.lower() in item.lower():
                data.append(item)

        un_search['values'] = data
        e.configure(state='normal')
        e.delete(0, END)
        e.insert(0, db[url_search.get()][un_search.get()])
        e.configure(state='readonly')
        url_search['values'] = url_list


def get_password():
    try:
        clipboard.copy(db[url_search.get()][un_search.get()])
    except:
        messagebox.showerror("", "Error: no password found")


url_list = [
    "gmail.com",
    "outlook.live.com",
    "netflix.com",
    "primevideo.com",
    "hotstar.com"
]

db = {}
for i in url_list:
    db[i] = {}

db[url_list[0]]['xxx@gmail.com'] = 'xxx'
db[url_list[0]]['yyy@gmail.com'] = 'yyy'

db[url_list[2]]['prss'] = 'flixpass'
db[url_list[3]]['+1234'] = 'primepass'
db[url_list[1]]['+1234'] = 'mspass'
db[url_list[4]]['+1234'] = 'disneypass'

root = Tk()
root.title('Password Manager')
root.iconbitmap('mystery-box.ico')
root.geometry("300x200")

url_label = Label(root, text="url", width=10)
url_label.grid(row=0, column=0, pady=2)
url_search = ttk.Combobox(root)
url_search.grid(row=0, column=1, pady=2)
url_search['values'] = url_list
url_search.bind('<KeyRelease>', set_url)
url_search.bind('<<ComboboxSelected>>', set_url)
url_search.bind('<Return>', enter_new_keys)

un_label = Label(root, text="username")
un_label.grid(row=1, column=0, pady=2)
un_search = ttk.Combobox(root)
un_search.grid(row=1, column=1, pady=2)
un_search['values'] = ''
un_search.bind('<<ComboboxSelected>>', set_username)

p_label = Label(root, text="password")
p_label.grid(row=2, column=0, pady=2)
e = Entry(root)
e.configure(state='readonly', show="*")
e.grid(row=2, column=1)
x1 = Button(root, text="❐", command=get_password)
x1.grid(row=2, column=2)

root.mainloop()

"""
# messagebox options 
messagebox.showinfo("showinfo", "Information")
messagebox.showwarning("showwarning", "Warning")
messagebox.showerror("showerror", "Error")
messagebox.askquestion("askquestion", "Are you sure?")
messagebox.askokcancel("askokcancel", "Want to continue?")
messagebox.askyesno("askyesno", "Find the value?")
messagebox.askretrycancel("askretrycancel", "Try again?")  
"""
