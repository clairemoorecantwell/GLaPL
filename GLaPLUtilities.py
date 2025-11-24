#!/usr/bin/env python3
import tkinter as tk
from tkinter import Variable, ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import re
import learner as l
from typing import NamedTuple

g = l.Grammar()

validChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "."]

def CheckNum(newVal):
    _decimal = False
    _count = 0
    for char in newVal:
        _count += 1
        if _count > 15:
            return False
        if char == '.' and _decimal == True:
            return False
        if char == '.' and _decimal == False:
            _decimal = True
        if char not in validChars:
            return False
    return True

validListChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ".", ","]

def CheckNumList(newVal):
    _decimal = False
    _comma = False
    _count = 0
    for char in newVal:
        _count += 1
        if _count > 15:
            return False
        if char != '.' and char != ',':
            _comma = False
        if char == '.' and _decimal == True:
            return False
        if char == '.' and _decimal == False:
            _decimal = True
        if char == ',' and _comma == True:
            return False
        if char == ',' and _comma == False:
            if _count == 1:
                return False
            else:
                _comma = True
                _decimal = False
        if char not in validListChars:
            return False
    return True

#not used
def ValidateNum(self, input_text):
    if not input_text:
        return True
    try:
        float(input_text)
        return True
    except ValueError:
        return False

#not used
def delete(entry: tk.Entry):
    entry.config(validate='none')
    entry.delete(0, END)
    entry.config(validate='key')

def GetEntryValue(val):
    value = val.get()
    print('Entry value:', value)

def ShowSelectedDecayRate(val):
    showinfo(title='DecayRate', message=val.get())

def GetDirectory(value):
    folder = filedialog.askdirectory(initialdir= '.\\')
    value.set(folder)

def ReadTrainingData(param, m):
    filename = filedialog.askopenfilename(initialdir= '.\\')
    print(filename)
    x = g.setParam(param,filename)
    m.set(x)

def SendDictionary(param, dictionary):
    newDict = {}
    for key in dictionary:
        newDict[key] = dictionary[key].get()
    g.setParam(param, newDict)

def GetFile(value):
    filename = filedialog.askopenfilename()
    value.set(filename)

def FlipInt(value):
    if value.get() == 0:
        value.set(1)
        print(value.get())
        return value
    if value.get() == 1:
        value.set(0)
        print(value.get())
        return value

def PrintOutput(value):
    print(value.get())
def ConvertStringListToFloats(value):
    x = value.split(",")
    return x

class Tkinter_Field_Settings:
    def __init__(self, parent = None, relief = 'flat', text = None, column = int(0), maxColumn = int(0), 
                 columnSpan = int(1), row = int(0), maxRow = int(0), rowSpan = int(1), width = int(600), 
                 height = int(200), weightx = int(1), weighty = int(1), sticky = 'NSEW', variable = None, 
                 variableDefault = None, command = None, radioVariable = None, entry = None, padx = int(0), 
                 ipadx = int(0), pady = int(0), ipady = int(0), borderWidth = int(0), labelWidth = 12, 
                 entryWidth = 15, dictionary = None, _list = [], parameter = None):
        self.parent = parent
        self.text = text
        self.column = column
        self.maxColumn = maxColumn
        self.columnSpan = columnSpan
        self.row = row
        self.maxRow = maxRow
        self.rowSpan = rowSpan
        self.width = width
        self.height = height
        self.weightx = weightx
        self.weighty = weighty
        self.sticky = sticky
        self.variable = variable
        self.variableDefault = variable
        self.command = command
        self.radioVariable = radioVariable
        self.entry = entry
        self.padx = padx
        self.ipadx = ipadx
        self.pady = pady
        self.ipady = ipady
        self.borderWidth = borderWidth
        self.labelWidth = labelWidth
        self.entryWidth = entryWidth
        self.dictionary = dictionary
        self.list = _list
        self.parameter = parameter
        self.relief = relief


