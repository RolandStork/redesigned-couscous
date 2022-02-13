from tkinter import Button, Canvas, Entry, Label, Tk, Frame, Checkbutton, IntVar
from functools import partial
from lib.db.db import Db
from pass_tools import Generator, Hasher
from enc import Cypher

import webbrowser

class AuthenticationS():

    def __init__(self):
        self.db = Db()
        self.new = self.db.get_configuration()
        self.window = Tk()
        self.window.update()
        self.window.geometry("550x450")
        self.window.title("Redesigned Couscous")
    
    def get_help(self):
        """
        This will open the help guide in browser.
        """
        webbrowser.open("https://github.com/r3veal/redesigned-couscous", new=2)

    def new_user(self):
        """
        This will create a new database for new users.
        """
        self.window.geometry("550x450")
        self.window.title("Creating new Database")

        master_pass_label = Label(self.window, text="Master Password")
        master_pass_label.config(anchor="center")
        master_pass_label.pack(pady=10)

        master_pass_entry = Entry(self.window, width=30, show="*")
        master_pass_entry.pack()
        master_pass_entry.focus()

        confirm_label = Label(self.window, text="Confirm Master Boot")
        confirm_label.config(anchor="center")
        confirm_label.pack(pady=10)

        confirm_label_entry = Entry(self.window, width=30, show="*")
        confirm_label_entry.pack()

        self.feedback = Label(self.window)
        self.feedback.anchor(anchor="center")
        self.feedback.pack()

        keyfile_variable = IntVar(value=1)
        keyfile_checkbox = Checkbutton(
            self.window,
            text="Keyfile",
            variable=keyfile_variable,
            onvalue=1,
            offvalue=0,
        )
        keyfile_checkbox.pack()

        help_button = Button(
            text="Need Help?",
            command=self.get_help
        )
        help_button.config(anchor="center")
        help_button.pack()

        create_button = Button(
            self.window,
            text="Create Database",
            command=partial(self.save_info, master_pass_entry, confirm_label_entry, keyfile_variable)
        )
        create_button.anchor(anchor="center")
        create_button.pack()
    
    def save_info(self, master_password: str, confirmed_master_password: str, keyfile: int):
        """
        Saves the password's hash in the database.
        and it creates a keyfile if needed.
        """
        master_password = master_password.get()
        confirmed_master_password = confirmed_master_password.get()
        keyfile = keyfile.get()
        if len(master_password) < 8:
            self.feedback.config(text="Password Too Short!\nAt Least 8 Characters.", fg="red")
            return 1

        if master_password == confirmed_master_password:
            if keyfile == 1:
                # Keyfile
                keyfile: str = Generator().gen_key()
                keyfile_hash: str = Hasher().create_hash(keyfile)

                with open("KEYFILE", "w") as file:
                    file.write(keyfile)
                
                # Password
                password_hash: str = Hasher().create_hash(master_password)

                # salt
                salt: bytes = Generator().gen_salt()

            else:
                # Password
                password_hash: str = Hasher().create_hash(master_password)

                # salt
                salt: bytes = Generator().gen_salt()
        else:
            self.feedback.config(text="Passwords Do Not Match", fg="red")
            return 1


auth = AuthenticationS()
print(auth.new)
auth.new_user()
auth.window.mainloop()