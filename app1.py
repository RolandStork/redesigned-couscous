from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pandas.io import clipboard
from time import sleep

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
    print(event.keysym)
    print(event.char)
    print(event.widget.get())
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
            mb = messagebox.askquestion("Question",
                                        "Entered url not in database. Do you want to add?")
            if mb == "yes":
                mb1 = messagebox.askquestion("Confirm",
                                             "please confirm url: %s" % (url_search.get()))
                if mb1 == "yes":
                    url_list.append(url_search.get())
                    db[url_search.get()] = {}
                    un_search.set('please enter username...')


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


def clear_clipboard():
    sleep(10)
    clipboard.copy('')


def get_password():
    try:
        clipboard.copy(db[url_search.get()][un_search.get()])
        clear_clipboard()
    except:
        messagebox.showerror("", "Error: no password found")

"""database needs to be sync with encrypt """
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
""" ###########################################"""

root = Tk()
root.title('DIGITAL SECURITY')
root.iconbitmap('mystery-box.ico')
root.geometry("340x200")
# root.progressbar = ttk.Progressbar(root)
# root.progressbar.place(relx=.5, rely=.5, anchor="c")

f_size = 13
l_width = 9
v_width = 25
fg_color = '#404040'
bg_color = '#FFFFFF'

# img = ImageTk.PhotoImage(Image.open("mystery-box.png"))
# panel = Label(root, image=img)
# panel.pack(side="bottom", fill="both", expand="yes")
# panel.grid(row=0, column=1, pady=2)

style = ttk.Style()
style.theme_use('alt')
root.option_add('*TCombobox*Listbox*Background', '#FFFFFF')
root.option_add('*TCombobox*Listbox*Foreground', '#404040')
root.option_add('*TCombobox*Listbox*selectBackground', '#404040')
root.option_add('*TCombobox*Listbox*selectForeground', '#FFFFFF')

url_label = Label(root, text="Website", font=('Helvetica', f_size), width=l_width)
url_label.grid(row=1, column=0, pady=2)
url_search = ttk.Combobox(root, font=('Helvetica', f_size), width=v_width)
url_search.grid(row=1, column=1, pady=2)
url_search['values'] = url_list
url_search.bind('<KeyRelease>', set_url)
url_search.bind('<<ComboboxSelected>>', set_url)
url_search.bind('<Return>', enter_new_keys)

un_label = Label(root, text="Username", font=('Helvetica', f_size), width=l_width)
un_label.grid(row=3, column=0, pady=2)
un_search = ttk.Combobox(root, font=('Helvetica', f_size), width=v_width)
un_search.grid(row=3, column=1, pady=2)
un_search['values'] = ''
un_search.bind('<<ComboboxSelected>>', set_username)

p_label = Label(root, text="Password", font=('Helvetica', f_size), width=l_width)
p_label.grid(row=5, column=0, pady=2, sticky='w')
e = Entry(root, font=('Helvetica', f_size), width=v_width-5)
e.configure(state='readonly', show="*")
e.grid(row=5, column=1)
x1 = Button(root, font=('Helvetica', f_size), text="❐", command=get_password)
x1.grid(row=5, column=1, sticky='e')

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


