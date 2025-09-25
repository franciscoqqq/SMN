# -*- coding: utf-8 -*-
"""
Created on Mon May 29 09:30:13 2023

@author: fquarin
"""

import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import os
import openpyxl
from datetime import datetime

#############################################
############ VENTANA PRINCIPAL ##############

###### Ventana Principal (root) ######
root = tk.Tk()
root.title("Nephelometer") 
root.geometry("")

frame = tk.Frame(root)
frame.pack()

##### INFO FRAME -1- #####

info_frame_1 = tk.LabelFrame(frame, text = "Información")
info_frame_1.grid(row=0, column=0)

root.mainloop()
