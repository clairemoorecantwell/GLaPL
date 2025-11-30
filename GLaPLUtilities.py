#!/usr/bin/env python3
import tkinter as tk
from tkinter import Variable, ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import re
import sys
import learner as l
from typing import NamedTuple

g = l.Grammar()
platform = sys.platform

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

def CheckNum0to1(newVal):
    _decimal = False
    _count = 0
    _firstChar = 0
    for char in newVal:
        _count += 1
        if _count > 15:
            return False
        if _count == 1 and char != '.' and (int(char) < 2):
            _firstChar = int(char)
            continue
        if _count == 1 and char != '.' and (int(char) > 1):
            return False
        if _count == 1 and char == '.':
            _decimal = True
            _firstChar = char
            continue
        if _count == 2 and _firstChar != '.' and char != '.':
            return False
        if char == '.' and _decimal == True:
            return False
        if char == '.' and _decimal == False:
            _decimal = True
            continue
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

def CreateFrame(arg):
    frame = tk.Frame(arg.parent, borderwidth=arg.borderWidth, width=arg.width, height=arg.height, relief=arg.relief)
    for i in range(arg.maxColumn):
        frame.columnconfigure(i, weight=arg.weightx)
    for i in range(arg.maxRow):
        frame.rowconfigure(i, weight=arg.weighty)
    frame.grid(column=arg.column, row=arg.row, columnspan=arg.columnSpan, rowspan=arg.rowSpan, sticky=arg.sticky, 
               padx = arg.padx, pady=arg.pady, ipadx=arg.ipadx, ipady=arg.ipady)
    return frame

def ToggleWeightsEntries(fieldList, active):
    for i in range(len(fieldList)):
        if any(x == i for x in active):
            fieldList[i].config(state = tk.NORMAL)
        else:
            fieldList[i].config(state = tk.DISABLED)

#not used - removing the command line prevents setting a default, it's also not able to intelligently not send a list for the values.
def CreateRadio_setParam(args, expandX = bool(True)):
    listItem = 0
    print(args)
    column = args.column
    row = args.row
    parameter = args.parameter
    _list = args.list
    for (text, value) in args.dictionary.items():
        print(text, value)
        commandVariable=args.variable[listItem]
        variable=args.radioVariable
        r = tk.Radiobutton(
            args.parent,
            text=text,
            value=value,
            variable=variable,
            command=lambda *args: g.setParam(parameter, [variable.get(), commandVariable]))
        r.grid(column=column, row=row, sticky=args.sticky, padx = args.padx, pady=args.pady, ipadx = args.ipadx, ipady = args.ipady)
        #find a solution for passing two variables through
        if (len(args.variable) > 1):
            listItem += 1
        if (expandX == True):
            column += 1
        else:
            row += 1
        _list.append(r)

def CreateEntry(args, b = None, fieldList = None, greyOut = None, fieldEntryList = None):
    if (b == 0):
        i = len(fieldList) - 1
        while i >= 0:
            fieldList[i].destroy()
            fieldList.remove(fieldList[i])
            i = i - 1
        greyOut.config(state = tk.NORMAL)
    else:
        for arg in args:
            fieldLabel = tk.Label(arg.parent, text = arg.text, width = arg.labelWidth, anchor='nw')
            fieldLabel.grid(column = arg.column, row = arg.row, sticky = arg.sticky, padx = arg.padx, 
                            ipadx = arg.ipadx, pady = arg.pady, ipady = arg.ipady)
            fieldEntry = tk.Entry(arg.parent, textvariable = arg.variable, validate = 'key', 
                                  validatecommand = arg.command, width = arg.entryWidth)
            fieldEntry.grid(column = arg.column +1, row = arg.row, sticky = arg.sticky, padx = arg.padx, 
                            ipadx = arg.ipadx, pady = arg.pady, ipady = arg.ipady)
            if fieldEntryList is not None:
                if fieldEntry not in fieldEntryList:
                    fieldEntryList.append(fieldEntry)
            if fieldList is not None:
                if fieldLabel not in fieldList:
                    fieldList.append(fieldLabel)
                if fieldEntry not in fieldList:
                    fieldList.append(fieldEntry)
        if greyOut is not None:
            greyOut.config(state = tk.DISABLED, disabledbackground = 'grey')
        return fieldEntry

def onFrameConfigure(canvas, frame):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.create_window((0,0), window=frame, anchor='nw')

def boundToMouseWheel(canvas, event):
    if platform == 'linux':
        canvas.bind_all("<Button-4>", onMouseWheel)
        canvas.bind_all("<Button-5>", onMouseWheel)
    else:
        canvas.bind_all("<MouseWheel>", onMouseWheel)

def unboundToMouseWheel(canvas, event):
    if platform == 'linux':
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
    else:
        canvas.unbind_all("<MouseWheel>")

def onMouseWheel(canvas, event):
    print(canvas)
    print(event)
    if platform == 'win32' or platform == 'cygwin' or platform == 'linux':
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    if platform == 'darwin':
        canvas.yview_scroll(int(-1*(event.delta)), "units")

def show_selected(values):
    selected_options = []
    for option, value in values.items():
        if value.get() == 1:
            selected_options.append(option)
    print("Selected options:", selected_options)

def getVars(param, entry):
    output = str(param)
    for e in entry:
        output += ','+e
    print (output)
    return output

def SendParams(param, type, value, convertToFloats = False):
    if convertToFloats == True:
        value = value.split(",")
    g.setParam(param, [type, value])

# def onNotebookTabChange(nb, nbScrollbars):
#     print('tab ', nb.index('current'))
#     nbActiveTab = nb.index('current')
#     for i in range(len(nbScrollbars)):
#         if i != nbActiveTab:
#             print('hiding tab ', i, ' scrollbar: ', nbScrollbars[i])
#             #nbScrollbars[i].grid_remove()
#             nbScrollbars[i].grid_forget()
#         else:
#             print('restoring tab ', i, ' scrollbar: ', nbScrollbars[i])
#             #nbScrollbars[i].grid()
#             nbScrollbars[i].grid(column=8, row=0, sticky='NS')

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


