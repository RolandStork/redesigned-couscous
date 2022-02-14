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
