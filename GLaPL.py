# -*- coding: utf-8 -*-
'''
Created on Wed Oct 22 20:20:47 2025

@author: moore-cantwell
'''
import tkinter as tk
from tkinter import END, Entry, Variable, ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import re
from venv import create
import sys
import learner as l
import GLaPLUtilities as util
from GLaPL_Settings import Settings
from GLaPL_Console import Console
from GLaPL_Output import Output


root = tk.Tk()
check_num_wrapper = (root.register(util.CheckNum),'%P')
check_num_0to1_wrapper = (root.register(util.CheckNum0to1), '%P')
check_numList_wrapper = (root.register(util.CheckNumList),'%P')

g = l.Grammar()

    

# def util.SendParams():
#     if weightsRadioVar == 'all':
#         weightsEntryList
    

# Setting some window properties
root.title('GLaPL')
root.configure(background='grey')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.minsize(1280, 720)
root.maxsize(screen_width, screen_height)
root.geometry('300x300+50+50')

# Root Grid
width = 1280
height = 720
content = util.CreateFrame(util.Tkinter_Field_Settings(root, ipadx = 6, ipady = 6, column=0, row=0, maxColumn=1, maxRow=1, width=width, height=height, sticky='NSEW'))
settingsFrame = util.CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge', column=0, row=0, maxColumn=1, maxRow=1, 
                                                             columnSpan=1, rowSpan= 2, width=width*.525, height=height, sticky='NSEW'))
#settingsFrame.grid(column=0, row=0, columnspan=3, sticky='NSEW')
outputFrame = util.CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge', column=1, row=0, maxColumn=1, maxRow=1, 
                                                           columnSpan=1, rowSpan = 1, width=width*.475, height=height / 2, sticky='NSEW'))
#outputFrame.grid(column=3, row=0, columnspan=3, sticky='NSEW')
consoleFrame = util.CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge', column=1, row=1, maxColumn=1, maxRow=1, 
                                                            columnSpan=1, rowSpan = 1, width=width*.475, height=height / 2, sticky='NSEW'))
#consoleFrame.grid(column=3, row=1, columnspan=3, sticky='NSEW')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Configuring columns and rows to scale with the window
maxColumn = 2
maxRow = 2
for i in range(maxColumn):
    content.columnconfigure(i, weight=1)
for i in range(maxRow):
    content.rowconfigure(i, weight=1)
content.grid(column=0, row=0, sticky='NSEW')




#Settings Frame:

#Console Frame:
# ConsoleFrame(consoleFrame)
console = Console(root=root, frame=consoleFrame)
console.ConsoleFrame()

settings = Settings(root=root, frame=settingsFrame, console=console)
settings.SettingsFrame()


#Output Frame:
output = Output(root=root, frame=outputFrame)
output.OutputFrame()




root.mainloop()

#g = l.Grammar()

### run to package as one file - takes longer to load, 
### but easier to distribute
### pyinstaller --onefile app.py

