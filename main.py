import storagemanager as sm
import tkinter as tk
import GUI as gui

data=sm.load_database()
PasswordGUI=gui.password_GUI(data)
PasswordGUI.run()   
