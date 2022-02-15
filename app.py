from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pandas.io import clipboard
from time import sleep
# from tkinter import Canvas
from PIL import ImageTk, Image
from threading import Timer


# from ttkwidgets.autocomplete import AutocompleteCombobox

def clear_clipboard():
    sleep(10)
    clipboard.copy('')


class App(Tk):
    f_size = 13
    l_width = 9
    v_width = 25

    def __init__(self, url_list=None, db=None):
        super().__init__()
        if db is None:
            db = {}
        if url_list is None:
            url_list = []
        self.url_list = url_list
        self.db = db
        # self.wait_state = False
        # configure root
        self.eval('tk::PlaceWindow . center')
        self.title('DIGITAL SECURED PASSWORD MANAGER')
        self.geometry('300x50')
        self.iconbitmap('mystery-box.ico')
        self.geometry("340x200")

        global openeye, closedeye
        self.show_pass = False
        openeye = PhotoImage(file="oe16.png")
        closedeye = PhotoImage(file="ce16.png")

        self.url_label = ttk.Label(self, text="Website", font=('Helvetica', self.f_size), width=self.l_width)
        self.url_label.grid(row=1, column=0, pady=2)
        self.url_search = ttk.Combobox(self, font=('Helvetica', self.f_size), width=self.v_width)
        # self.url_search = AutocompleteCombobox(self, width=v_width, font=('Helvetica', f_size), completevalues=self.url_list)
        self.url_search.grid(row=1, column=1, pady=2)
        self.url_search['values'] = self.url_list
        self.url_search.bind('<KeyRelease>', self.set_url)
        self.url_search.bind('<<ComboboxSelected>>', self.set_url)
        self.url_search.bind('<BackSpace>', self.set_url)
        self.url_search.bind('<Return>', self.config_url)

        self.un_label = ttk.Label(self, text="Username", font=('Helvetica', self.f_size), width=self.l_width)
        self.un_label.grid(row=3, column=0, pady=2)
        self.un_search = ttk.Combobox(self, font=('Helvetica', self.f_size), width=self.v_width)
        self.un_search.grid(row=3, column=1, pady=2)
        self.un_search['values'] = ''
        self.un_search.bind('<KeyRelease>', self.set_username)
        # self.un_search.bind('<KeyPress>', self.set_username)
        self.un_search.bind('<<ComboboxSelected>>', self.set_username)
        self.un_search.bind('<BackSpace>', self.set_username)
        self.un_search.bind('<Return>', self.config_username)
        self.un_search.bind("<FocusIn>", self.clear_temp_text)

        self.p_label = ttk.Label(self, text="Password", font=('Helvetica', self.f_size), width=self.l_width)
        self.p_label.grid(row=5, column=0, pady=2, sticky='w')
        self.password = ttk.Entry(self, font=('Helvetica', self.f_size), width=self.v_width - 5)
        self.password.configure(state='readonly', show="*")
        self.password.grid(row=5, column=1)
        self.password.bind("<FocusIn>", self.clear_temp_text)
        self.password.bind("<Button-1>", self.clear_temp_text)
        self.password.bind("<Return>", self.create_password)
        # self.e1 = Button(self, font=('Helvetica', self.f_size), text="👁", command=self.get_password)
        # self.e1.grid(row=5, column=1, sticky='e')
        self.button_qwer = Button(self, borderwidth=0, image=openeye, command=self.show_password)
        self.button_qwer.image = openeye
        self.button_qwer.grid(row=5, column=1, padx=(160, 10))

        self.x1 = Button(self, font=('Helvetica', self.f_size), text="❐", command=self.get_password)
        self.x1.grid(row=5, column=1, sticky='e')

    def hide_password(self, *args):
        global openeye, closedeye
        self.button_qwer.grid_remove()
        self.show_pass = not self.show_pass
        self.button_qwer = Button(self, borderwidth=0, image=openeye, command=self.show_password)
        self.button_qwer.image = openeye
        self.button_qwer.grid(row=5, column=1, padx=(160, 10))
        self.password.configure(state='readonly', show="*")

    def show_password(self, *args):
        global openeye, closedeye
        self.button_qwer.grid_remove()
        self.show_pass = not self.show_pass
        if self.show_pass:
            self.button_qwer = Button(self, borderwidth=0, image=closedeye, command=self.show_password)
            self.button_qwer.image = closedeye
            self.button_qwer.grid(row=5, column=1, padx=(160, 10))
            self.password.configure(state='readonly', show="")
            # sleep(1)
            # self.hide_password()
            t = Timer(1.0, self.hide_password)
            t.start()
        else:
            self.button_qwer = Button(self, borderwidth=0, image=openeye, command=self.show_password)
            self.button_qwer.image = openeye
            self.button_qwer.grid(row=5, column=1, padx=(160, 10))
            self.password.configure(state='readonly', show="*")

    def print_(self, event):
        print(event.widget.get())

    def reset_all(self):
        self.url_search['values'] = self.url_list
        self.un_search['values'] = ''
        self.un_search.set('')
        self.set_password('')

    def set_url(self, event):
        value = event.widget.get()
        if value == '':
            self.url_search['values'] = self.url_list
            self.un_search['values'] = ''
            self.un_search.set('')
            self.set_password('')
        else:
            data = []
            for item in self.url_list:
                if value.lower() in item.lower():
                    data.append(item)
            self.url_search['values'] = data

            if data and self.url_search.get() in self.db.keys():
                self.un_search.set('')
                self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                " will it be a new username scenario?  if Yes -> set_username handles it "
                pass

    def config_url(self, event):
        value = event.widget.get()
        if value == '':
            self.url_search['values'] = self.url_list
            self.un_search['values'] = ''
            self.un_search.set('')
            self.set_password('')
        else:
            data = []
            for item in self.url_list:
                if value.lower() in item.lower():
                    data.append(item)
            self.url_search['values'] = data

            if data and self.url_search.get() in self.db.keys():
                self.un_search.set('')
                self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                mb = messagebox.askquestion("Question", "Entered url not in database. Do you want to add?")
                if mb == "yes":
                    mb1 = messagebox.askquestion("Confirm", "please confirm the url: %s" % (self.url_search.get()))
                    if mb1 == "yes":
                        self.url_list.append(self.url_search.get())
                        self.db[self.url_search.get()] = {}

                        # self.un_search.set('please enter username...')
                        # self.un_search.focus()
                        self.un_search.insert(0, "please enter username...")
                        # self.wait_state = True
                        # print(self.db)
                    else:
                        pass

    def clear_temp_text(self, event):
        # self.wait_variable(self.un_search.get())
        # self.un_search.delete(0, "end")
        if "please enter username..." in self.un_search.get():
            self.un_search.delete(0, "end")
        if "please enter password" in self.password.get():
            self.password.delete(0, "end")

    def set_username(self, event):
        # if self.wait_state:
        #     s_ = str(self.un_search.get())
        #     self.un_search.set(s_.replace("please enter username...", ""))
        #     self.un_search.focus()
        #     self.wait_state = False

        self.url_search['values'] = self.url_list
        self.set_password('')
        value = event.widget.get()
        if value == '':
            if self.url_search.get() in self.db.keys():
                self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                self.un_search['values'] = ''
        # elif "please enter username..." in self.un_search.get():
        #     s_ = str(self.un_search.get())
        #     self.un_search.set(s_.replace("please enter username...", ""))
        #     # self.un_search.set(str(event.keysym))
        #     self.un_search.focus()
        else:
            data = []
            if self.url_search.get() in self.db.keys():
                for item in [*self.db[self.url_search.get()]]:
                    if value.lower() in item.lower():
                        data.append(item)
                self.un_search['values'] = data

                if data and self.un_search.get() in [*self.db[self.url_search.get()]]:
                    if self.db[self.url_search.get()][self.un_search.get()]:
                        self.set_password(self.db[self.url_search.get()][self.un_search.get()])
                    else:
                        self.config_username()
                    self.un_search['values'] = [*self.db[self.url_search.get()]]
            else:
                self.un_search['values'] = ''

    def config_username(self, *args):
        try:
            if self.db[self.url_search.get()][self.un_search.get()] == None:
                self.password.configure(state='normal', show="")
                self.password.delete(0, END)
                self.password.insert(0, 'please enter password...')
        except:
            self.url_search['values'] = self.url_list
            self.set_password('')
            try:
                value = str((args)[0].widget.get())
            except:
                value = ''
            # value = event.widget.get()
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
                        if self.db[self.url_search.get()][self.un_search.get()]:
                            self.set_password(self.db[self.url_search.get()][self.un_search.get()])
                        else:
                            self.config_username()
                        self.un_search['values'] = [*self.db[self.url_search.get()]]
                    else:
                        if self.un_search.get() == "please enter username...":
                            self.clear_temp_text()
                        mb = messagebox.askquestion("Question", "Entered username not in database. Do you want to add?")
                        if mb == "yes":
                            mb1 = messagebox.askquestion("Confirm",
                                                         "please confirm username: %s" % (self.un_search.get()))
                            if mb1 == "yes":
                                self.db[self.url_search.get()][self.un_search.get()] = None
                                # need to add password here into database
                                self.password.configure(state='normal', show="")
                                self.password.delete(0, END)
                                self.password.insert(0, 'please enter password...')
                                # self.un_search.focus()
                                # self.password.focus()
                                # self.create_password()
                            else:
                                pass

                else:
                    self.un_search['values'] = ''

    def create_password(self, *args):
        if self.password.get == None:
            self.password.configure(state='normal', show="")
            self.password.delete(0, END)
            self.password.insert(0, 'please enter password...')

        else:
            # mb = messagebox.askquestion("Question", "please enter password")
            # if mb == "yes":
            #     mb1 = messagebox.askquestion("Confirm", "please confirm : %s" % (self.un_search.get()))
            try:
                self.password_c = ttk.Entry(self, font=('Helvetica', self.f_size), width=self.v_width - 5)
                self.password_c.grid(row=7, column=1)
                self.password_c.bind('<Return>', self.confirm_password)
                # self.password_c.focus()
                self.wrongpass = ttk.Entry(self, font=('Helvetica', self.f_size - 4), width=self.v_width - 5)
                self.wrongpass.configure(state='readonly', foreground="red")
                self.wrongpass.grid(row=9, column=1)
                self.password_c.focus()
            except:
                self.confirm_password()

    def confirm_password(self, *args):
        if self.password.get() == self.password_c.get() and self.password.get():
            self.db[self.url_search.get()][self.un_search.get()] = self.password.get()
            self.password.configure(state='readonly', show="*")
            # self.password_c.configure(state='readonly', show="*")

            print(self.db)
            self.url_search['values'] = self.url_list
            self.un_search['values'] = ''
            self.un_search.set('')
            self.url_search.set('')
            self.set_password('')
            self.password_c.grid_remove()
            self.wrongpass.grid_remove()
        elif self.password_c.get() == '':
            self.wrongpass.configure(state='normal')
            self.wrongpass.delete(0, END)
            self.wrongpass.configure(state='readonly')
            self.password_c.delete(0, END)
            self.password_c.focus()
        else:
            self.wrongpass.configure(state='normal')
            self.wrongpass.delete(0, END)
            self.wrongpass.insert(0, 'Password does not match... ')
            self.wrongpass.configure(state='readonly')

            self.password_c.delete(0, END)
            self.password_c.focus()

    def set_password(self, p):
        self.password.configure(state='normal')
        self.password.delete(0, END)
        self.password.insert(0, p)
        self.password.configure(state='readonly')

    def get_password(self):
        try:
            clipboard.copy(self.db[self.url_search.get()][self.un_search.get()])
            clear_clipboard()
            """ if you want you can try below without pandas """
            # self.clipboard_clear()
            # self.clipboard_append(self.db[self.url_search.get()][self.un_search.get()])
            # sleep(10)
            # self.clipboard_clear()
            # t = Timer(5.0, self.clear_clipboard)
            # t.start()
        except:
            messagebox.showerror("", "Error: Password not found. Please check website url and username")

    def clear_clipboard(self):
        self.clipboard_clear()


if __name__ == "__main__":
    """ database needs to be sync with encrypt """
    # url_list = [
    #     "gmail.com",
    #     "outlook.live.com",
    #     "netflix.com",
    #     "primevideo.com",
    #     "hotstar.com"
    # ]
    #
    # db = {}
    # for i in url_list:
    #     db[i] = {}
    #
    # db[url_list[0]]['xxx@gmail.com'] = 'xxx'
    # db[url_list[0]]['yyy@gmail.com'] = 'yyy'
    #
    # db[url_list[2]]['prss'] = 'flixpass'
    # db[url_list[3]]['+1234'] = 'primepass'
    # db[url_list[1]]['+1234'] = 'mspass'
    # db[url_list[4]]['+1234'] = 'disneypass'
    # """   ---------------------------------------   """
    # app = App(url_list, db)
    app = App()
    app.mainloop()
