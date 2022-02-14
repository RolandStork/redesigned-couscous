from tkinter import Button, Canvas, Entry, Label, Tk, Frame, Checkbutton, IntVar, filedialog, PhotoImage, LabelFrame

import random
import os
import hashlib
import string

class Generator():
    """
    Generates a custom password, keyfile, and salt.
    """
    def __init__(self):
        self.digits = string.digits
        self.letters = string.ascii_letters
        self.punctuation = string.punctuation
        self.default_settings = {
            "Digits": True,
            "Punctuation": True,
            "Letters": True,
            "Number of Spaces": 2,
            "Length": 20
        }
        self.keyfile_settings = {
            "Digits": True,
            "Punctuation": True,
            "Letters": True,
            "Number of Spaces": random.randint(1, 25),
            "Length": 256
        }

    def gen_password(self, settings: dict = None) -> str:
        """
        Generates a Password with custom settings.
        """
        settings = settings or self.default_settings
        password = []

        settings_ = [key for key, value in settings.items() if value == True]

        if settings.get("Number of Spaces") != 0:
            for i in range(settings.get("Number of Spaces")):
                password.append(" ")
        
        while len(password) < settings.get("Length"):
            setting = random.choice(settings_)
            if setting == "Digits":
                password.append(random.choice(self.digits))
            elif setting == "Letters":
                password.append(random.choice(self.letters))
            elif setting == "Punctuation":
                password.append(random.choice(self.punctuation))
        
        random.shuffle(password)

        return "".join(password)

    def gen_key(self) -> str:
        """
        Generates a 256 bytes key for the KEYFILE
        """
        return self.gen_password(self.keyfile_settings)
    
    def gen_salt(self) -> bytes:
        """
        Generates a permanent salt for the encryption.
        """
        return os.urandom(32)

class Hasher():
    """
    Generates and checks a hash.
    """
    def create_hash(self, password: str) -> str:
        """
        Generates a SHA256 hash.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    def check_hash(self, password: str, hashed_version: str) -> bool:
        """
        Checks the password and the hash.
        """
        if hashlib.sha256(password.encode("utf-8")).hexdigest() == hashed_version:
            return True
        else:
            return False

class GuiGenerator(Generator):
    """
    Generator but GUI
    """
    def __init__(self):
        super().__init__()

        self.window = Tk()
        self.window.update()

        logo = PhotoImage(file="mystery-box.png")
        self.window.iconphoto(True, logo)
        self.window.geometry("500x250")
        self.window.resizable(False, False)
        self.window.title("Password Generator")
    
    def gui_gen(self):
        """
        GUI Generator Function.
        """
        pass_label = Label(self.window, text="Password:")
        pass_label.grid(
            column=0,
            row=0,
            padx=(10,0),
            pady=(10,0)
        )

        password_entry = Entry(self.window, width=50, text="asdjhads")
        password_entry.grid(
            column=1,
            row=0,
            padx=(0,0),
            pady=(10,0)
        )
        
        copy_to_clipboard = Button(self.window, text="Copy")
        copy_to_clipboard.grid(
            column=2,
            row=0,
            padx=(0,10),
            pady=(10,0)
        )


        configuration_frame = LabelFrame(self.window, text="Configuration")
        configuration_frame.grid(
            columnspan=3
        )


        letter_variable = IntVar(value=1)
        letter_checkbox = Checkbutton(
            configuration_frame,
            text="Letters  ",
            variable=letter_variable,
            onvalue=1,
            offvalue=0,
        )
        letter_checkbox.grid(
            column=0,
            row=0
        )

        punctuation_variable = IntVar(value=1)
        letter_checkbox = Checkbutton(
            configuration_frame,
            text="Punctuation  ",
            variable=punctuation_variable,
            onvalue=1,
            offvalue=0,
        )
        letter_checkbox.grid(
            column=1,
            row=0
        )

        digits_variable = IntVar(value=1)
        letter_checkbox = Checkbutton(
            configuration_frame,
            text="Digits  ",
            variable=digits_variable,
            onvalue=1,
            offvalue=0,
        )
        letter_checkbox.grid(
            column=2,
            row=0
        )

        pass_label = Label(configuration_frame, text="Length:")
        pass_label.grid(
            column=0,
            row=1,
            sticky="w"
        )

        password_entry = Entry(configuration_frame, text="20", width=2)
        password_entry.grid(
            column=0,
            row=1,
            sticky="e"
        )
        

gen = GuiGenerator()
gen.gui_gen()
gen.window.mainloop()