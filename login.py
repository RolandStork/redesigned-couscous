from tkinter import Button, Canvas, Entry, Label, Tk, Frame, Checkbutton, IntVar, filedialog, PhotoImage
from functools import partial
from lib.db.db import Db
from pass_tools import Generator, Hasher
from enc import Cypher

import webbrowser
import os

class AuthenticationS():

    def __init__(self):
        self.db = Db()
        self.configuration = self.db.get_configuration()

        self.window = Tk()
        self.window.update()

        logo = PhotoImage(file="mystery-box.png")
        self.window.iconphoto(True, logo)
        self.window.resizable(False, False)
        self.window.title("Redesigned Couscous")
    
    def new_user(self):
        """
        This will create a new database for new users.
        """
        self.window.geometry("500x250")
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
        create_button.config(anchor="center")
        create_button.pack()
    
    def login_with_keyfile(self):
        """
        Login to the database.
        """
        self.window.geometry("500x250")
        self.window.title("Login")

        password = Label(self.window, text="Enter Password")
        password.config(anchor="center")
        password.pack(pady=(50,10))

        password_entry = Entry(self.window, width=30, show="*")
        password_entry.pack()

        self.feedback = Label(self.window)
        self.feedback.anchor(anchor="center")
        self.feedback.pack()

        displayed_name = [i for i in self.configuration.get("keyfile_path", "").split("/")]

        if len(displayed_name) > 3:
            minimal_filepath = f"../{'/'.join(displayed_name[-3::])}"
        else:
            minimal_filepath = f"..{'/'.join(displayed_name[-3::])}"

        self.keyfile_path = Label(self.window, text=minimal_filepath, fg="green")
        self.keyfile_path.anchor(anchor="center")
        self.keyfile_path.pack()

        keyfile_button = Button(
            self.window,
            text="Select KEYFILE",
            command=self.browse_file
        )
        keyfile_button.config(anchor="center")
        keyfile_button.pack()

        login_button = Button(
            self.window,
            text="Login",
            command=partial(
                self.check_login_with_keyfile,
                password_entry
            )
        )
        login_button.config(anchor="center")
        login_button.pack(pady=(10,0))

    def login_without_keyfile(self):
        """
        Login to the database.
        """
        self.window.geometry("500x250")
        self.window.title("Login")

        password = Label(self.window, text="Enter Password")
        password.config(anchor="center")
        password.pack(pady=(50,10))

        password_entry = Entry(self.window, width=30, show="*")
        password_entry.pack()

        self.feedback = Label(self.window)
        self.feedback.anchor(anchor="center")
        self.feedback.pack()

        login_button = Button(
            self.window,
            text="Login",
            command=partial(
                self.check_login_without_keyfile,
                password_entry
            )
        )
        login_button.config(anchor="center")
        login_button.pack(pady=(10,0))

    def check_login_with_keyfile(self, password) -> bool:
        """
        This function will let you login to the database, and if set's up the encryption.
        """
        # Cheking Password
        password_hash_check: bool = Hasher().check_hash(password.get(), self.configuration.get("password_hash"))

        # Cheking KEYFILE
        with open(self.configuration.get("keyfile_path"), "r") as file:
            content = file.read()
        
        keyfile_hash_check: bool = Hasher().check_hash(content, self.configuration.get("keyfile_hash"))

        if password_hash_check == True and keyfile_hash_check == True:
            print("yay")
            return True
        else:
            if keyfile_hash_check == True and password_hash_check == False:
                self.feedback.config(text="Wrong Password!", fg="red")
                return False
            elif keyfile_hash_check == False and password_hash_check == True:
                self.feedback.config(text="Wrong KEYFILE!", fg="red")
                return False
            else:
                self.feedback.config(text="Wrong Password and KEYFILE!", fg="red")
                return False

    def check_login_without_keyfile(self, password) -> bool:
        """
        This function will let you login to the database, and if set's up the encryption.
        """
        # Cheking Password
        password_hash_check: bool = Hasher().check_hash(password.get(), self.configuration.get("password_hash"))

        if password_hash_check == True:
            print("yay")
            return True
        else:
            self.feedback.config(text="Wrong Password!", fg="red")
            return False

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
                
                keyfile_path = os.path.abspath("KEYFILE")
                print(keyfile_path)
                
                # Password
                password_hash: str = Hasher().create_hash(master_password)

                # salt
                salt: bytes = Generator().gen_salt()
                
                config_dict: dict = {
                    "password_hash": password_hash,
                    "keyfile_hash": keyfile_hash,
                    "keyfile_path": keyfile_path,
                    "salt": salt,
                }

                self.db.set_configuration(config_dict)
            else:
                # Password
                password_hash: str = Hasher().create_hash(master_password)

                # salt
                salt: bytes = Generator().gen_salt()

                config_dict: dict = {
                    "password_hash": password_hash,
                    "salt": salt
                }
                
                self.db.set_configuration(config_dict)
        else:
            self.feedback.config(text="Passwords Do Not Match", fg="red")
            return 1

    def get_help(self):
        """
        This will open the help guide in browser.
        """
        webbrowser.open("https://github.com/r3veal/redesigned-couscous", new=2)

    def browse_file(self):
        """
        Let's you insert the KEYFILE
        """
        file = filedialog.askopenfile(
            mode="r",
        )
        if file:
            filepath = os.path.abspath(file.name)

            displayed_name = [i for i in filepath.split("/")]

            if len(displayed_name) > 3:
                minimal_filepath = f"../{'/'.join(displayed_name[-3::])}"
            else:
                minimal_filepath = f"..{'/'.join(displayed_name[-3::])}"

            self.keyfile_path.config(text=minimal_filepath, fg="green")

            # Update Database
            self.configuration["keyfile_path"] = filepath

            new_config_dict: dict = {
                "password_hash": self.configuration["password_hash"],
                "keyfile_hash": self.configuration["keyfile_hash"],
                "keyfile_path": self.configuration["keyfile_path"],
                "salt": self.configuration["salt"]
            }

            self.db.set_configuration(new_config_dict)



# Test
auth = AuthenticationS()
print(auth.configuration)
auth.new_user()
auth.window.mainloop()