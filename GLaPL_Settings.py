
import tkinter as tk
#from tkinter import *
from tkinter import END, Entry, Variable, ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import re
from venv import create
import sys
import learner as l
import GLaPLUtilities as util

class GLaPL_Settings:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root

        check_num_wrapper = (self.root.register(util.CheckNum),'%P')
        check_num_0to1_wrapper = (self.root.register(util.CheckNum0to1), '%P')
        check_numList_wrapper = (self.root.register(util.CheckNumList),'%P')

        g = l.Grammar()

        platform = sys.platform

