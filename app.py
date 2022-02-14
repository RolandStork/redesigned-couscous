from tkinter import *
from tkinter import ttk
# from tkinter.messagebox import showinfo
from tkinter import messagebox
from pandas.io import clipboard
from time import sleep


def clear_clipboard():
    sleep(10)
    clipboard.copy('')


class App(Tk):
    def __init__(self, url_list=None, db=None):
        super().__init__()
        if db is None:
            db = {}
        if url_list is None:
            url_list = []
        self.url_list = url_list
        self.db = db
        # configure root
        self.title('DIGITAL SECURED PASSWORD MANAGER')
        self.geometry('300x50')
        self.iconbitmap('mystery-box.ico')
        self.geometry("340x200")

        f_size = 13
        l_width = 9
        v_width = 25

        self.url_label = ttk.Label(self, text="Website", font=('Helvetica', f_size), width=l_width)
        self.url_label.grid(row=1, column=0, pady=2)
        self.url_search = ttk.Combobox(self, font=('Helvetica', f_size), width=v_width)
        self.url_search.grid(row=1, column=1, pady=2)
        self.url_search['values'] = self.url_list
        self.url_search.bind('<KeyRelease>', self.set_url)
        self.url_search.bind('<<ComboboxSelected>>', self.set_url)
        self.url_search.bind('<BackSpace>', self.set_url)
        self.url_search.bind('<Return>', self.config_url)

        self.un_label = ttk.Label(self, text="Username", font=('Helvetica', f_size), width=l_width)
        self.un_label.grid(row=3, column=0, pady=2)
        self.un_search = ttk.Combobox(self, font=('Helvetica', f_size), width=v_width)
        self.un_search.grid(row=3, column=1, pady=2)
        self.un_search['values'] = ''
        self.url_search.bind('<KeyRelease>', self.set_username)
        self.un_search.bind('<<ComboboxSelected>>', self.set_username)
        self.url_search.bind('<BackSpace>', self.set_username)
        self.url_search.bind('<Return>', self.config_username)

        self.p_label = ttk.Label(self, text="Password", font=('Helvetica', f_size), width=l_width)
        self.p_label.grid(row=5, column=0, pady=2, sticky='w')
        self.password = ttk.Entry(self, font=('Helvetica', f_size), width=v_width - 5)
        self.password.configure(state='readonly', show="*")
        self.password.grid(row=5, column=1)
        self.x1 = Button(self, font=('Helvetica', f_size), text="❐", command=self.get_password)
        self.x1.grid(row=5, column=1, sticky='e')

    def reset_all(self):
        self.url_search['values'] = url_list
        self.un_search['values'] = ''
        self.un_search.set('')
        self.set_password('')

    def set_url(self, event):
        value = event.widget.get()
        if value == '':
            self.url_search['values'] = url_list
            self.un_search['values'] = ''
            self.un_search.set('')
            self.set_password('')
        else:
            data = []
            for item in url_list:
                if value.lower() in item.lower():
                    data.append(item)
            self.url_search['values'] = data

            if data and self.url_search.get() in db.keys():
                self.un_search.set('')
                self.un_search['values'] = [*db[self.url_search.get()]]
            else:
                " will it be a new username scenario?  if Yes -> set_username handles it "
                pass

    def config_url(self, event):
        print(event.keysym)
        print(event.char)
        print(event.widget.get())
        value = event.widget.get()
        if value == '':
            self.url_search['values'] = url_list
            self.un_search['values'] = ''
            self.un_search.set('')
            self.set_password('')
        else:
            data = []
            for item in url_list:
                if value.lower() in item.lower():
                    data.append(item)
            self.url_search['values'] = data

            if data and self.url_search.get() in self.db.keys():
                self.un_search.set('')
                self.un_search['values'] = [*db[self.url_search.get()]]
            else:
                mb = messagebox.askquestion("Question", "Entered url not in database. Do you want to add?")
                if mb == "yes":
                    mb1 = messagebox.askquestion("Confirm", "please confirm url: %s" % (self.url_search.get()))
                    if mb1 == "yes":
                        self.url_list.append(self.url_search.get())
                        self.db[self.url_search.get()] = {}
                        # self.un_search.set('please enter username...')

    def set_username(self, event):
        self.url_search['values'] = url_list
        self.set_password('')
        value = event.widget.get()
        if value == '':
            if self.url_search.get() in self.db.keys():
                self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                self.un_search['values'] = ''
        else:
            data = []
            if self.url_search.get() in self.db.keys():
                for item in [*self.db[self.url_search.get()]]:
                    if value.lower() in item.lower():
                        data.append(item)
                self.un_search['values'] = data

                if data and self.un_search.get() in [*self.db[self.url_search.get()]]:
                    self.set_password(self.db[self.url_search.get()][self.un_search.get()])
                    self.un_search['values'] = [*self.db[self.url_search.get()]]
                else:
                    mb = messagebox.askquestion("Question", "Entered username not in database. Do you want to add?")
                    if mb == "yes":
                        mb1 = messagebox.askquestion("Confirm", "please confirm username: %s" % (self.un_search.get()))
                        if mb1 == "yes":
                            self.db[self.url_search.get()][self.un_search.get()] = 'testpass'
                            # need to add password here into database

            else:
                self.un_search['values'] = ''

    def config_username(self, event):
        self.url_search['values'] = url_list
        self.set_password('')
        value = event.widget.get()
        if value == '':
            if self.url_search.get() in self.db.keys():
                self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                self.un_search['values'] = ''
        else:
            data = []
            if self.url_search.get() in self.db.keys():
                for item in [*self.db[self.url_search.get()]]:
                    if value.lower() in item.lower():
                        data.append(item)
                self.un_search['values'] = data

                if data and self.un_search.get() in [*self.db[self.url_search.get()]]:
                    self.set_password(self.db[self.url_search.get()][self.un_search.get()])
                    self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                self.un_search['values'] = ''

    def set_password(self, p):
        self.password.configure(state='normal')
        self.password.delete(0, END)
        self.password.insert(0, p)
        self.password.configure(state='readonly')

    def get_password(self):
        try:
            clipboard.copy(self.db[self.url_search.get()][self.un_search.get()])
            clear_clipboard()
        except:
            messagebox.showerror("", "Error: Password not found. Please check website url and username")


if __name__ == "__main__":
    """ database needs to be sync with encrypt """
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
    """   ---------------------------------------   """
    app = App(url_list, db)
    app.mainloop()
